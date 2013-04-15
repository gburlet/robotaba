'''
Copyright (C) 2013 Gregory Burlet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from __future__ import division
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.conf import settings

import os
import math

from robotaba.models import Audio, MetaMusic
from tabulate.models import MeiTab
from robotaba.resources.meitoalphatex import meitoalphatex
from robotaba.forms import UploadTablatureForm

def home(request):
    '''
    Serve the home page
    '''

    # get 10 most recent tablatures.
    num_tabs = 4
    tabs = MeiTab.objects.all()
    if num_tabs <= len(tabs):
        tabs = tabs[len(tabs)-num_tabs:]
    
    return render_to_response('index.html', {'tabs': tabs}, context_instance=RequestContext(request))

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

def tabs(request):
    '''
    List all tabs
    '''

    tabs = MeiTab.objects.all()
    page_numbers = [i+1 for i in range(int(math.ceil(len(tabs) / settings.NUM_RESULTS)))]

    p = int(request.GET.get('p', 1))
    i_start = (p-1) * settings.NUM_RESULTS
    i_end = i_start + settings.NUM_RESULTS
    if i_end >= len(tabs):
        i_end = len(tabs)
    tabs = tabs[i_start:i_end]

    return render_to_response('tabs.html', {'tabs': tabs, 'pages': page_numbers}, context_instance=RequestContext(request))

def search(request):
    '''
    Search for tabs
    '''

    q = request.GET.get('q')
    if q:
        mm = [m.id for m in MetaMusic.objects.filter(Q(title__icontains=q) | Q(artist__icontains=q))]
        tabs = MeiTab.objects.filter(pk__in=mm)
        page_numbers = [i+1 for i in range(int(math.ceil(len(tabs) / settings.NUM_RESULTS)))]

        p = int(request.GET.get('p', 1))
        i_start = (p-1) * settings.NUM_RESULTS
        i_end = i_start + settings.NUM_RESULTS
        if i_end >= len(tabs):
            i_end = len(tabs)
        tabs = tabs[i_start:i_end]
    else:
        tabs = []
        page_numbers = []

    return render_to_response('results.html', {'tabs': tabs, 'pages': page_numbers}, context_instance=RequestContext(request))

def upload_tablature(request):
    '''
    Handle score file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadTablatureForm(request.POST, request.FILES)
        if form.is_valid():
            # check extension of uploaded score file
            input_file = request.FILES['score_file']

            # TODO: try and parse this information from the XML file
            meta = MetaMusic(
                title=request.POST['title'], 
                artist=request.POST['artist'],
                copyright=request.POST['copyright']
            )
            meta.save()

            filename, input_ext = os.path.splitext(input_file.name)
            if input_ext == '.xml':
                # convert the MusicXML file to Mei format
                tmei = MeiTab(fk_mid=meta)
                tmei.convert_musicxml(filename+'.mei', request.FILES['score_file'].read())
            elif input_ext == '.mei':
                # the uploaded file is an mei file, put it directly into the model
                tmei = MeiTab(mei_file=input_file, fk_mid=meta)
                tmei.save()
            else:
                raise ValueError('Input file must be a MusicXML or Mei file')

            # display the uploaded tab
            return HttpResponseRedirect('/display/%d' % tmei.id)
    else:
        # serve the form
        form = UploadTablatureForm()

    return render_to_response('uploadtablature.html', {'form': form}, context_instance=RequestContext(request))

def display(request, tmei_id):
    # query db for the mei tab file
    tmei = get_object_or_404(MeiTab, pk=tmei_id)

    alpha_tex = meitoalphatex(tmei.mei_file.path)

    return render_to_response('displaytab.html', {'alphatex': alpha_tex}, context_instance=RequestContext(request))
