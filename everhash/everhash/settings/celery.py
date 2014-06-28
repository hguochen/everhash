from __future__ import absolute_import
# std lib imports
import os
# django imports
from django.conf import settings

# 3rd party lib imports

from celery import Celery

# app imports
 
# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'everhash.settings')
 
app = Celery('everhash')
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)