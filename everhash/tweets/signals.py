# std lib imports
import time

# django imports
from django.core.signals import request_finished
from django.dispatch import receiver, Signal

# third-party app imports

# app imports

fetch_tweet = Signal()

class Fetch_signal:
	def __init__(self):
		pass

	def countdown_fetch_tweets(self):		
		time.sleep(5)
		fetch_tweet.send(sender=self.__class__)
		