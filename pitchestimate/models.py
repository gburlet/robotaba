from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings

from robotaba.models import Audio

from musicxmlmeiconversion.musicxmltomei import MusicXMLtoMei
from multif0estimation.f0estimate import F0Estimate

import os

'''
Entities
'''
class MeiPitch(models.Model):
    mei_file = models.FileField(upload_to='mei/pitch')
    # may be null (if uploaded just for tab generation)
    upload_ts = models.DateTimeField(auto_now_add=True, null=True)

    def convert_musicxml(self, mei_filename, musicxml_str):
        # convert the musicxml string to mei string
        meiconv = MusicXMLtoMei(input_str=musicxml_str)
        mei_str = meiconv.convert()

        # save the string to a file in the Django media location
        file_contents = ContentFile(mei_str)
        self.mei_file.save(mei_filename, file_contents, save=True)

class PitchDetect(models.Model):
    fk_audio = models.ForeignKey(Audio)
    fk_pmei = models.ForeignKey(MeiPitch, null=True)
    # timestamp when processing begins
    process_ts = models.DateTimeField(auto_now_add=True)
    # timestamp when processing has completed
    output_ts = models.DateTimeField(auto_now=True)

    def estimate_pitches(self):
        input_audio_path = os.path.join(settings.MEDIA_ROOT, self.fk_audio.audio_file.name)
        # get filename and change extension to mei
        filename, _ = os.path.splitext(os.path.split(input_audio_path)[1])
        filename += '.mei'

        # perform the pitch estimation on the audio input file
        freq_est = F0Estimate(max_poly=1)
        f0_estimates, notes = freq_est.estimate_f0s(input_audio_path)
        notes_c = freq_est.collapse_notes(notes)
        mei_str = freq_est.write_mei(notes_c)

        # save the mei to the output file
        file_contents = ContentFile(mei_str)
        pmei = MeiPitch()
        pmei.mei_file.save(filename, file_contents, save=True)

        # attach the tab to the Tabulate object
        self.fk_pmei = pmei
        # Note that saving also updates self.output_ts to clock out the
        # analysis time
        self.save()
