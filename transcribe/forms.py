from django import forms

from robotaba.forms import UploadMusicForm
from tabulate.forms import UploadScoreForm

class UploadAudioForm(UploadMusicForm):
    num_frets = forms.IntegerField(
        label = "Number of Guitar Frets",
        min_value = 10,
        max_value = 24,
        initial=22
    )
    tuning = forms.ChoiceField(
        label = "Guitar Tuning",
        choices = [("standard", "Standard (E A D G B E)"),
                   ("drop_d", "Drop D (D A D G B E)")]
    )
    capo = forms.IntegerField(
        label = "Fret location of capo",
        help_text = "0 for no capo",
        min_value = 0,
        max_value = 12,
        initial=0
    )
    audio_file = forms.FileField(
        label = "Select an audio file",
        help_text = "Maximum 15MB (.wav)"
    )
