# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User

# third-party app imports
# app imports
from .views import index

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

	def test_index_page_header(self):
		"""Test index page renders correct header"""
		response = self.client.get('/')
		self.assertTrue('Everhash', response.content)	

	def test_index_page_caption(self):
		"""Test index page renders correct caption"""
		response = self.client.get('/')
		self.assertTrue('Twitter hashtag images collected.', response.content)
		
	def test_login_page_working(self):
		"""Test login page working."""
		response = self.client.get('/accounts/login/')
		self.assertEquals(response.status_code, 200)

	def test_login_page_functional(self):
		"""Test user able to login and redirects """
		response = self.client.post('/accounts/login/', {'username':'hguochen', 'password':'1234'})
		self.assertEquals(response.status_code, 200)

	def test_register_page_working(self):
		"""Test register page working and redirects to login success page."""
		response = self.client.post('/accounts/register', {'username':'test1', 'email':'test1@email.com', 'password1':'test1', 'password2':'test1'})
		self.assertEquals(response.status_code, 301)

	def test_404_error_page_working(self):
		"""Test 404 page working"""
		response = self.client.get('/234234fasds')
		self.assertEquals(response.status_code, 404)

	def test_accounts_page_functional(self):
		"""Test user able to access account page with redirection"""
		self.client.post('/accounts/login/', {'username':'hguochen', 'password':'1234'})
		response = self.client.get('/accounts/profile')
		self.assertEquals(response.status_code, 301)

	def test_access_profile_page_without_login(self):
		"""Test accessing profile page without login. Receives redirection"""
		response = self.client.get('/accounts/profile/', follow=True)
		self.assertEquals(response.redirect_chain, [('http://testserver/accounts/login/?next=/accounts/profile/', 302)])

	def test_album_page_working(self):
		"""Test album page working."""
		response = self.client.get('/album/apple/')
		self.assertEquals(response.status_code, 200)