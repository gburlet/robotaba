from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

from robotaba.models import Audio
from robotaba.forms import UploadAudioForm

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html')

def upload_audio(request):
    '''
    Handle an audio file upload
    '''

    if request.method == 'POST':
        # deal with the form input
        form = UploadAudioForm(request.POST, request.FILES)
        if form.is_valid():
            # enter audio information into db
            new_audio = Audio(audio_file=request.FILES['audio_file'], piece_name=request.POST['piece_name'], author_name=request.POST['author_name'])
            new_audio.save()
            return HttpResponseRedirect('/transcribe/' + str(new_audio.id))
    else:
        # serve the form
        form = UploadAudioForm()

    return render_to_response('uploadaudio.html', {'form': form}, context_instance=RequestContext(request))
