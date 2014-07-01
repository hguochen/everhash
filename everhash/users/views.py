# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.http import is_safe_url
from django.contrib.sites.models import get_current_site
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# third-party app imports
from registration.backends.default.views import RegistrationView

#app imports
from settings.base import LOGIN_REDIRECT_URL
from albums.utils import generate_album_thumbnail
from albums.models import Album
from .forms import UsersRegistrationForm, UsersProfileForm, UsersPasswordChangeForm
from .utils import get_user_albums_count, get_user_picture_count, get_user_albums, get_user_picture_count, dictionary_store


class UsersRegistrationView(RegistrationView):
	"""Sub class for user registration views"""
	
	form_class = UsersRegistrationForm
	success_url = None	

@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='reg/login.html',
	redirect_field_name=REDIRECT_FIELD_NAME,
	authentication_form=None,
	current_app=None, extra_content=None):
	"""
	Displays the login form and handles the login action.
	"""
	
	# set redirect
	redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, LOGIN_REDIRECT_URL))
	if request.method == "POST":
		form = authentication_form(request, data=request.POST)
		if form.is_valid():

			# Ensure the user-originating redirection url is safe.
			if not is_safe_url(url=redirect_to, host=request.get_host()):
				redirect_to = resolve_url(LOGIN_REDIRECT_URL)

			# Okay, security check complete. Log the user in.
			auth_login(request, form.get_user())

			# If remember me checkbox is checked, set expiry time to 2 weeks
			if request.POST.has_key('remember_me'):
				request.session.set_expiry(1209600) # 2 weeks

			return HttpResponseRedirect(redirect_to)
	else:
		form = authentication_form(request)

	current_site = get_current_site(request)
	# collate context
	context = {
		'form': form,
		redirect_field_name: redirect_to,
		'site': current_site,
		'site_name': current_site.name,
	}
	return TemplateResponse(request, template_name, context,
							current_app=current_app)

@login_required
def profile_view(request):
	"""Setup and get the profile view of users."""
	if request.user.is_authenticated():
		# get user instance
		user = User.objects.get(username=request.user)
		
		# put user usage stats into dictionary
		stats = {}
		stats['album_count'] = get_user_albums_count(user)
		stats['picture_count'] = get_user_picture_count(user)
		
		# get all albums by users
		albums = Album.objects.get_user_posted_albums(user)
		# store album names in a dict
		album_names = dictionary_store(albums)

		# generate thumbnail
		thumbnail = generate_album_thumbnail(album_names)
		
		context_instance = RequestContext(request, {'user': user, 'stats':stats, 'thumb_nail':thumbnail})
		return render_to_response('reg/account.html', context_instance)
	else:
		HttpResponseRedirect(reverse('login'))

@login_required
def settings_view(request):
	"""Settings view for request.user pre-populated with user configurable details."""
	user_object = User.objects.get(username=request.user)
	ProfileFormSet = modelformset_factory(User, form=UsersProfileForm, extra=0)
	profile_formset = ProfileFormSet(request.POST or None, queryset=User.objects.filter(username=request.user), initial=[
										{'username': user_object.username,
										 'email': user_object.email,
										 'first_name': user_object.first_name,
										 'last_name': user_object.last_name}
										])	
	if request.method == 'POST':
		if profile_formset.is_valid():
			profile_formset.save()
		return HttpResponseRedirect(reverse('settings'))
	else:
		return render_to_response('reg/settings.html', {'profile_formset':profile_formset}, context_instance=RequestContext(request))

