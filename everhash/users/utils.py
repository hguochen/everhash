# std lib imports
# django imports
# 3rd party app imports
# app imports
from albums.models import Album
from pictures.models import Picture

# List of utility functions to facilitate a thin view layer

def dictionary_store(album_objects):
	"""
	Takes in a list of album_objects and return a list of album_names in which each element is a dictionary.
	"""
	temp = {}
	album_names = []
	for i in range(len(album_objects)):
		temp['name'] = album_objects[i].name # key= 'name', value = albums[i].name
		album_names.append(temp)
		temp = remove_key(temp, 'name')
	return album_names

def get_user_albums_count(user_object):
	"""
	Takes in a user object and return the total number of albums that the user has.
	"""

	return Album.objects.get_user_albums_count(user_object)

def get_user_picture_count(user_object):
	"""
	Takes in a user object and return the total number of pictures that the user has.
	"""

	# get all albums of user
	albums = get_user_albums(user_object)
	# for each album, get the picture count of the album and add to total
	picture_count = 0
	for album in albums:
		album_pics = Picture.objects.get_picture_count_by_album(album)
		picture_count += album_pics
	return picture_count

def get_user_albums(user_object):
	"""
	Takes in a user object and return all the albums that the user has.
	"""

	return Album.objects.get_user_posted_albums(user_object)
	
def remove_key(dictionary, key):
	"""
	Removes an element from a dictionary
	"""
	
	item = dict(dictionary)
	del item[key]
	return item