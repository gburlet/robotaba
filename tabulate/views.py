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

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from robotaba.models import MetaMusic
from robotaba.models import Guitar as GuitarModel
from pitchestimate.models import MeiPitch
from tabulate.models import MeiTab, Tabulate
from tabulate.forms import UploadScoreForm

import os

def upload_score(request):
    '''
    Handle score file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadScoreForm(request.POST, request.FILES)
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
                pmei = MeiPitch(fk_mid=meta)
                pmei.convert_musicxml(filename+'.mei', request.FILES['score_file'].read())
            elif input_ext == '.mei':
                # the uploaded file is an mei file, put it directly into the model
                pmei = MeiPitch(mei_file=input_file, fk_mid=meta)
                pmei.save()
            else:
                raise ValueError('Input file must be a MusicXML or Mei file')
            
            frets = request.POST['num_frets']
            capo = request.POST['capo']
            tuning = request.POST['tuning']
            sanitize = request.POST['pitch_sanitize']

            # redirect and construct the Tabulate object in the process view to allow
            # the input file to be processed multiple times by the user
            # to get different tablature output, if desired.
            return HttpResponseRedirect('/tabulate/%d/?frets=%s&capo=%s&tuning=%s&sanitize=%s' % (pmei.id, frets, capo, tuning, sanitize))
    else:
        # serve the form
        form = UploadScoreForm()

    return render_to_response('uploadscore.html', {'form': form}, context_instance=RequestContext(request))

def process(request, pmei_id):
    # query db for the mei file containing the pitch information
    pmei = get_object_or_404(MeiPitch, pk=pmei_id)

    try:
        frets = int(request.GET['frets'])
        capo = int(request.GET['capo'])
        tuning = request.GET['tuning']
        pitch_sanitize_prune = True if request.GET['sanitize'] == 'prune' else False
    except KeyError:
        return HttpResponse("Need to specify number of frets, capo position, and guitar tuning")

    guitar = GuitarModel(
        num_frets=frets,
        capo=capo,
        tuning=tuning
    )
    guitar.save()

    taber = Tabulate(fk_pmei=pmei, fk_guitar=guitar, pitch_sanitize_prune=pitch_sanitize_prune)
    # writing to the database writes the start timestamp
    taber.save()

    # TODO: create spinner on interface
    taber.gen_tab()

    # redirect to tab display page
    return HttpResponseRedirect('/display/%d' % taber.fk_tmei.id)
