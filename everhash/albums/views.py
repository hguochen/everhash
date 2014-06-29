# std lib imports
# django imports
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext

# third-party app imports
# app imports
from models import Album
from pictures.views import Picture
from everhash.settings.base import S3_URL

def add_album(new_album):
	# get existing database albums
	album_names = Album.objects.get_album_names()
	new_album = new_album.lower()

	# check is album exists
	if new_album in album_names:
		return
	else:
		# save new album
		user = User.objects.get(username='hguochen')		
		album = Album(user=user, name=new_album)
		album.save()

def view_album(request, album_name=None):
	album_name = album_name.lower()
	album = get_object_or_404(Album, name=album_name)
	
	if album != None:
		pictures = Picture.objects.album_pictures(album)
		pictureset = []
		urls = []
		for pic in pictures:			
			url = S3_URL + pic.album.name + "/" +pic.url
			urls.append(url)
			pictureset.append([pic, url])
		context_instance = RequestContext(request, 
										{'album':album_name, 'pictureset':pictureset, 'urls':urls})
	return render_to_response('album.html', context_instance)