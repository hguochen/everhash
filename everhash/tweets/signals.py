# std lib imports
import time

# django imports
from django.core.signals import request_finished
from django.dispatch import receiver, Signal

# third-party app imports

# app imports
#from pictures.views import update_picture_database
from albums.models import Album
from pictures.models import Picture
from pictures.views import update_picture_database

fetch_tweet = Signal()

@receiver(fetch_tweet)
def fetch_tweet_handler(sender, **kwargs):	
	print "AHA"
	print "ADASd"
	time.sleep(5)
	# get all album names
	album_names = Album.objects.get_album_names()
	for album in album_names:
		for key,hashtag in album.items():
			print key
			print hashtag
			update_picture_database(hashtag)
	