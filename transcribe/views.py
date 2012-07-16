from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from robotaba.models import Audio
from transcribe.models import Transcription
from transcribe.forms import UploadAudioForm

def upload_audio(request):
    '''
    Handle an audio file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # enter audio information into db
            meta_data = MetaMusic(title=request.POST['title'], artist=request.POST['artist'], copyright=request.POST['copyright'])
            meta_data.save()

            new_audio = Audio(fk_mid=meta_data.id, audio_file=request.FILES['audio_file'])
            new_audio.save()

            return HttpResponseRedirect('/transcribe/%s' % str(new_audio.id))
    else:
        # serve the form
        form = UploadAudioForm()

    return render_to_response('uploadaudio.html', {'form': form}, context_instance=RequestContext(request))

def process(request, audio_id):
    # query db for the audio id
    audio = get_object_or_404(Audio, pk=audio_id)

    # transcribe the audio
    #t = Transcription(audio_id=audio)
    #t.transcribe()
    
    return HttpResponse("Transcribing audio id (%s)." % audio_id)
