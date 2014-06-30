# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.contrib.auth.models import User

# third-party app imports
# app imports
from pictures.models import Picture

class PictureModelTests(TestCase):
	"""
	Test cases for picture models.
	"""
	fixtures = ['pictures.json', 'albums.json', 'users.json']

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_get_album_pictures(self):
		"""Test get all album pictures of a given hashtag"""
		pictures = Picture.objects.album_pictures('carnival')
		items = []
		for picture in pictures:
			items.append(picture.url)
		
		self.assertEquals(u'20140630132818-57491019.jpg' in items, True)
		self.assertEquals(u'20140630132817-78466345.jpg' in items, True)

	def test_get_tweet_ids(self):
		"""Test get all tweet ids."""
		pictures = Picture.objects.get_tweet_ids()
		items = []
		for picture in pictures:
			items.append(picture['tweet_id'])
		
		# random tweet id selected
		self.assertEquals(483482578281058304 in items, True)

	def test_get_all_src_url(self):
	 	"""Test get all src urls"""
	 	pictures = Picture.objects.all_src_url()
	 	items = []
	 	for picture in pictures:
	 		items.append(picture['src_url'])
	 	#random src url selected
	 	self.assertEquals('http://pbs.twimg.com/media/BrWsrJZIYAAeoFN.jpg' in items, True)

	def test_get_all_values(self):
		"""Test get all values of a given field name"""
		pictures = Picture.objects.get_all_values('owner')
	 	items = []
	 	for picture in pictures:
	 		items.append(picture['owner'])
	 	# random owner name selected
	 	self.assertEquals('LUZKINGKING' in items, True)

	def test_get_most_popular(self):
		"""Test the get most popular picture of a hashtag"""
		picture = Picture.objects.get_most_popular('apple')
		self.assertEquals(picture.url , '20140630133233-45000935.jpg')
