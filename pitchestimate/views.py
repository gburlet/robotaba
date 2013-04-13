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
from pitchestimate.forms import UploadAudioForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from robotaba.models import Audio, MetaMusic
from robotaba.models import Guitar as GuitarModel
from pitchestimate.models import PitchDetect

import os

def upload_audio(request):
    '''
    Handle audio file upload
    '''

    if request.method == 'POST':
        # handle form input
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # check extension of uploaded audio file
            input_file = request.FILES['audio_file']
            filename, input_ext = os.path.splitext(input_file.name)
            if input_ext != '.wav':
                raise ValueError('Input file must be a .wav file')

            # enter metadata of the uploaded audio into the db
            # TODO: hook up to musicbrainz to gather this information
            meta = MetaMusic(
                title=request.POST['title'], 
                artist=request.POST['artist'],
                copyright=request.POST['copyright']
            )
            meta.save()

            get_vars = ""
            if request.POST.get('guitarify', False):
                frets = request.POST['num_frets']
                capo = request.POST['capo']
                tuning = request.POST['tuning']
                sanitize = request.POST['pitch_sanitize']

                get_vars = '?frets=%s&capo=%s&tuning=%s&sanitize=%s' % (frets, capo, tuning, sanitize)

            audio = Audio(fk_mid=meta, audio_file=input_file)
            audio.save()

            return HttpResponseRedirect('/pitchestimate/%d/%s' % (audio.id, get_vars))
    else:
        # serve the form
        form = UploadAudioForm()

    return render_to_response('uploadaudio.html', {'form': form}, context_instance=RequestContext(request))

def process(request, audio_id):
    # query db for the audio file
    audio = get_object_or_404(Audio, pk=audio_id)

    guitar_model = True
    try:
        frets = int(request.GET['frets'])
        capo = int(request.GET['capo'])
        tuning = request.GET['tuning']
        pitch_sanitize_prune = True if request.GET['sanitize'] == 'prune' else False
    except KeyError:
        # don't use a guitar model for polyphonic transcription
        guitar_model = False

    db_fields = {'fk_audio': audio}
    if guitar_model:
        guitar = GuitarModel(
            num_frets=frets,
            capo=capo,
            tuning=tuning
        )
        guitar.save()

        db_fields['fk_guitar'] = guitar
        db_fields['pitch_sanitize_prune'] = pitch_sanitize_prune

    pestimator = PitchDetect(**db_fields)
    # writing to the database writes the analysis start timestamp
    pestimator.save()

    # TODO: create spinner on the interface
    audio_url = request.build_absolute_uri(audio.audio_file.url)
    pestimator.estimate_pitches(audio_url)

    # redirect to xml display
    return HttpResponseRedirect('/media/%s' % pestimator.fk_pmei.mei_file.name)
