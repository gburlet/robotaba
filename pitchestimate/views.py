from django.http import HttpResponseRedirect, HttpResponse
from pitchestimate.forms import UploadAudioForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from robotaba.models import Audio, MetaMusic
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

            audio = Audio(fk_mid=meta, audio_file=input_file)
            audio.save()

            return HttpResponseRedirect('/pitchestimate/%d/' % audio.id)
    else:
        # serve the form
        form = UploadAudioForm()

    return render_to_response('uploadaudio.html', {'form': form}, context_instance=RequestContext(request))

def process(request, audio_id):
    # query db for the audio file
    audio = get_object_or_404(Audio, pk=audio_id)

    p_detector = PitchDetect(fk_audio=audio)
    # writing to the database writes the analysis start timestamp
    p_detector.save()

    # TODO: create spinner on the interface
    p_detector.estimate_pitches()

    # redirect to xml display
    return HttpResponseRedirect('/media/%s' % p_detector.fk_pmei.mei_file.name)
