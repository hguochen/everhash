# std lib imports
# django imports
from django.shortcuts import render_to_response

# third-party app imports
from twython import Twython

# app imports
from everhash.settings.base import TWITTER_APP_KEY, TWITTER_ACCESS_TOKEN


def authenticate():
	"""
	Authenticate the application with OAuth 2 authentication.

	Returns a Twython instance which allows Twitter REST API calls
	"""
	return Twython(TWITTER_APP_KEY, access_token=TWITTER_ACCESS_TOKEN)

def search(query_term, count=100, until=None):
	"""
	Perform a twitter REST API search with a compulsory parameter, 'query_term'.

	Example query terms:
		@everhash: username being everhash.
		#everhash: hashtag being everhash.
		everhash: text value being everhash.

	Optional search parameters:
		count: The number of tweets to return per page, up to a maximum of 100. Defaults to 15. 
		until: Returns tweets generated before the given date. Date should be formatted as YYYY-MM-DD. Keep in mind that the 
			   search index may not go back as far as the date you specify here.
	
	Returns a list of list with the following parameters within list - [media_url, favorite_count, screen_name, tweet_id]
	"""
	# return a twitter instance
	twitter = authenticate()

	# retrieve a JSON list of tweets
	search_results = twitter.search(q=query_term, count=count, until=until)	
	tweets = search_results['statuses']
	result = []
	for tweet in tweets:	
		for item in tweet['entities'].get('media', []):
			try:				
				result.append([item['media_url'], tweet['favorite_count'], tweet['user']['screen_name'], tweet['id']])
			except IndexError, KeyError:
				continue
	return result
	
	