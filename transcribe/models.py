from django.db import models

from robotaba.models import Audio

class Transcription(models.Model):
    audio = models.ForeignKey(Audio)
    analysis_time = models.DecimalField(max_digits=12, decimal_places=2)
    midi_path = models.CharField(max_length=200)
    tab_path = models.CharField(max_length=200)

    def __unicode__(self):
        return self.id
