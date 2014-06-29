# std lib imports
from media import *
# django imports

# 3rd party imports
# app imports
from models import Picture


def img_read( text_line ):
	"""
	Read the image information from file and return the collage information as a list of image lists.
	"""
	index = text_line.find('#')
	text_line = text_line[:index]

	# split the text_line on commas
	words = text_line.split(',')
	if len(words) < 6:
	    return None

	info = []

	# process the values in words
	# first value is the filename (string), strip front and end spaces
	info.append(words[0].strip())
	# second value is the effect (string), strip front and end spaces
	info.append(words[1].strip())

	# third value is whether to remove the bluescreen or not (yes/no)
	if words[2].strip() == 'yes':
	    info.append(True)
	else:
	    info.append(False)

	# fourth and fifth values are coordinates
	info.append(int(words[3]))
	info.append(int(words[4]))
	# sixth value is the alpha
	info.append(float(words[5]))

	# seventh value is the mirroring
	if words[6].strip() == 'vertical':
	    info.append( 'vertical' )
	elif words[6].strip() == 'horizontal':
	    info.append( 'horizontal' )
	else:
	    info.append( 'none' )

	return info

def img_copy(info, bkg) :
	"""
	Inserts the image described by imagelist into the bkg image using the parameters in the image list.
	"""
	# for every pixel in the fg picture
	for p in getPixels( info[-1] ):
		red = get_red(p)
		green = get_green(p)
		blue = get_blue(p)

		if info[2]:
		    total = float(red + green + blue)
		    if total == 0.0:
		      	total = 1.0
		    blue_area = float(b) / total
		    # if we remove the blue and it is part of the blue screen
		    if blue_area > 0.38 and total > 50:
				continue

		try:
		    q = get_pixel(bkg, info[3] + get_x(p), info[4] + get_y(p))
		except:
		    # pixel is out of range
		    continue;

	alpha = info[5]

	new_red = red
	new_green = green
	new_blue = blue

	if info[1] == 'negative':
	  new_red = (255 - red)
	  new_green = (255 - green)
	  new_blue = (255 - blue)

	elif info[1] == 'swap':
	  new_red = blue
	  new_green = green
	  new_blue = red

	new_red = new_red * alpha + (1.0 - alpha) * getRed(q)
	new_green = new_green * alpha + (1.0 - alpha) * getGreen(q)
	new_blue = new_blue * alpha + (1.0 - alpha) * getBlue(q)

	set_color( q, makeColor( new_red, new_green, new_blue ) )    
    
def collage_read_file(file_name):
	"""
	Reads collage information from a text file and returns the collage information as a list of image lists.
	"""
	# open the file
	print 'opening ', filename
	fp = file(filename)
	info = []

	# read all of the lines of the file into memory
	lines = fp.readlines()

	# go through each text_line
	for text_line in lines:
	    # read the image information from the file
	    file_info = imageReadInformation( text_line )
	    # test if it read in valid information
	    if file_info == None:
			continue
	    # append this list into the info list
	    info.append(file_info)
	fp.close()
	return info


def collage_read_image(collage):
	"""
	Reads the picture data using the filenames stored in the collage(list of image lists) and stores the picture data in the 
	last element of each of the image lists.
	"""
  	# go through the list of image information
	for data in collage:
		# the filename is the first element of the list
		filename = data[0]
		pic = makePicture(filename)
		data.append( pic )

def collage_build(collage):
	"""
	Creates a blank background image and places each image in the collage background.
	Returns a background image.
	"""
	# calculate the size of the background
	width = 0
	height = 0
	for data in collage:
		rightside = data[3] + getWidth( data[-1] )
		if rightside > width:
  			width = rightside

	bottomside = data[4] + getHeight( data[-1] )
	if bottomside > height:
		height = bottomside

	bkg = makeEmptyPicture( width, height )

	for data in collage:
		imageCopyInto( data, bkg )
		return bkg


def collage_rebuild( collage, bkg ):
	"""
	Rebuilds the collage given an existing collage and background.
	"""
	# clear the background image
	bkg = create_color(255, 255, 255)
	# paste in all the collage images given the current settings
	for data in collage:
		img_copy(data, bkg)
	return bkg
