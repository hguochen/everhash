========================
Project_everhash
========================
Everhash is a web application that crawls the twitter-universe by specific hashtags, retrieves and stores media contents. In the current version 1.0, only images with extension, jpg, png, diff, gif are stored. Future versions are expected to store audio/video contents with support for typical media extensions such as mp4, avi etc.

A Django 1.6.5(python 2.7.5) project. This is part of an assignment done with [Eversnap](http://www.geteversnap.com/).

The project is currently deployed and hosted live on Amazon EC2 Ubuntu(14.10) - Trusty Tahr at [http://ec2-54-179-136-56.ap-southeast-1.compute.amazonaws.com/](http://ec2-54-179-136-56.ap-southeast-1.compute.amazonaws.com/). Amazon S3 storage is also used to host media related contents,

Project assumptions
===========
1. Definition of a 'smart' automatic album is that the album should populate itself with contents with little or no user interference.
2. 20 minutes featching time interval is not the optimal fetching solution from twitter. Twitter has a fetching window of 15minutes in which each windows allows 15 requests. The given fetching time is to allow demonstration of the ability to consume public APIs.
3. 'User' in our case refers to the owner of the album who started the album itself and not visitors who browses the site and view albums.
4. Storing BLOB data in databases such as MySQL is a bad practice in general and should not be used. In view of optimizations, everhash decides to store BLOB data in cloud storages such as S3 and save a reference to these storages.
5. Sending email notifications is seen as a proof of concept to utilize cron jobs and django signals in the development of applications. At a greater picture, to demonstrate ability to schedule work tasks with little or no developer intervention in production environments.
6. Duplicate photos would mean the same photo rendered without any form of altering or any application of filters. A picture sent by two different individuals using different filters are seen as two entirely different photos.
7. Accessing REST API to retrieve photos means with some knowledge of the photo, such as its url, we are able to retrieve the actual photo contents.
8. The test to show data structure through REST API is demonstrated through accessing an album page itself. ie. If an album has the name 'apple', the way to retrieve the apple album through everhash is with the URL http://HOST/album/apple.
9. Automated testing are in place to demonstrate the ability to operate in a test driven development setup.

To use this project follow these steps:

#. Create your working environment
#. Install Django
#. Create the new project by templating th django-two-scoops template
#. Install dependencies
#. Use Django admin to create the project

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

Working Environment
===================
Eversnap is built with the Linux(MacOS), Apache server for deployment, MySQL database with innoDB and Python programming language. A LAMP stack in short.

[Virtualenv](https://pypi.python.org/pypi/virtualenv) is used to separate the dependencies between the operating environment and application's environment.
Version control 
[Git](http://git-scm.com/) is used to mark development milestones.



Virtualenv Only
---------------

Make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv ENV

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Once virtualenv is setup, navigate to file root level and execute the following command to move into virtual environment to install dependencies.

	$ source ENV/bin/activate


Installing Django
=================

To install Django in the new virtual environment, run the following command::

    $ pip install django

Everhash runs optimally on Django 1.6.5. You may want to use the same version to avoid django related issues. Trunk version is untested yet.

Dependencies
=================
Everhash project is built on the following dependencies and versions. They are categorized into their respective development environments. Note that some dependencies are used across multiple/all environments. These dependencies are categorized in the base.py section.

base.py
	
	Django==1.6.5 
	South==0.8.4
	django-registration==1.0
	MySQL-python==1.2.5
	PIL==1.1.7
	requests-oauthlib==0.4.0
	twython==3.1.2

local.py

	django-debug-toolbar==1.2.1
	Sphinx==1.2.2

production.py
	
	wsgiref==0.1.2
	gunicorn==18.0

test.py

	coverage==3.7.1

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*Many PaaS expect a requirements.txt file in the root of projects.*

Project Template
======================
Everhash adopts two scoops django project template structure. You can check out the awesome two scoops template [here](https://github.com/twoscoops/django-twoscoops-project).

Everhash application is essentially the sum of 4 app implementations, mainly

* users - to handle authentication
* pictures - to handle all picture objects and related functions/methods
* albums - to handle all album objects and related functions/methods
* tweets - to handle all interactions with twitter APIs
* collage - to handle all image manipulation techniques.

App structure
======================
Everhash application has the following app structure:

	project_everhash/
		.gitignore
		README.rst
		requirements.txt
		docs/
		ENV/		
		requirements/
		everhash/
			albums/
			collages/
			everhash/
			pictures/
			static/
			templates/
			tweets/
			users/
			.coverage
			manage.py
			
Under the second level, everhash/ folder contains all the applications and folders needed to run everhash application. Specifically, 5 apps are developed alongside and facilitates the main application.

App specifications
==================
everhash
--------
Main app of the project. Multiple setting files are housed under the settings sub-folder to cater to different operating environments. 
	
	everhash/
	
		settings/
			
			base.py
			
			local.py
			
			passwd.py *
			
			production.py
			
			test.py
			
passwd.py keeps sensitive informations such as secret keys and are kept out of the version control for obvious reasons.

urls in this folder forms the base urls for the project. urls.py has the following definitions:

	url(r'^$', 'views.index', name='index'),

	url(r'^admin/', include(admin.site.urls)),

	url(r'^album/', include('albums.urls')),

	url(r'^accounts/', include('users.urls')),
			
Extensions after album or accounts urls goes to its corresponding sub-urls housed in its respective app. Only index view is defined in the views layer. This lightweight approach in the main app can be viewed as a funnel in which other apps provide contents through the funnel. It is generally good to have thin view layers and fat models, and utility functions.

albums
------

albums app stores album models and its related views on displaying the albums. It's models have the following fields:
	
	id - Primary key of the model
	
	user - ForeignKey for django auth user model
	
	name - name of the album in CharField.
	
	pub_date - date at which the album is created.
	
	default_pic - collage pic for the album.
	
	milestone - the subsequent pictures count for the album. (arbitrary field)
	
The model class `Album`, is supplemented with a proxy queryset class `AlbumManager` to provide custom querysets. `AlbumManager` class is a proxy for the `AlbumQuerySet` class which provides the actual querysets.

urls.py is an app level url specification which has the following urls definitions:

	url(r'^add/$', 'albums.views.add_album', name='add_album'),
	
    url(r'^add/(?P<hashtag>\w+)/$', 'albums.views.add_confirm', name='add_confirm'),
    
    url(r'^(?P<album_name>\w+)/$', 'albums.views.view_album', name='view_album'),
    
Each of the urls are supported by its corresponding views, which forms the 3 main functions in views layer.
	
	def add_album(request):
	"""
	Add a new album by POST-ing a hashtag.
	"""
	...
	
	def add_confirm(request, hashtag=None):
	"""
	Confirmation view for adding a new album.
	"""
	...
	
	def view_album(request, album_name=None):
	"""
	Takes in an album name parameter and display the album page. Return a 404 page 	if album does not exist.
	"""	
	...
	
Template layer are housed in-app under templates/ directory with the following HTML files.

	base_album.html
	
	album.html
	
	add_album.html
	
	add_album_confirmation.html

Forms layer houses 1 form, `AlbumForm` which allows users to add albums into their respective account.

Admin uses django admin system which displays all of its attribute fields and inline pictre objects associated with the album.

collages
--------
Collages app takes in a series of pictures and generates a collage with a custom built library housed in views layer. Collage app needs the actual image file contents to be accessible in order to generate a combined collage. Thus, the models layer does the unconventional thing that actually has a ImageField field which stores BLOB data in the database. 

To prevent unnecessary bloating of database, once collages are generated, the images are removed from the database. Since picture urls are already stored in the pictures model. Image contents can be retrieved and processed on demand. 

Views layer houses the following main functions that builds the actuall collage:

	def img_read(text_line):
	"""
	Read the image information from file and return the collage information as a list of image lists.
	"""
	
	def img_copy(info, bkg) :
	"""
	Inserts the image described by imagelist into the bkg image using the parameters in the image list.
	"""
	
	def collage_read_file(file_name):
	"""
	Reads collage information from a text file and returns the collage information as a list of image lists.
	"""
	
	def collage_read_image(collage_set):
	"""
	Reads the picture data using the filenames stored in the collage(list of image lists) and stores the picture data in the 
	last element of each of the image lists.
	"""
	
	def collage_build(collage):
	"""
	Creates a blank background image and places each image in the collage background.
	Returns a background image.
	"""
	
	def collage_rebuild(collage, bkg):
	"""
	Rebuilds the collage given an existing collage and background.
	"""

The collage app functions like a utility module that manipulates images and send the outcome to S3 storage and its relevant url to albums storage.

pictures
------
pictures app stores pictures object and its associated functions and methods. models layer in the app has the following fields:

	id - primary key of the model
	
	album - ForeignKey field to albums object
	
	url - url location of the picture, which is stored in s3.
	
	pub_date - date to which the picture is saved.
	
	like_count - the number of favorites associated with the picture in twitter. note that if multiple pictures are in the same tweet, they share the same number of likes.
	
	owner - twitter user who posted the original tweet picture.
	
	tweet_id - id of the tweet from which the picture comes from.
	
	src_url - source url form which the picture is from.
	
The model class `Picture`, is supplemented with a proxy queryset class `PictureManager` to provide custom querysets. `PictureManager` class is a proxy for the `PictureQuerySet` class which provides the actual querysets.

picture app has a img_compares module which does image comparisons between 2 file images and checks for percentage similarity between the 2 images. Purpose of this image compare module is to remove image duplicates from a set of tweet images. 

Image comparison is based on a version of root mean square value comparison. In this case, we give each set of RGB values an index and organizes the set of indexes of an image by histogram. We then compare the histogram results. Returned result of close to 0 would indicate the 2 images are most likely the same. However, for some versions of picture effects, results may vary.

pictures app registers a send_email django signal which fires off once an album has reached its successive 100 pictures until the albm has reached 500 picture count. The signal is emitted after every new save to the database and check for album counts. In turn, picture saves are routinely performed with django custom commands and linux cron jobs.

Views layer in pictures app serves 1 main function, update_picture_database which periodically updates the database with new pictures of each album. 

this is achieved by a cron job which is run every 20minutes. the cron job looks like the following:

	*/20 * * * * cd /path/to/project/level/dir && source ENV/bin/activate && ./manage.py fetch_tweets

tweets
-----
Tweets app handles the interaction between twitter and everhash. Mainly the fetching of hashtag tweets. tweets app pulls JSON data from twitter through its REST API v1.1 at every 20 minutes interval. Since twitter REST API v1.1. Rate limiting window has decreased to 15minute intervals and you are allowed to make at most 15 requests during each window. This figure puts everhash well below its optimal request rate and ensures each request is bound for success. 

Management command folder has a fetch_tweets.py file which indicates the custom ./manage.py fetch_tweets command. 

The views layer contains 1 main method search() to search for a given hashtag using REST API and appends the relevant result to a list to be processed.

users
-----
Everhash is exploring to become a Saas application to provide users with timely collated twitter media contents. Therefore authentication is implemented to test drive this concept's popularity.

Users app sub classes the django authentication module and implements custom authentication, model fields, formsets, views to suit the application's needs.

User can perform the following functions with the application:

	-registration()
	
	- login()
	
	- logout()
	
	- password_change()
	
	- password_reset()
	
	- email_activation()
	
Each list of actions are supported through a RESTful API and provides the user with page templates in views. 

2 factor authentication is implemented and requires the user to submit the correct email in order to register a user on the app.

Testing
=======
Testing is performed for all views layer and models layers of each app.

[Coverage](https://pypi.python.org/pypi/coverage) third party app is used to generate the extent of app tests and leads the direction for app testings.

View album and pictures tests are done at 

	albums/tests/test_views.py 
	
and 

	everhash/tests/test_views.py. 
	
These tests ensures client facing parts are tested for correctness of execution.

Model integrity and querysets tests are done at 

	albums/test/test_models.py 

and 

	users/test/test_models.py. 
	
These tests ensures correct querysets are written and model behaviors are as intended.

Acknowledgements
================

Thanks to Mikaela, Michelle Tang and Davide for the inspirations given to build eversnap. It is a really fun project!