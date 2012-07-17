from django.db import models

from robotaba.models import Audio

'''
Entities
'''
class MeiPitch(models.Model):
    mei_file = models.FileField(upload_to='mei/pitch')
    # may be null (if uploaded just for tab generation)
    upload_ts = models.DateTimeField(auto_now_add=True, null=True)

class PitchDetect(models.Model):
    fk_audio = models.ForeignKey(Audio)
    fk_pmei = models.ForeignKey(MeiPitch)
    # timestamp when processing begins
    process_ts = models.DateTimeField(auto_now_add=True)
    # timestamp when processing has completed
    output_ts = models.DateTimeField(auto_now_add=True)
