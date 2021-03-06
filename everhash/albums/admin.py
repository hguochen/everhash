# std lib imports
# django imports
from django.contrib import admin
from django.contrib.auth.models import User

# third-party app imports
# app imports
from models import Album
from pictures.admin import PictureInline

# Everhash admin interface

class AlbumAdmin(admin.ModelAdmin):
	"""
	Admin field set displays.
	"""
	fieldsets = [
		('Album', {'fields':['name']}),
		('Date information', {'fields':['pub_date']}),
		('Posted by', {'fields':['user']}),
		('Default Picture', {'fields':['default_pic']}),
		('Milestone', {'fields':['milestone']}),
	]
	# pictures for an album are displayed inline instead of as a separate app by itself.
	inlines = [PictureInline]
	list_display = ('name', 'pub_date', 'user')
	list_filter = ['pub_date']
	search_fields = ['name', 'pub_date']

admin.site.register(Album, AlbumAdmin)
