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

def index(request):
	if request.method == "GET":		
		#update_picture_database('carnival')
		
		thumbnail = {}		
		albums = Album.objects.values('name')
		
		# generate thumbnail pic from each of the albums. if album is empty, no pic urls are stored.
		for album in albums:
			try:
				popular_img_url = Picture.objects.get_most_popular(album['name'])
				thumbnail[album['name']] = S3_URL + album['name'] + "/" + popular_img_url.url
			except IndexError:
				thumbnail[album['name']] = 'NONE'
		print thumbnail
		context_instance=RequestContext(request,
										{'albums':albums, 'thumb_nail':thumbnail})
		return render_to_response('index.html', context_instance)
