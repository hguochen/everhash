# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User

# third-party app imports
# app imports
from views import index

class EverhashViewTests(TestCase):
	"""
	Testing views for everhash app.
	"""

	def setUp(self):
		client = Client()
		new_user = User(username='hguochen', email='hguochen@email.com', password='1234')
		new_user.save()

	def tearDown(self):
		pass

	def test_get_index_page(self):
		"""Test index page view working"""
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)

	def test_login_page_working(self):
		"""Test login page working."""
		response = self.client.get('/accounts/login/')
		self.assertEquals(response.status_code, 200)

	def test_register_page_working(self):
		response = self.client.get('/accounts/register')
		self.assertEquals(response.status_code, 200)

	def test_404_error_page_working(self):
		"""Test 404 page working"""
		response = self.client.get('/234234fasds')
		self.assertEquals(response.status_code, 404)

	def test_login_page_functional(self):
		"""Test user able to login"""
		response = self.client.post('/accounts/login/', {'username':'hguochen', 'password':'1234'})
		self.assertEquals(response.status_code, 200)