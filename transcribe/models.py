import os
from scikits.audiolab import wavread

from django.db import models
from django.conf import settings

from robotaba.models import Audio
from pitchestimate.models import PitchDetect
from tabulate.models import Tabulate


class Transcription(models.Model):
    audio_id = models.ForeignKey(Audio)
    fk_pid = models.ForeignKey(PitchDetect)
    fk_tabid = models.ForeignKey(Tabulate)

    def __unicode__(self):
        return self.id

    def transcribe(self):
        # get path of audio file being transcribed
        path = os.path.join(settings.MEDIA_ROOT, str(self.audio_id.audio_file))
        out_path = os.path.join(settings.MEDIA_ROOT, '/midi/test.mid')

        # min and max f0 candidates from gagnon2003, "A Neural Network Approach
        # for Pre-classification in Musical Chords Recognition (82.41Hz - 1244.51Hz)
        #transcriber = F0Estimate(path, max_poly=6, min_f0=82, max_f0=1245, method='iterative', frame_len=0.093)
        #transcriber.gen_piano_roll(out_path)
