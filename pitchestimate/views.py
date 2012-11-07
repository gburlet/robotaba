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
    pestimator.estimate_pitches()

    # redirect to xml display
    return HttpResponseRedirect('/media/%s' % pestimator.fk_pmei.mei_file.name)
