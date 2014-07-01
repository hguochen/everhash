========================
Project_everhash
========================
Everhash is a web application that crawls the twitter-universe by specific hashtags, retrieves and stores media contents. In the current version 1.0, only images with extension, jpg, png, diff, gif are stored. Future versions are expected to store audio/video contents with support for typical media extensions such as mp4, avi etc.

A Django 1.6.5(python 2.7.5) project. This is part of an assignment done with [Eversnap](http://www.geteversnap.com/).

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
###albums

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

Acknowledgements
================

- Many thanks to Randall Degges for the inspiration to write the book and django-skel.
- All of the contributors_ to this project.

.. _contributors: https://github.com/twoscoops/django-twoscoops-project/blob/master/CONTRIBUTORS.txt
