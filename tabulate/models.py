from django.db import models

from robotaba.models import MetaMusic
from pitchestimate.models import MeiPitch

'''
Entities
'''
class MeiTab(models.Model):
    fk_mid = models.ForeignKey(MetaMusic)
    path = models.CharField(max_length=200)

class Tabulate(models.Model):
    fk_pmei = models.ForeignKey(MeiPitch)
    fk_tmei = models.ForeignKey(MeiTab)
    # timestamp when processing begins
    process_ts = models.DateTimeField(auto_now_add=True)
    # timestamp when processing has completed
    output_ts = models.DateTimeField(auto_now_add=False)
