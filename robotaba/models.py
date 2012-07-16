from django.db import models

class MetaMusic(models.Model):
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    copyright = models.CharField(max_length=50, null=True)

class Audio(models.Model):
    fk_mid = models.ForeignKey(MetaMusic)
    # timestamp of when the audio was uploaded to the server
    upload_ts = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audio')

    def __unicode__(self):
        return str(self.id) + ": " + self.piece_name
