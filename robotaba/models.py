from django.db import models

class Audio(models.Model):
    piece_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200)
    upload_date = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audio')

    def __unicode__(self):
        return str(self.id) + ": " + self.piece_name
