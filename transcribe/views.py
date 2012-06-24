from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from robotaba.models import Audio

def index(request, audio_id):
    # query db for audio information
    audio = get_object_or_404(Audio, pk=audio_id)

    return HttpResponse("Transcribing audio id (%s)." % audio.piece_name)
