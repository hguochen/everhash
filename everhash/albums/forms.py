# std lib imports
# django imports
from django import forms
from django.forms import ModelForm

# 3rd party app imports
# app imports

class AlbumForm(forms.Form):
	"""
	Album forms capture only a single hashtag field. Users who submit to this field will indicate a new album setup.
	"""
	hashtag = forms.CharField(max_length = 254, 
							widget=forms.TextInput(attrs={'type':'text', 
																'class': 'form-control', 
																'placeholder':'#hashtag'}))
