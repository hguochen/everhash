# std lib imports
# django imports
from django.db import models

# 3rd party imports
# app imports
from albums.views import Albums


class AlbumManager(models.Manager):
	"""
	Image model manager class with proxy querysets.
	"""

	def get_query_set(self):
		return ImageQuerySet(self.model)

	def get_images(self):
		self.get_query_set().get_images()


class Image(model.Model):
	"""
	Images fields for Album. Image model has a many to one relationship with Album.
	"""

	album = models.ForeignKey(Album)
	image = models.ImageField()

	class Meta:
		app_label ='images'		
		verbose_name= 'images'

	def __unicode__(self):
		return self.album

class ImageQuerySet(QuerySet):
	"""
	Image model predefined querysets.
	"""

	def get_images(self):
		return self.values_list('image').filter(entity=self)
