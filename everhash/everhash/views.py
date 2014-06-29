# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# third-party app imports
# app imports
from tweets.signals import *
from albums.models import Album

def index(request):
	if request.method == "GET":		
		update_picture_database('carnival')

		albums = Album.objects.values('name')
		for album in albums:
			print album
		context_instance=RequestContext(request,
										{'albums':albums})
		return render_to_response('index.html', context_instance)
