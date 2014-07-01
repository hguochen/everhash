# std lib imports
# django imports
from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Max

# third-party app imports
# app imports
from albums.models import Album


class PictureManager(models.Manager):
	"""
	Picture model manager class with proxy querysets.
	"""

	def get_query_set(self):
		return PictureQuerySet(self.model)

	# get pictures of given album and organize by decreasing like count
	def album_pictures(self, album_name):
		return self.get_query_set().album_pictures(album_name)

	# get tweet id values
	def get_tweet_ids(self):
		return self.get_query_set().get_tweet_ids()

	# get all src urls from database
	def all_src_url(self):
		return self.get_query_set().all_src_url()

	# get all values of a given field
	def get_all_values(self, field):
		return self.get_query_set().get_all_values(field)

	# get the most popular photo of the album
	def get_most_popular(self, album_name):
		return self.get_query_set().get_most_popular(album_name)

	# get picture count by album
	def get_picture_count_by_album(self, album_object):
		return self.get_query_set().get_picture_count_by_album(album_object)

class Picture(models.Model):
	"""
	Model fields for Picture. Picture model has a many to one relationship with Album.

	ie. One album can have 0 or many pictures.
	"""
	
	album = models.ForeignKey(Album)
	url = models.CharField(max_length=600, null=True, blank=True) # stores the url where the picture is stored	
	pub_date = models.DateTimeField('date_published', default=timezone.now()) # saved at UTC timezone
	like_count = models.IntegerField(default=0)
	owner = models.CharField(max_length=600, null=True, blank=True) # name of the original picture owner
	tweet_id = models.BigIntegerField(default=0)
	src_url = models.CharField(max_length=600, null=True, blank=True) # store source url location

	objects = PictureManager()

	class Meta:
		verbose_name= u'picture'

	def __unicode__(self):
		return self.url


class PictureQuerySet(QuerySet):
	"""
	Picture model predefined querysets
	"""

	def album_pictures(self, album_name):
		album = Album.objects.get(name=album_name)
		return self.filter(album=album).order_by('-like_count')

	def get_tweet_ids(self):
		return self.values('tweet_id')

	def all_src_url(self):
		return self.values('src_url')

	def get_all_values(self, field):
		return self.values(field)

	def get_most_popular(self, album_name):
		return self.filter(album__name=album_name).order_by('-like_count')[0]

	def get_picture_count_by_album(self, album_object):
		return self.filter(album=album_object).count()