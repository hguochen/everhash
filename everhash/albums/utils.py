# std lib imports
# django imports
# 3rd party app imports
# app imports
from pictures.models import Picture
from everhash.settings.base import S3_URL

def generate_album_thumbnail(album_objects):
	"""
	Generates a dictionary of album thumbnails from a list of album_objects.
	Returns the dictinoary of thumbnails.
	"""	
	thumbnail = {}
	for album in album_objects:
		try:
			popular_img_url = Picture.objects.get_most_popular(album['name'])
			thumbnail[album['name']] = S3_URL + album['name'] + "/" + popular_img_url.url

		except IndexError:
			thumbnail[album['name']] = None
	return thumbnail