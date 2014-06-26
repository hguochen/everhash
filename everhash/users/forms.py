# std lib imports
# django imports
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
# third-party app imports
from registration.forms import RegistrationFormUniqueEmail

# app imports


class UsersRegistrationForm(RegistrationFormUniqueEmail):
	username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
                                widget=forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'placeholder':'Username'}))
	email = forms.EmailField(label=_("Email address"), widget=forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'placeholder':'Email'}))
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control', 'placeholder':'Password'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control', 'placeholder':'Confirm Password'}))


class UsersAuthenticationForm(AuthenticationForm):
	username = forms.CharField(max_length = 254, widget=forms.TextInput(attrs={'type':'text', 'class': 'form-control', 'placeholder':'Username'}))
	password = forms.CharField(max_length = 100, label=_("Password"), widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control', 'placeholder': 'Password'}))


class UsersPasswordResetForm(PasswordResetForm):
	"""
	Generates a one-use only link for resetting password and sends to the users' specified email
	"""
	email = forms.EmailField(label=_("Email address"), widget=forms.TextInput(attrs={'type':'text', 'class' : 'form-control', 'placeholder': 'Email'}))


class UsersSetPasswordForm(SetPasswordForm):
	"""
	Sub class SetPasswordForm that lets a user set his/her password without entering the old password
	"""
	new_password1 = forms.CharField(max_length = 100, label=_("New password:"), widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control'}))
	new_password2 = forms.CharField(max_length = 100, label=_("Confirm password:"), widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control'}))


class UsersPasswordChangeForm(UsersSetPasswordForm):
	"""
	Sub class PasswordChangeForm that lets a user change his/her password by entering their old password
	"""
	old_password = forms.CharField(max_length = 100, label=_("Old password:"), widget=forms.PasswordInput(attrs={'type':'password', 'class' : 'form-control'}))

	def __init__(self, *args, **kwargs):
		super(UsersPasswordChangeForm, self).__init__(*args, **kwargs)
		self.fields.keyOrder = ['old_password', 'new_password1', 'new_password2']


class UsersProfileForm(forms.ModelForm):
	"""
	Custom form that lets users change his/her personal information.
	"""	
	username = forms.RegexField(required=True, regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=_("Username"),
                                error_messages={'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")},
                                widget=forms.TextInput(attrs={'type':'text', 'class' : 'form-control'}))	
	email = forms.EmailField(required=True, label=_("Email address"), widget=forms.TextInput(attrs={'type':'email', 'class' : 'form-control'}))
	first_name = forms.CharField(required=False, label=_(u'First name'), max_length=30, widget=forms.TextInput(attrs={'type':'text', 'class':'form-control'}))
	last_name = forms.CharField(required=False, label=_(u'Last name'), max_length=30, widget=forms.TextInput(attrs={'type':'text', 'class':'form-control'}))	

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']