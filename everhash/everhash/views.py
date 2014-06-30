# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# third-party app imports
# app imports
from tweets.signals import *
from albums.models import Album
from pictures.models import Picture
from everhash.settings.base import S3_URL
from albums.utils import generate_album_thumbnail

def index(request):
	if request.method == "GET":		
		albums = Album.objects.values('name')
		
		# generate thumbnail pic from each of the albums. if album is empty, no pic urls are stored.
		thumbnail = generate_album_thumbnail(albums)

		context_instance=RequestContext(request,
										{'albums':albums, 'thumb_nail':thumbnail})
		return render_to_response('index.html', context_instance)
