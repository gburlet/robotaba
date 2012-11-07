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

    def transcribe(self, frets, capo, tuning, pitch_sanitize_prune):
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

        pestimator.estimate_pitches()

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

