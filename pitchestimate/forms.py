from django import forms

from robotaba.forms import MetaDataForm, GuitarDataForm

class UploadAudioForm(MetaDataForm, GuitarDataForm):
    guitarify = forms.BooleanField(
        label = "Guitarify",
        help_text = "Create pitch estimates in the pitch range of your guitar",
        required=False
    )
    audio_file = forms.FileField(
        label = "Select an audio file",
        help_text = "Maximum 15MB (.wav)"
    )
