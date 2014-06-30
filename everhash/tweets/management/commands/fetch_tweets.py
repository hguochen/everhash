# std lib imports
import datetime

# django imports
from django.core.management.base import NoArgsCommand, CommandError

# 3rd party imports
# app imports
from albums.models import Album
from pictures.views import update_picture_database

# Custom manage.py command set
# The custom command ./manage.py fetch_tweets pulls results from all twitter hashtag albums
# and updates the picture database with new uploads.
# fetch_tweets custom commands runs on linux cron job every 20minutes.
# cron job has the following setup: 
# */20 * * * * /filepath/to/env && ./manage.py fetch_tweets
class Command(NoArgsCommand):
	
	help = "Fetches all hashtag tweets avilable in database when command is executed."

	def handle_noargs(self, **options):
		"""
		Tasks to execute when command is given.
		"""
		album_names = Album.objects.get_album_names()
		for album in album_names:
			for key,hashtag in album.items():				
				print hashtag
				update_picture_database(hashtag)

		self.stdout.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ' Successfully fetched all hashtag tweets.')

