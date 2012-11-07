from darwintab.guitar.guitar import Guitar
from darwintab.score.scoreevent import Note
from pymei import XmlImport, XmlExport, MeiElement

class Guitarify:
    '''
    Class with functions to sanitize pitches of notes in an MEI file
    to be ones that can be played on a specific guitar
    '''

    def __init__(self, num_frets, tuning, capo):
        # create the guitar model to get the pitch range
        self.guitar = Guitar(num_frets, tuning, capo)
        self.mei_doc = None
        self.redistribute = False # whether or not to redistribute notes

    def sanitize_mei_file(self, mei_path, output_mei_path=None, prune=True):
        self.mei_doc = XmlImport.documentFromFile(str(mei_path))
        self._sanitize_mei(prune)

        if output_mei_path:
            XmlExport.meiDocumentToFile(self.mei_doc, str(output_mei_path))
        else:
            return XmlExport.meiDocumentToText(self.mei_doc)

    def sanitize_mei_str(self, mei_str, output_mei_path=None, prune=True):
        self.mei_doc = XmlImport.documentFromText(mei_str)
        self._sanitize_mei(prune)

        if output_mei_path:
            XmlExport.meiDocumentToFile(self.mei_doc, str(output_mei_path))
        else:
            return XmlExport.meiDocumentToText(self.mei_doc)
            
    def _sanitize_mei(self, prune):
        '''
        Remove (prune) or transpose notes in the mei document that are unable to
        be performed on the guitar.
        '''

        lb_pitch, ub_pitch = self.guitar.get_pitch_range()

        notes = self.mei_doc.getElementsByName('note')
        for mei_n in notes[:]:
            pname = str(mei_n.getAttribute('pname').value)
            oct = int(mei_n.getAttribute('oct').value)
            n = Note(pname, oct)

            # make sure pitch is within the pitch range of the guitar
            if n < lb_pitch:
                if prune:
                    self._remove_note(mei_n)
                else:
                    # attempt to transpose pitch
                    candidate_note = Note(pname, oct)
                    # jump by octave
                    step = 12
                    while candidate_note < lb_pitch:
                        candidate_note += step
                        step += 12

                    if candidate_note <= ub_pitch:
                        mei_n.addAttribute('pname', str(candidate_note.pname))
                        mei_n.addAttribute('oct', str(candidate_note.oct))
                    else:
                        self._remove_note(mei_n)
            elif n > ub_pitch:
                if prune:
                    self._remove_note(mei_n)
                else:
                    # attempt to transpose pitch
                    candidate_note = Note(pname, oct)
                    # jump by octave
                    step = 12
                    while candidate_note > ub_pitch:
                        candidate_note -= step
                        step += 12

                    if candidate_note >= lb_pitch:
                        mei_n.addAttribute('pname', str(candidate_note.pname))
                        mei_n.addAttribute('oct', str(candidate_note.oct))
                    else:
                        self._remove_note(mei_n)

        if prune and self.redistribute:
            self._redistribute()

    def _remove_note(self, note):
        '''
        Remove a note from the MEI document
        '''

        note_container = note.getParent()
        note_container.removeChild(note)
        if note_container.getName() == 'chord':
            layer = note_container.getParent()
            notes_in_chord = note_container.getChildrenByName('note')
            if len(notes_in_chord) == 0:
                # this should never happen
                layer.removeChild(note_container)
                self.redistribute = True
            elif len(notes_in_chord) == 1:
                # there is only one note left, so it's no longer a chord
                layer.addChildBefore(note_container, notes_in_chord[0])
                layer.removeChild(note_container)
        else:
            self.redistribute = True

    def _redistribute(self):
        '''
        Redistribute notes in the measures to match the 4/4 time signature
        '''
        
        layers = self.mei_doc.getElementsByName('layer')
        note_events = []
        for l in layers:
            note_events.extend(l.getChildren())

        # remove all measures
        for m in self.mei_doc.getElementsByName('measure'):
            m.getParent().removeChild(m)
        
        section = self.mei_doc.getElementsByName('section')[0]
        score_def = self.mei_doc.getElementsByName('scoreDef')[0]
        meter_count = int(score_def.getAttribute('meter.count').value)

        # insert the note events again
        note_container = None
        for i, note_event in enumerate(note_events):
            if i % meter_count == 0:
                measure = MeiElement('measure')
                measure.addAttribute('n', str(int(i/meter_count + 1)))
                staff = MeiElement('staff')
                staff.addAttribute('n', '1')
                layer = MeiElement('layer')
                layer.addAttribute('n', '1')
                section.addChild(measure)
                measure.addChild(staff)
                staff.addChild(layer)
                note_container = layer

            note_container.addChild(note_event)
