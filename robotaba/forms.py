from django import forms

class UploadAudioForm(forms.Form):
    piece_name = forms.CharField(
        max_length=200,
        label="Name of piece"
    )
    author_name = forms.CharField(
        max_length=200,
        label="Name of author"
    )
    audio_file = forms.FileField(
        label = "Select an audio file",
        help_text = "Maximum 15MB (.wav, .mp3)"
    )
