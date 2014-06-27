# std lib imports
# django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# third-party app imports
# app imports

def index(request):
	if request.method == "GET":
		return render_to_response('index.html', context_instance=RequestContext(request))