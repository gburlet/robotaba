from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from pitchestimate.models import MeiPitch
from robotaba.models import MetaMusic
from robotaba.models import Guitar as GuitarModel
from robotaba.resources.guitarify import Guitarify

import os

from darwintab.ga.simplega import SimpleGA
from darwintab.guitar.guitar import Guitar
from darwintab.score.score import Score
from darwintab.score.scoreevent import Note

from pymei import XmlImport, XmlExport, MeiElement

'''
Entities
'''
class MeiTab(models.Model):
    mei_file = models.FileField(upload_to='mei/tab')
    fk_mid = models.ForeignKey(MetaMusic)

    def get_abs_path(self):
        return str(os.path.join(settings.MEDIA_ROOT, self.mei_file.name))

    def append_guitar_data(self, tuning, capo):
        '''
        Append meta data about the guitar the transcriber is using
        '''

        mei_path = self.get_abs_path()
        mei_doc = XmlImport.documentFromFile(mei_path)

        staff_def = mei_doc.getElementsByName('staffDef')[0]
        sounding_pitches = Guitar.tunings[tuning]
        # From the MEI guidelines:
        # "this is given using the written pitch, not the sounding pitch. 
        # For example, the Western 6-string guitar, in standard tuning, sounds an octave below written pitch."
        written_pitches = [s.pname + str(s.oct+1) for s in sounding_pitches]

        staff_def.addAttribute('lines', str(len(sounding_pitches)))
        staff_def.addAttribute('tab.strings', " ".join(written_pitches))

        # Capo could be implicitly encoded by setting the pitches of the open strings
        # but I really don't like this solution. Instructions are lost about how to tune
        # and perform the piece on the guitar.
        # TODO: this attribute doesn't exist in MEI, make a custom build
        if capo > 0:
            staff_def.addAttribute('tab.capo', str(capo))

        XmlExport.meiDocumentToFile(mei_doc, mei_path)

class Tabulate(models.Model):
    fk_pmei = models.ForeignKey(MeiPitch)
    fk_tmei = models.ForeignKey(MeiTab, null=True)
    fk_guitar = models.ForeignKey(GuitarModel) 
    pitch_sanitize_prune = models.NullBooleanField(null=True)
    # timestamp when processing begins
    process_ts = models.DateTimeField(auto_now_add=True)
    # timestamp when processing has completed
    output_ts = models.DateTimeField(auto_now=True)

    def gen_tab(self):
        input_mei_path = os.path.join(settings.MEDIA_ROOT, self.fk_pmei.mei_file.name)
        filename = os.path.split(input_mei_path)[1]

        # sanitize pitches to conform with the guitar model
        # don't clobber original pmei file, since the tablature should be able to be arranged
        # with different guitar models
        guitarify = Guitarify(self.fk_guitar.num_frets, self.fk_guitar.tuning, self.fk_guitar.capo)
        sanitized_mei_str = guitarify.sanitize_mei_file(self.fk_pmei.get_abs_path(), None, prune=self.pitch_sanitize_prune)

        # instantiate a model of the guitar the user is using
        guitar = Guitar(self.fk_guitar.num_frets, self.fk_guitar.tuning, self.fk_guitar.capo)

        # generate the score model
        score = Score()
        score.parse_mei_str(sanitized_mei_str)
        
        # start up the genetic algorithm
        ga = SimpleGA(500, 50, 5, 0.9, 0.04, True)

        # create tablature for the guitar with the given parameters
        ga.evolve(score, guitar)
        
        # save the elites to the output file
        mei_str = ga.save_elite(score)

        file_contents = ContentFile(mei_str)
        tab = MeiTab(fk_mid=self.fk_pmei.fk_mid)
        tab.mei_file.save(filename, file_contents, save=True)
           
        # append data about the guitar to the MEI document
        tab.append_guitar_data(self.fk_guitar.tuning, self.fk_guitar.capo)

        # attach the tab to the Tabulate object
        self.fk_tmei = tab
        # Note that saving also updates self.output_ts to clock out the
        # analysis time
        self.save()
