# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client

# third-party app imports
# app imports


class AlbumViewTests(TestCase):
	fixtures = ['albums.json', 'users.json']
	"""
	Testing views for albums app.
	"""
	def setUp(self):
		client = Client()

	def tearDown(self):
		pass

	def test_album_page_working(self):
		"""Test album page working"""
		response = self.client.get(reverse('view_album', kwargs={'album_name':'apple'}))
		self.assertEquals(response.status_code, 200)

	def test_album_404_page_working(self):
		"""Test invalid album get request"""
		response = self.client.get('/album/ffdsa/')
		self.assertEquals(response.status_code, 404)