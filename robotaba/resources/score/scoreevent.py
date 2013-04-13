'''
Copyright (c) 2012 Gregory Burlet

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

from __future__ import division

class ScoreEvent(object):

    def __init__(self, **kwargs):
        # optional timing information
        # onset timestamp
        self.onset_ts = kwargs.get('onset_ts')
        # offset timestamp
        self.offset_ts = kwargs.get('offset_ts')
        # beat start
        self.beat_start = kwargs.get('beat_start')
        # beat duration
        self.dur = kwargs.get('dur')

class Chord(ScoreEvent):

    def __init__(self, notes=[], **kwargs):
        '''
        Creates a chord

        PARAMETERS
        ----------
        notes {list}: optional list of notes to put in the chord container
        kwargs: {beat_start (int), dur (int)}
        '''

        super(Chord, self).__init__(**kwargs)

        self._set_notes(notes)

    def add_note(self, note):
        self._notes.append(note)

    def del_note(self, pname, oct):
        note = Note(pname, oct)
        self._notes = filter(lambda n: n != note, self._notes)

    def _get_notes(self):
        return self._notes

    def _set_notes(self, notes):
        self._notes = notes

    notes = property(_get_notes, _set_notes)

    def __str__(self):
        return "<chord: %s>" % ", ".join([n.__str__() for n in self._notes])

    def __repr__(self):
        return self.__str__()

class Note(ScoreEvent):

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, pname, oct, id=None, **kwargs):
        '''
        id {String}: id of the mei element this note originates from
            default is None (may or may not be tied to an MeiElement)
        pname {String}: pitch name
        oct {Integer}: octave
        kwargs is for passing in timing information
        '''
        super(Note, self).__init__(**kwargs)

        # pitch class
        if pname.upper() in Note.pitch_classes:
            self.pname = pname.upper()
        else:
            raise ValueError('Invalid pitch name')

        # octave
        self.oct = oct

        self.id = id

    def toMidi(self):
        '''
        Convert the pitch name and octave to a MIDI note number
        between 0 and 127
        '''

        p_ind = Note.pitch_classes.index(self.pname)
        num_chroma = len(Note.pitch_classes)

        midi = (self.oct-1)*num_chroma + 24 + p_ind
        
        if midi >= 0 and midi <= 127:
            return midi
        else:
            return None

    def __add__(self, step):
        '''
        Add an integer number of semitones to the note
        '''

        num_chroma = len(Note.pitch_classes)
        step_up = True
        if step < 0:
            step_up = False

        note = Note(self.pname, self.oct)
        p_ind = Note.pitch_classes.index(self.pname)
        new_p_ind = (p_ind + step) % num_chroma

        note.pname = Note.pitch_classes[new_p_ind]
        oct_diff = int(step / 12)

        note.oct = self.oct + oct_diff

        if oct_diff == 0:
            if step_up:
                if new_p_ind >= 0 and new_p_ind < p_ind:
                    note.oct += 1
            else:
                if new_p_ind > p_ind and new_p_ind < num_chroma:
                    note.oct -= 1

        return note

    def __sub__(self, step):
        '''
        Subtract an integer number of semitones to the note
        '''

        return self.__add__(-step)

    def __eq__(self, other_note):
        return self.pname == other_note.pname and self.oct == other_note.oct

    def __lt__(self, other_note):
        return self.oct < other_note.oct or (self.oct == other_note.oct and Note.pitch_classes.index(self.pname) < Note.pitch_classes.index(other_note.pname))

    def __le__(self, other_note):
        return self.__lt__(other_note) or self.__eq__(other_note)

    def __gt__(self, other_note):
        return self.oct > other_note.oct or (self.oct == other_note.oct and Note.pitch_classes.index(self.pname) > Note.pitch_classes.index(other_note.pname))

    def __ge__(self, other_note):
        return self.__gt__(other_note) or self.__eq__(other_note)

    def __str__(self):
        return "<note: %s%d>" % (self.pname, self.oct)

    def __repr__(self):
        return self.__str__()
