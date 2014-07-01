# std lib imports
import filecmp
import hashlib
import urllib2

# django imports
# 3rd party lib imports
from boto.s3.key import Key
from boto.s3.connection import S3Connection

# app imports
from albums.models import Album
from tweets.views import search
from models import Picture
from everhash.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_MEDIA_STORAGE_BUCKET

# Utility library for to facilitate pictures app


def get_s3_bucket():
	"""
	Return a s3 bucket reference.
	"""	
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(AWS_MEDIA_STORAGE_BUCKET)
	return bucket

def remove_duplicates(latest_tweets, pivot):
	"""
	Compare database_sets and latest_tweets, remove duplicates from 'latest_tweets' list if there's a tweet id match
	remove duplicates between tweet result and existing database result
	perform duplicate removals by comparing pivots:
		1. tweet_id
		2. src_url
	
	"""
	
	db_fields = Picture.objects.get_all_values(pivot)
	#db_src_urls = Picture.objects.get_src_url()  ENABLE AFTER DATABASE RESET AND POPULATED
	
	# extract pivot from database and latest_tweets
	pivot_field = []
	database_field = []
	for tweet in latest_tweets:
		if pivot == "tweet_id":
			pivot_field.append(tweet[3]) # extract tweet_ids
		elif pivot == "src_url":
			pivot_field.append(tweet[0]) # extract media_urls
	for row in db_fields:
		for name,field in row.items():
			database_field.append(field)

	# compare field from database and "latest_reweet" and put only output "latest_tweet" items if its not a duplicate
	retained_tweets = []
	for i in range(len(pivot_field)):
		if pivot_field[i] not in database_field:
			retained_tweets.append(latest_tweets[i])
	# remove file content duplicates
	retained_tweets = remove_duplicate_file(retained_tweets)
	return retained_tweets

def remove_duplicate_file(latest_tweets):
	"""
	Given a tweet list, remove tweets from which its images are duplicates to each other.
	Return a list of unique file contents from each other.

	This function should be used to distinguish images which have different urls but the same file contents.
	"""
	
	result = []
	hashed_url = []
	for i in range(len(latest_tweets)):
		hash_img = hashlib.md5(urllib2.urlopen(latest_tweets[i][0]).read()).hexdigest()
		hashed_url.append(hash_img)
	for i in range(1, len(latest_tweets)):
		if hashed_url[i-1] not in hashed_url[i:]:
			result.append(latest_tweets[i-1])
	return result	