from django.db import models
from django.conf import settings

from pitchestimate.models import MeiPitch

import os

from darwintab.ga.simplega import SimpleGA
from darwintab.guitar.guitar import Guitar
from darwintab.score.score import Score

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
        # TODO: figure out a better way to tie the mei output writesting to the Django FileField
        output_mei_path = os.path.join(settings.MEDIA_ROOT, 'mei/tab', filename)

        # instantiate a model of the guitar the user is using
        guitar = Guitar(self.num_frets, self.tuning)

        # generate the score model
        score = Score(input_mei_path)
        
        # start up the genetic algorithm
        ga = SimpleGA(400, 5, 6, 0.6, 0.05, True)

        # create tablature for the guitar with the given parameters
        ga.evolve(score, guitar)
        
        # save the elites to the output file
        ga.save_elite(score, str(output_mei_path))

        # get metadata of tab
        tab = MeiTab(fk_mid=self.fk_pmei.fk_mid, mei_file=output_mei_path)
        tab.save()

        # attach the tab to the Tabulate object
        self.fk_tmei=tab
        # Note that saving also updates self.output_ts to clock out the
        # analysis time
        self.save()

        return output_mei_path
