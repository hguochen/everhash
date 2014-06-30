# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.contrib.auth.models import User
# third-party app imports
# app imports
from albums.models import Album
from users.utils import get_user_albums_count, get_user_albums, get_user_picture_count

class UserTestCase(TestCase):
	fixtures = ['albums.json', 'users.json']

	def setUp(self):
		User.objects.create(username='apple', email='apple@apple.com', password='apple')
		User.objects.create(username='12345', email='12345@12345.com', password='12345')
		User.objects.create(email='noname@email.com', password='noname')

	def tearDown(self):
		pass

	def test_user_created_with_alphabets(self):
		"""Test lowercase alphabet user registration case"""
		apple = User.objects.get(username='apple')		
		
		self.assertEqual(apple.username, 'apple')
		self.assertEqual(apple.email, 'apple@apple.com')
		self.assertEqual(apple.password, 'apple')		

	def test_user_created_with_numbers(self):
		"""Test numbers user registration case"""
		num = User.objects.get(username='12345')
		
		self.assertEqual(num.username, '12345')
		self.assertEqual(num.email, '12345@12345.com')
		self.assertEqual(num.password, '12345')

	def test_user_created_without_username(self):
		"""Test user creation without username"""
		noname = User.objects.filter(email='noname@email.com')

		self.assertEqual(noname.email, AttributeError)
		self.assertEqual(noname.password, AttributeError)


class UserProfileTestCase(TestCase):
	fixtures = ['albums.json', 'users.json']

	def setUp(self):
		self.user = User.objects.get(username='hguochen')

	def tearDown(self):
		pass

	def test_get_user_albums(self):
		"""Test get_user_albums function to return all albums owned by a user"""		
		albums = get_user_albums(self.user)
		album_names = []
		for album in albums:
			album_names.append(album.name)
		self.assertEqual('apple' in album_names,True)
		self.assertEqual('pear' in album_names,True)
		self.assertEqual('carnival' in album_names,True)

	def test_get_user_albums_count(self):
		"""Test get_user_album_count to return correct album count by a user"""
		album_count = get_user_albums_count(self.user)
		
		self.assertEqual(album_count, 4)

	def test_get_user_picture_count(self):
		"""Test get_user_picture_count to return correct album count by a user"""
		album = Album.objects.get(name='apple')
		print album
