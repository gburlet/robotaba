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

import os
from scikits.audiolab import wavread

from django.db import models
from django.conf import settings

from robotaba.models import Audio
from robotaba.models import Guitar as GuitarModel
from pitchestimate.models import PitchDetect
from tabulate.models import Tabulate


class Transcription(models.Model):
    fk_audio = models.ForeignKey(Audio)
    fk_pid = models.ForeignKey(PitchDetect)
    fk_tabid = models.ForeignKey(Tabulate)

    def __unicode__(self):
        return self.id

    def transcribe(self, frets, capo, tuning, pitch_sanitize_prune, audio_url):
        # get path of audio file being transcribed
        path = os.path.join(settings.MEDIA_ROOT, str(self.fk_audio.audio_file))

        ####################
        # PITCH ESTIMATION #
        ####################
        guitar = GuitarModel(
            num_frets=frets,
            capo=capo,
            tuning=tuning
        )
        guitar.save()

        pestimator = PitchDetect(fk_audio=self.fk_audio, fk_guitar=guitar, pitch_sanitize_prune=pitch_sanitize_prune)
        # writing to the database writes the analysis start timestamp
        pestimator.save()

        pestimator.estimate_pitches(audio_url)

        # attach the pitch detection analysis information to the transcription model
        self.fk_pid = pestimator

        ########################
        # TABLATURE GENERATION #
        ########################
        taber = Tabulate(fk_pmei=self.fk_pid.fk_pmei, fk_guitar=guitar, pitch_sanitize_prune=pitch_sanitize_prune)
        # writing to the database writes the analysis start timestamp
        taber.save()

        taber.gen_tab()

        # attach the tablature to the transcription model
        self.fk_tabid = taber

        self.save()

