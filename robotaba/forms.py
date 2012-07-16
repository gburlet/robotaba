from django import forms

class UploadMusicForm(forms.Form):
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
