# std lib imports
# django imports
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone

# third-party app imports
# app imports


class AlbumManager(models.Manager):
	"""
	Album model manager class with proxy querysets
	"""
	def get_query_set(self):
		return AlbumQuerySet(self.model)

	# get albums by descending order of published date
	def desc_pub_date(self):
		return self.get_query_set().desc_pub_date()

	# get name of album
	#def get_name(self):
	#	return self.get_query_set().get_name(self.name)

	# get all albums posted by a user
	def get_user_posted_albums(self, user):
		return self.get_query_set().get_user_posted_albums(user)

	def get_album_names(self):
		return self.get_query_set().get_album_names()

	#def get_album(self, name):
	#	return self.get_query_set().get_album(name)

class Album(models.Model):
	"""
	Model fields for Album. Album model has a many to one relationship with User.

	ie. One user can have 0 or many albums.
	"""
	user = models.ForeignKey(User)
	name = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date published', default=timezone.now()) # saved at UTC timezone
	default_pic = models.CharField(max_length=600, blank=True, null=True) # collage pic for album	
	milestone = models.IntegerField(default=100)

	objects = AlbumManager()
	
	class Meta:
		app_label = 'albums'
		get_latest_by = 'pub_date'
		verbose_name= 'album'

	def __unicode__(self):
		return self.name

	user.short_description = 'Posted by'


class AlbumQuerySet(QuerySet):
	"""
	Album model predefined querysets:
	"""
	def desc_pub_date(self):
		return self.filter(pub_date__year=timezone.now().year).order_by('-pub_date')

	#def get_name(self, name):
	#	return self.get(name=name)

	def get_user_posted_albums(self, user):
		return self.filter(user=user).order_by('-pub_date')

	def get_album_names(self):
		return self.values('name')

	#def get(self, name):
	#	return self. get(name='name')