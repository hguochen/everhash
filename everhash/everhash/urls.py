# std lib imports
#django imports
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# third-party app imports
#app imports

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'views.index', name='index'),    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
# albums app urls
urlpatterns += patterns('',
    url(r'^album/', include('albums.urls')),
)
# users app urls
urlpatterns += patterns('',
    url(r'^accounts/', include('users.urls')),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
