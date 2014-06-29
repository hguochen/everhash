# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest

# third-party app imports
# app imports
from albums.models import Album

class AlbumTests(TestCase):
	"""
	This is the fixture: fixtures/albums.json in the following format
	[
		{
		    "pk": 20, 
		    "model": "albums.album", 
		    "fields": {
		        "default_pic": "", 
		        "milestone": 100, 
		        "pub_date": "2014-06-29T12:31:04Z", 
		        "user": 1, 
		        "name": "apple"
		    }
		},
		...
	]
	"""

	def test_get_album_names(self):
		"""Get album names."""
		obj = Album.objects.get_album_names()
		self.assertEquals(obj.name, 'apple')
	
	def test_update_milestone(self):
		"""Get object and update milestone field."""
		obj = Album.objects.get(pk=20)
		obj.milestone = 150
		obj.save()

		apple = Album.objects.get(pk=20)
		self.assertEquals(apple.milestone, 150)