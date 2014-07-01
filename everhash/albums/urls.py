# std lib imports
#django imports
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# third-party app imports
#app imports


urlpatterns = patterns('',
	# album app level urls 
	# urls routes over from everhash.urls
    url(r'^add/$', 'albums.views.add_album', name='add_album'),
    url(r'^add/(?P<hashtag>\w+)/$', 'albums.views.add_confirm', name='add_confirm'),
    url(r'^(?P<album_name>\w+)/$', 'albums.views.view_album', name='view_album'),
)