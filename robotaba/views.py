from django.template import RequestContext
from django.shortcuts import render_to_response

from robotaba.models import Audio, MetaMusic

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))


