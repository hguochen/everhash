# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

# third-party app imports
# app imports
from models import Album


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