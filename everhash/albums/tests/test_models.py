# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.contrib.auth.models import User

# third-party app imports
# app imports
from .models import Album


class AlbumModelTests(TestCase):
	fixtures = ['albums.json', 'users.json']
	"""
	This is the fixture: fixtures/albums.json in the following format
	[
		{
		    "pk": 1, 
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
	
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_user_fields(self):
		"""Get album names."""
		user = User.objects.get(pk=1)
		#obj = Album.objects.get_user_posted_albums(user)
		self.assertEquals(user.username, 'hguochen')
		self.assertEquals(user.email, 'hguochen@gmail.com')
		self.assertTrue(user.is_superuser, True)

	def test_get_album_names(self):
		"""Get all album names"""
		albums = Album.objects.get_album_names()		
		album_name = []
		for album in albums:
			album_name.append(album['name'])
		self.assertEquals(album_name[0], 'apple')
		self.assertEquals(album_name[1], 'carnival')
		self.assertEquals(album_name[2], 'dogs')
		self.assertEquals(album_name[3], 'pear')

	def test_get_user_posted_album_names(self):
		"""Get album names."""
		user = User.objects.get(username='hguochen')
		albums = Album.objects.get_user_posted_albums(user)
		album_name = []
		for album in albums:
			album_name.append(album.name)
		self.assertEquals(album_name[0], 'apple')
		self.assertEquals(album_name[1], 'carnival')
		self.assertEquals(album_name[2], 'dogs')
		self.assertEquals(album_name[3], 'pear')

	def test_most_recent_pub_date(self):
		"""Get most recent pub date"""
		dates = Album.objects.desc_pub_date()
		test_dates = []
		for date in dates:
			test_dates.append(str(date.pub_date))
		print test_dates
		self.assertEquals(test_dates[0], '2014-06-30 05:19:33+00:00')
