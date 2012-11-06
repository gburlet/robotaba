from django import forms

from robotaba.forms import MetaDataForm, GuitarDataForm

class UploadAudioForm(MetaDataForm, GuitarDataForm):
    audio_file = forms.FileField(
        label = "Select an audio file",
        help_text = "Maximum 15MB (.wav)"
    )
