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

from django.db import models

class MetaMusic(models.Model):
    artist = models.CharField(max_length=50, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    copyright = models.CharField(max_length=50, null=True)

class Audio(models.Model):
    fk_mid = models.ForeignKey(MetaMusic)
    # timestamp of when the audio was uploaded to the server
    upload_ts = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='audio')

    def __unicode__(self):
        return str(self.id) + ": " + self.piece_name

class Guitar(models.Model):
    num_frets = models.IntegerField(default=24)
    tuning = models.CharField(max_length=25, default='standard')
    capo = models.IntegerField(default=0)
