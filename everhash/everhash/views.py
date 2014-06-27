# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# third-party app imports
from boto.s3.connection import S3Connection
# app imports
from settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_MEDIA_STORAGE_BUCKET
from tweets.signals import *
from tweets.views import search

def index(request):
	if request.method == "GET":
		from pictures.views import update_picture_database
		
		update_picture_database('apple')
		return render_to_response('index.html', context_instance=RequestContext(request))

def get_s3_bucket():
	"""
	Return a s3 bucket reference.
	"""	
	conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = conn.get_bucket(AWS_MEDIA_STORAGE_BUCKET)
	return bucket