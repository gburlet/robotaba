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
        choices=[
            ("E4 B3 G3 D3 A2 E2", "Standard (E A D G B E)"),
            ("Eb4 Bb3 Gb3 Db3 Ab2 Eb2", "Tune down 1/2 step (Eb Ab Db Gb Bb Eb)"),
            ("D4 A3 F3 C3 G2 D2", "Tune down 1 step (D G C F A D)"),
            ("C4 G3 Eb3 Bb2 F2 C2", "Tune down 2 steps (C F Bb Eb G3 C4)"),
            ("E4 B3 G3 D3 A2 D2", "Dropped D (D A D G B E)"),
            ("E4 A3 G3 D3 A2 D2", "Dropped D Variant (D A D G A E)"),
            ("D4 B3 G3 D3 A2 D2", "Double Dropped D (D A D G B D)"),
            ("D4 A3 F3 C3 G2 C2", "Dropped C (C G C F A D)"),
            ("Gb4 Db4 A3 E3 B2 E2", "Dropped E (E B E A Db Gb)"),
            ("Db4 Ab3 E3 B2 Gb2 B1", "Dropped B (B Gb B E Ab Db)"),
            ("B3 Gb3 D3 A2 E2 B1", "Baritone (B E A D Gb B)"),
            ("E4 C4 G3 C3 G2 C2", "Open C (C G C G C E)"),
            ("Eb4 C4 G3 C3 G2 C2", "Open Cm (C G C G C Eb)"),
            ("E4 A3 G3 C3 G2 C2", "Open C6 (C G C G A E)"),
            ("E4 B3 G3 E3 G2 C2", "Open CM7 (C G E G B E)"),
            ("D4 A3 Gb3 D3 A2 D2", "Open D (D A D Gb A D)"),
            ("D4 A3 F3 D3 A2 D2", "Open Dm (D A D F A D)"),
            ("D4 A3 D3 D3 A2 D2", "Open D5 (D A D D A D)"),
            ("D4 B3 Gb3 D3 A2 D2", "Open D6 (D A D Gb B D)"),
            ("D4 A3 G3 D3 A2 D2", "Open Dsus4 (D A D G A D)"),
            ("E4 B3 Ab3 E3 B2 E2", "Open E (E B E Ab B E)"),
            ("E4 B3 G3 E3 B2 E2", "Open Em (E B E G B E)"),
            ("E4 B3 G3 E3 A2 E2", "Open Esus11 (E A E G B E"),
            ("F4 C4 F3 C3 A2 F2", "Open F (F A C F C F)"),
            ("D4 B3 G3 D3 G2 D2", "Open G (D G D G B D)"),
            ("D4 Bb3 G3 D3 G2 D2", "Open Gm (D G D G Bb D)"),
            ("D4 C4 G3 D3 G2 D2", "Open Gsus4 (D G D G C D)"),
            ("E4 B3 G3 D3 G2 D2", "Open G6 (D G D G B E)"),
            ("E4 Db4 A3 E3 A2 E2", "Open A (E A E A Db E)"),
            ("E4 C4 A3 E3 A2 E2", "Open Am (E A E A C E)"),
            ("D4 B3 G3 D3 B2 G2", "Dobro Open G (G B D G B D)"),
            ("E4 B3 G4 D4 A3 E3", "Nashville (E A D G B E)"),
            ("E4 B3 Gb3 D3 A2 E2", "Lute or Vihuela (E A D Gb B E)")
        ]
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
