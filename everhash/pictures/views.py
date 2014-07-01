# std lib imports
from urlparse import urlparse
from random import randint
import urllib2
import datetime
import time

# django imports
from django.shortcuts import render_to_response
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

# third-party app imports
from boto.s3.key import Key
from boto.s3.connection import S3Connection

# app imports
from albums.models import Album
from tweets.views import search
from models import Picture
from everhash.settings.local import EMAIL_HOST_USER
from utils import get_s3_bucket, remove_duplicates
from .signals import send_email


def update_picture_database(album_name):
	"""
	Updates the picture database that has field name 'album_name'.

	Performs a twitter REST API search with 'album_name' as a hashtag and retrive the new pictures from results to be added to Picture
	database.
	"""

	hashtag = "#" + album_name
	# 'tweets_result' list has the following contents: [media_url, favorite_count, user_screen_name, tweet_id]
	tweets_result = search(hashtag)

	# remove results that already exists in database
	pivots = ['tweet_id', 'src_url']
	print "Result tweets has %d results BEFORE duplicate removal." % len(tweets_result)
	for pivot in pivots:		
		if len(tweets_result) <= 0:
			print "No new tweets are found."
			break
		tweets_result = remove_duplicates(tweets_result, pivot)		
	print "Result tweets has %d results AFTER duplicate removal." % len(tweets_result)	
	
	# modify picture contents.
	# modifications are:
	# 	1. set new picture name to be stored
	#	2. extract image contents from url
	if len(tweets_result) > 0:
		new_pictures = []		
		for i in range(len(tweets_result)):	
			# set new img name to be stored
			src = tweets_result[i][0]
			new_img_name = generate_img_filename(src)			
			# extract img content and put to new file			
			new_img_file = get_img_content(src, new_img_name)
			new_pictures.append(new_img_file)

		# upload new_pictures list to s3 bucket		
		upload_to_bucket(new_pictures, album_name)
		print "New '%s' album images has been uploaded to S3 bucket." % album_name		
				
		# upload contents to database
		i = 0
		album = Album.objects.get(name=album_name) # get album object
		if album != None:
			for img in tweets_result:
				pic = Picture(album=album, url=new_pictures[i][0], src_url=img[0], like_count=img[1], owner=img[2], tweet_id=img[3])
				pic.save()
				print "%s saved to database." % img[0]
				i += 1
		# fire off signal
		abcd = Picture(album=album, url=new_pictures[0], like_count=img[1], owner=img[2], tweet_id=img[3])
		send_email.send(sender=Picture, instance=abcd)
	return

def generate_img_filename(img_url):
	"""
	Takes in an image file url and returns a new image name.
	"""

	random_number = randint(1,100000000) # append to end of 'img_string' to ensure unique img_name. chance of name collision is less than 1 in 100mil.
	
	temp_name = urlparse(img_url).path.split('/')[-1]
	extension = temp_name.split(".")[-1]
	img_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(random_number)
	new_img_name =  img_string + "." + extension
	return new_img_name

def get_img_content(img_url, new_name):
	"""
	Get image contents from image file url and return image contents in a list in the format:
	[new_img_name, File(temp_img), content_type]
	"""
	
	temp_img = NamedTemporaryFile(delete=True)
	pic = urllib2.urlopen(img_url)
	content_type = pic.info().type
	
	# read and write pic data into var
	temp_img.write(pic.read())
	temp_img.flush()
	file_content = [new_name, File(temp_img), content_type]
	return file_content

def upload_to_bucket(pic_info_list, album_name):
	"""
	Takes in a list of picture information and upload to s3 bucket.

	pic_info_list has a list structure of [[img_name, img_content, content_type]]
	"""

	bucket = get_s3_bucket()
	if bucket:
		for img in pic_info_list:
			# setup file upload keys
			new_key = Key(bucket)
			new_key.key = album_name + "/" + img[0]
			new_file = File(img[1])
			new_key.set_metadata('Content-Type', img[2])
			new_key.set_contents_from_file(new_file, rewind=True)			
			new_key.set_acl('public-read')	
