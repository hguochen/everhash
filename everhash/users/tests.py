# std lib imports
# django imports
from django.test import TestCase
from django.utils import unittest
from django.contrib.auth.models import User
# third-party app imports
# app imports

# Create your tests here.

# Test guidelines:
# If model has custom methods, you should test that with unit tests.
# Same goes for custom views, forms, template tags, context processors, middleware, management commands, etc.
# If you implemented the business logic, you should test your aspects of the code.

class UserTestCase(TestCase):

	def setUp(self):
		User.objects.create(username='apple', email='apple@apple.com', password='apple')
		User.objects.create(username='12345', email='12345@12345.com', password='12345')
		User.objects.create(email='noname@email.com', password='noname')

	def test_user_created_1(self):
		apple = User.objects.get(username='apple')		
		
		self.assertEqual(apple.username, 'apple')
		self.assertEqual(apple.email, 'apple@apple.com')
		self.assertEqual(apple.password, 'apple')		

	def test_user_created_2(self):
		num = User.objects.get(username='12345')
		
		self.assertEqual(num.username, '12345')
		self.assertEqual(num.email, '12345@12345.com')
		self.assertEqual(num.password, '12345')

	def test_user_created_without_username(self):
		noname = User.objects.filter(email='noname@email.com')

		self.assertEqual(noname.email, AttributeError)
		self.assertEqual(noname.password, AttributeError)
