'''
Copyright (C) 2013 Gregory Burlet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from django import forms

class MetaDataForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label='Title'
    )
    artist = forms.CharField(
        max_length=50,
        label='Artist'
    )
    copyright = forms.CharField(
        max_length=50,
        label='Copyright Holder'
    )

class GuitarDataForm(forms.Form):
    pitch_sanitize=forms.ChoiceField(
        label="Pitch sanitization",
        choices=[("prune", "Prune"),
                 ("transpose", "Transpose")],
        initial="prune",
        widget=forms.RadioSelect()
    )
    num_frets=forms.IntegerField(
        label="Number of Guitar Frets",
        min_value=10,
        max_value=24,
        initial=22
    )
    tuning = forms.ChoiceField(
        label="Guitar Tuning",
        choices=[("standard", "Standard (E A D G B E)"),
                   ("drop_d", "Drop D (D A D G B E)")]
    )
    capo = forms.IntegerField(
        label="Fret location of capo",
        help_text="0 for no capo",
        min_value=0,
        max_value=12,
        initial=0
    )

class UploadTablatureForm(MetaDataForm):
    score_file = forms.FileField(
        label = "Select a symbolic music file",
        help_text = "Maximum 15MB (.xml, .mei)"
    )
