# std lib imports
# django imports
from django.contrib import admin
from django.contrib.auth.models import User

# third-party app imports
# app imports
from .models import Picture

# Picture admin interface

# Since Picture is list inline wrt to Album, no need to do admin.site.register() here.
class PictureInline(admin.TabularInline):
	model = Picture
	extra = 1
