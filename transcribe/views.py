from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from robotaba.models import MetaMusic, Audio
from transcribe.models import Transcription
from transcribe.forms import UploadAudioForm
from tabulate.views import display

import os

def upload_audio(request):
    '''
    Handle an audio file upload
    '''

    if request.method == 'POST':
        # deal with the form input
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

            audio = Audio(fk_mid=meta, audio_file=input_file)
            audio.save()

            frets = request.POST['num_frets']
            capo = request.POST['capo']
            tuning = request.POST['tuning']

            return HttpResponseRedirect('/transcribe/%d/?frets=%s&capo=%s&tuning=%s' % (audio.id, frets, capo, tuning))
    else:
        # serve the form
        form = UploadAudioForm()

    return render_to_response('uploadtranscribe.html', {'form': form}, context_instance=RequestContext(request))

def process(request, audio_id):
    # query db for the audio id
    audio = get_object_or_404(Audio, pk=audio_id)

    try:
        frets = int(request.GET['frets'])
        capo = int(request.GET['capo'])
        tuning = request.GET['tuning']
    except KeyError:
        return HttpResponse("Need to specify number of frets, capo position, and guitar tuning")

    # transcribe the audio
    # TODO: GUI spinner
    t = Transcription(fk_audio=audio)
    t.transcribe(frets, capo, tuning)
    
    # redirect to tab display page
    return HttpResponseRedirect('/tabulate/display/%d' % t.fk_tabid.fk_tmei.id)
