from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings

from robotaba.models import Audio, MetaMusic
from robotaba.models import Guitar as GuitarModel

from musicxmlmeiconversion.musicxmltomei import MusicXMLtoMei
from ztranscribe.polytrans import PolyTrans

from pymei import XmlImport, XmlExport, MeiElement

import os

'''
Entities
'''
class MeiPitch(models.Model):
    mei_file = models.FileField(upload_to='mei/pitch')
    fk_mid = models.ForeignKey(MetaMusic)
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
    fk_guitar = models.ForeignKey(GuitarModel, null=True)
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
        t = PolyTrans()
        note_events = t.transcribe(input_audio_path)

        if self.fk_guitar is not None:
            t.guitarify(note_events, self.fk_guitar.num_frets, self.fk_guitar.tuning, self.fk_guitar.capo)

        mei_str = t.write_mei(note_events)
        mei_str = self._appendMetaData(mei_str)

        # save the mei to the output file
        file_contents = ContentFile(mei_str)
        pmei = MeiPitch(fk_mid=self.fk_audio.fk_mid)
        pmei.mei_file.save(filename, file_contents, save=True)

        # attach the tab to the Tabulate object
        self.fk_pmei = pmei
        # Note that saving also updates self.output_ts to clock out the
        # analysis time
        self.save()

    def _appendMetaData(self, mei_str):
        '''
        Append meta data for the musical work
        '''

        mei_doc = XmlImport.documentFromText(mei_str)

        mei = mei_doc.getRootElement()
        mei_head = MeiElement('meiHead')
        music = mei.getChildrenByName('music')[0]
        
        file_desc = MeiElement('fileDesc')

        # title
        title_stmt = MeiElement('titleStmt')
        title = MeiElement('title')
        title.setValue(str(self.fk_audio.fk_mid.title))

        # contributers
        resp_stmt = MeiElement('respStmt')
        pers_name_artist = MeiElement('persName')
        pers_name_artist.addAttribute('role', 'artist')
        pers_name_artist.setValue(str(self.fk_audio.fk_mid.artist))
        pers_name_tabber = MeiElement('persName')
        pers_name_tabber.addAttribute('role', 'tabber')
        pers_name_tabber.setValue(str(self.fk_audio.fk_mid.copyright))

        # encoding information
        encoding_desc = MeiElement('encodingDesc')
        app_info = MeiElement('appInfo')
        application = MeiElement('application')
        application.setValue('Robotaba')

        mei_head.addChild(file_desc)
        file_desc.addChild(title_stmt)
        title_stmt.addChild(title)
        title_stmt.addChild(resp_stmt)
        resp_stmt.addChild(pers_name_artist)
        resp_stmt.addChild(pers_name_tabber)
        title_stmt.addChild(encoding_desc)
        encoding_desc.addChild(app_info)
        app_info.addChild(application)

        # attach mei metadata to the document
        mei.addChildBefore(music, mei_head)

        return XmlExport.meiDocumentToText(mei_doc)
