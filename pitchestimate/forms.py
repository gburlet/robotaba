from django import forms

from robotaba.forms import UploadMusicForm

class UploadAudioForm(UploadMusicForm):
    audio_file = forms.FileField(
        label = "Select an audio file",
        help_text = "Maximum 15MB (.wav)"
    )
