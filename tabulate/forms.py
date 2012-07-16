from django import forms

from robotaba.forms import UploadMusicForm

class UploadScoreForm(UploadMusicForm):
    num_frets = forms.IntegerField(
        label = "Number of Guitar Frets",
        min_value = 12,
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
    score_file = forms.FileField(
        label = "Select a symbolic music file",
        help_text = "Maximum 15MB (.xml, .mei)"
    )
