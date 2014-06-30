# std lib imports
# django imports
from django import forms
from django.forms import ModelForm

# 3rd party app imports
# app imports

class AlbumForm(forms.Form):
	hashtag = forms.CharField(max_length = 254, 
							widget=forms.TextInput(attrs={'type':'text', 
																'class': 'form-control', 
																'placeholder':'#hashtag'}))
