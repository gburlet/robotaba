from django import forms

from robotaba.forms import MetaDataForm, GuitarDataForm

class UploadScoreForm(MetaDataForm, GuitarDataForm):
    score_file = forms.FileField(
        label = "Select a symbolic music file",
        help_text = "Maximum 15MB (.xml, .mei)"
    )
