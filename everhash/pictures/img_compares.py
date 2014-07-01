# std lib imports
import os, time, re, urllib2

# django imports
# 3rd party lib imports
from PIL import Image
import logging

# app imports

# This is a custom built image comparison library to compare the similarities of 2 file images.
# This is based on a version of root mean square value comparison. 
# In this case, we pixelate R G B values and give each an index.
# Once R G B datas are indexed. we use histogram to organize the values to compare.

def image_similarity_bands_via_numpy(filepath1, filepath2):
    """
    This method uses numpy and reshapes image into band sizes and compare their individual elements.
    """

    import math
    import operator
    import numpy
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    # create thumbnails - resize em
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)
    
    # this eliminated unqual images - though not so smarts....
    if image1.size != image2.size or image1.getbands() != image2.getbands():
        return -1
    s = 0
    for band_index, band in enumerate(image1.getbands()):
        m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
        m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s

def image_similarity_histogram_via_pil(filepath1, filepath2):
	"""
	Collects a histogram from both file images and compare their differences in root mean square value.
	A value that is close to 0 indicates that both file images are highly similar.
	"""

    from PIL import Image
    import math
    import operator
    
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)
    
    h1 = image1.histogram()
    h2 = image2.histogram()
 
    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return rms

def image_similarity_greyscale_hash_code(filepath1, filepath2):
    """
	Converts both file images to greyscale hashcode and find the differences between both hashcodes. A single 
	difference in hashcode value indicates a different file.
    """
 
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    image1 = get_thumbnail(image1, greyscale=True)
    image2 = get_thumbnail(image2, greyscale=True)
    
    code1 = image_pixel_hash_code(image1)
    code2 = image_pixel_hash_code(image2)
    # use hamming distance to compare hashes
    res = hamming_distance(code1,code2)
    return res
    
def image_pixel_hash_code(image):
    """
    Taskes in an image and converts image pixels into hash code.
    """
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))  # '00010100...'
    hexadecimal = int(bits, 2).__format__('016x').upper()
    return hexadecimal
 
def hamming_distance(s1, s2):
    """
    Hamming distance between len1 and len2
    """
    len1, len2 = len(s1),len(s2)
    if len1!=len2: 
        "hamming distance works only for string of the same length, so i'll chop the longest sequence"
        if len1>len2:
            s1=s1[:-(len1-len2)]
        else:
            s2=s2[:-(len2-len1)]
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])

def get_thumbnail(image, size=(128,128), stretch_to_fit=False, greyscale=False):
    """
    Get a smaller version of the image - makes comparison much faster/easier. Note, small sampling size have also low accuracy
    """
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size); # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image
 
def mkdir_p_filepath(path):
    dirpath = os.path.dirname(os.path.abspath(path))
    mkdir_p(dirpath)
 
def mkdir_p(path):
    """Custom image file dirs"""
    import errno
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise