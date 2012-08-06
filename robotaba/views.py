from django.template import RequestContext
from django.shortcuts import render_to_response

from robotaba.models import Audio, MetaMusic

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

def about(request):
    '''
    Serve the about page
    '''

    return render_to_response('about.html', context_instance=RequestContext(request))

def contact(request):
    '''
    Serve the contact page
    '''

    return render_to_response('contact.html', context_instance=RequestContext(request))
