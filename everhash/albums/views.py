# std lib imports
# django imports
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# third-party app imports
# app imports
from models import Album
from pictures.views import Picture
from everhash.settings.base import S3_URL
from forms import AlbumForm

@login_required
def add_album(request):
	"""
	Add a new album by POST-ing a hashtag.
	"""
	album_form = AlbumForm(request.POST or None)
	errors = []

	if request.method == 'POST':
		if album_form.is_valid():
			# sanitize data
			value = album_form.cleaned_data
			hashtag = value['hashtag']
			print hashtag
			# get existing database albums
			user = User.objects.get(username=request.user)			
			user_albums = Album.objects.get_user_posted_albums(user=user)
			print user_albums

			for album in user_albums:
				if album.name == hashtag:
					errors.append('Album already exists.')
					break
			
			# add album to user albums if it doesn't exist already.
			if len(errors) == 0:
				new_album = Album(name=hashtag, user=user)
				new_album.save()
				print hashtag			
				return HttpResponseRedirect(reverse('add_confirm', kwargs={'hashtag':hashtag}))
			else:
				context_instance = RequestContext(request, {'errors':errors})
				return render_to_response('add_album.html', context_instance)

	context_instance = RequestContext(request, {'album_form':album_form, 'errors':errors})
	return render_to_response('add_album.html', context_instance)

def add_confirm(request, hashtag=None):
	"""
	Confirmation view for adding a new album.
	"""
	context_instance = RequestContext(request, {'hashtag':hashtag})
	return render_to_response('add_album_confirmation.html', context_instance)

def view_album(request, album_name=None):
	"""
	Takes in an album name parameter and display the album page. Return a 404 page if album does not exist.
	"""
	album_name = album_name.lower()
	album = get_object_or_404(Album, name=album_name)
	
	if album != None:
		# get album pictures
		pictures = Picture.objects.album_pictures(album)
		
		# get picture s3 url
		pictureset = []
		urls = []
		for pic in pictures:			
			url = S3_URL + pic.album.name + "/" +pic.url
			urls.append(url)
			pictureset.append([pic, url])
		# get sharing icon
		icon = Picture.objects.get_most_popular(album_name)
		icon = S3_URL + album_name + "/" + pic.url

		context_instance = RequestContext(request, 
										{'album':album_name, 'pictureset':pictureset, 'icon':icon, 'urls':urls})
	return render_to_response('album.html', context_instance)