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

logger = get_task_logger(__name__)

# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="0", minute="1", day_of_week="*")))
def scraper():
	logger.info("Start task")
	now = datetime.now()
	result = scrapers.scraper(now.day, now.minute)
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