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
from pictures.signals import pic_save
from everhash.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_MEDIA_STORAGE_BUCKET

def update_picture_database(album_name):
	"""
	Updates the picture database that has field name 'album_name'.

	Performs a twitter REST API search with 'album_name' as a hashtag and retrive the new pictures from results to be added to Picture
	database.
	"""

	# get results of a tweet search
	hashtag = "#" + album_name # setup hashtag

	# compare tweet ids and remove duplicates
	tweets_result = search(hashtag)
	db_tweet_ids = Picture.objects.get_tweet_ids()
	print len(tweets_result)
	tweets_result = remove_duplicates(db_tweet_ids, tweets_result)
	print len(tweets_result)
	if len(tweets_result) > 0:
		# get picture object from list of tweet_results
		new_pictures = []		
		for i in range(len(tweets_result)):	
			# set new img name to be stored
			temp_img_name = urlparse(tweets_result[i][0]).path.split('/')[-1]
			extension = temp_img_name.split(".")[-1]		
			random_number = randint(1,1000000) # ensure unique img_name
			img_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "-" + str(random_number)
			new_img_name =  img_string + "." + extension
			
			# extract img content
			temp_img = NamedTemporaryFile(delete=True)
			pic = urllib2.urlopen(tweets_result[i][0])
			content_type = pic.info().type
			temp_img.write(pic.read())
			temp_img.flush()
			new_pictures.append([new_img_name, File(temp_img), content_type])
		
		# upload new_pictures list to s3 bucket		
		upload_to_bucket(new_pictures, album_name)
		print "New '%s' album images has been uploaded." % album_name
		# upload contents to database
		i = 0
		album = Album.objects.get(name=album_name) # get album object
		if album != None:
			for img in tweets_result:
				pic = Picture(album=album, url=new_pictures[i][0], like_count=img[1], owner=img[2], tweet_id=img[3])
				pic.save()
				i += 1
		abcd = Picture(album=album, url=new_pictures[0], like_count=img[1], owner=img[2], tweet_id=img[3])
			
		# fire off signal 
		pic_save.send(sender=Picture, instance=abcd)


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
	
def remove_duplicates(database_tweet_ids, latest_tweets):
	"""
	Compare database_tweet_ids and latest_tweets, remove duplicates from 'latest_tweets' list if there's a tweet id match
	"""
	latest_tweet_ids = []
	for i in range(len(latest_tweets)):
		latest_tweet_ids.append(latest_tweets[i][3])
	data_tweed_ids = []
	for row in database_tweet_ids:
		for field, tweet_id in row.items():
			data_tweed_ids.append(tweet_id)
	final_tweets = []
	for i in range(len(latest_tweet_ids)):
		if latest_tweet_ids[i] not in data_tweed_ids:
			final_tweets.append(latest_tweets[i])
	return final_tweets

def get_s3_bucket():
	"""
	Return a s3 bucket reference.
	"""	
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(AWS_MEDIA_STORAGE_BUCKET)
	return bucket
