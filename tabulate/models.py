from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from pitchestimate.models import MeiPitch

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

class Tabulate(models.Model):
    fk_pmei = models.ForeignKey(MeiPitch)
    fk_tmei = models.ForeignKey(MeiTab, null=True)
    num_frets = models.IntegerField(default=22)
    tuning = models.CharField(max_length=25, default='standard')
    capo = models.IntegerField(default=0)
    # timestamp when processing begins
    process_ts = models.DateTimeField(auto_now_add=True)
    # timestamp when processing has completed
    output_ts = models.DateTimeField(auto_now=True)

    def gen_tab(self):
        input_mei_path = os.path.join(settings.MEDIA_ROOT, self.fk_pmei.mei_file.name)
        filename = os.path.split(input_mei_path)[1]

        # instantiate a model of the guitar the user is using
        guitar = Guitar(self.num_frets, self.tuning)

        # generate the score model
        score = Score(input_mei_path)
        
        # start up the genetic algorithm
        ga = SimpleGA(100, 25, 4, 0.65, 0.04, True)

        # create tablature for the guitar with the given parameters
        ga.evolve(score, guitar)
        
        # save the elites to the output file
        mei_str = ga.save_elite(score)
        mei_str = self._appendMetaData(mei_str)
        file_contents = ContentFile(mei_str)
        
        tab = MeiTab()
        tab.mei_file.save(filename, file_contents, save=True)

        # attach the tab to the Tabulate object
        self.fk_tmei = tab
        # Note that saving also updates self.output_ts to clock out the
        # analysis time
        self.save()

    def _appendMetaData(self, mei_str):
        '''
        Append meta data about the guitar the transcriber is using
        '''

        mei_doc = XmlImport.documentFromText(mei_str)

        staff_def = mei_doc.getElementsByName('staffDef')[0]
        sounding_pitches = Guitar.tunings[self.tuning]
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
        staff_def.addAttribute('tab.capo', str(self.capo))

        return XmlExport.meiDocumentToText(mei_doc)
