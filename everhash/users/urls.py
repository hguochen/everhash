# std lib imports
# django imports
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

# third-party app imports
from registration.backends.default.views import ActivationView

# app imports
from views import UsersRegistrationView,login, profile_view, settings_view
from forms import UsersAuthenticationForm, UsersPasswordResetForm, UsersSetPasswordForm, UsersPasswordChangeForm

urlpatterns = patterns('',
    url(r'^activate/complete/$', TemplateView.as_view(template_name='reg/activation_complete.html'),
        name='registration_activation_complete'),
   # Activation keys get matched by \w+ instead of the more specific
   # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
   # that way it can return a sensible "invalid key" message instead of a
   # confusing 404.
   url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
   url(r'^register/$', UsersRegistrationView.as_view(), name='registration_register'),
   url(r'^register/complete/$', TemplateView.as_view(template_name='reg/registration_complete.html'),
       name='registration_complete'),
   url(r'^register/closed/$', TemplateView.as_view(template_name='reg/registration_closed.html'),
       name='registration_disallowed'),
)

"""
URL patterns for the views included in ``django.contrib.auth``.

Including these URLs (via the ``include()`` directive) will set up the
following patterns based at whatever URL prefix they are included
under:

* User login at ``login/``.

* User logout at ``logout/``.

* The two-step password change at ``password/change/`` and
  ``password/change/done/``.

* The four-step password reset at ``password/reset/``,
  ``password/reset/confirm/``, ``password/reset/complete/`` and
  ``password/reset/done/``.

The default registration backend already has an ``include()`` for
these URLs, so under the default setup it is not necessary to manually
include these views. Other backends may or may not include them;
consult a specific backend's documentation for details.

"""

urlpatterns += patterns('',
    url(r'^login/$', login, {'template_name': 'reg/login.html', 'authentication_form': UsersAuthenticationForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'reg/logout.html'}, name='logout'),
    url(r'^profile/$', profile_view, name='profile'),
    url(r'^password/change/$', auth_views.password_change, {'password_change_form':UsersPasswordChangeForm, 'template_name':'reg/password_change_form.html'}, name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done, {'template_name':'reg/password_change_done.html'}, name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, {'password_reset_form':UsersPasswordResetForm, 'template_name':'reg/password_reset_form.html'}, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'set_password_form':UsersSetPasswordForm, 'template_name':'reg/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, {'template_name':'reg/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, {'template_name':'reg/password_reset_done.html'}, name='password_reset_done'),
    url(r'^settings/$', settings_view, name='settings'),
)
