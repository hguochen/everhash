# std lib imports
from datetime import datetime

# django imports
# 3rd party lib imports
from django_cron import CronJobBase, Schedule
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from celery.task import task

# app imports
from pictures.views import update_picture_database
from albums.models import Album
from tweets.utils import scrapers

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="0", minute="1", day_of_week="*")))
def scraper_example():
	logger.info("Start task")
	now = datetime.now()
	result = scrapers.scraper_example(now.day, now.minute)
	logger.info("Task finished: result = %i" % result)

@periodic_task(run_every=(crontab(hour="0", minute="20", day_of_week="*")))
def update_picture_database_automater():
	"""
	Update picture database for every album present in database
	"""
	album_names = Album.objects.get_album_names()
	for album in album_names:
		for name, hashtag in album:
			update_picture_database(hashtag)

"""
def update_albums():
	# get all album names
	album_names = Album.objects.get_album_names()
	update_picture_database()
"""

"""
class Fetch_tweet_job(CronJobBase):
	RUN_EVERY_MINS = 1

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'everhash.Fetch_tweet_job'

	def do(self):
		send_mail('cron_test', 'body is here.', 'everhash@gmail.com', ['hguochen@gmail.com'], fail_silently=False)

"""