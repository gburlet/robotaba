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

from darwintab.score.scoreevent import Note
from guitarevent import Pluck

class InvalidTuning(Exception):
    '''
    Custom exception that is raised when an invalid
    guitar tuning has been specified
    '''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Guitar(object):

    tunings = {
        'standard': [Note('E', 4), Note('B', 3), Note('G', 3), Note('D', 3), Note('A', 2), Note('E', 2)],
        'dropped_d': [Note('E', 4), Note('B', 3), Note('G', 3), Note('D', 3), Note('A', 2), Note('D', 2)],
        'dropped_c': [Note('D', 4), Note('A', 3), Note('F', 3), Note('C', 3), Note('G', 2), Note('C', 2)]
    }

    def __init__(self, num_frets=24, tuning='standard', capo=0):
        self.num_frets = num_frets

        self.tuning = tuning
        if tuning in Guitar.tunings:
            # first look up shorthand reference to tuning, e.g., 'standard'
            self.strings = Guitar.tunings[self.tuning]
        elif len(tuning.split(' ')) == 6:
            # this may be a string specifying the tuning
            # from thinnest to thickest string
            self.strings = []
            for s in tuning.split(' '):
                # make sure this is a valid pitch/octave
                try:
                    oct = int(s[-1])
                    pname = s[:-1]
                    n = Note(pname, oct)
                    self.strings.append(n)
                except ValueError:
                    raise InvalidTuning('%s is not a valid tuning' % tuning)
        else:
            raise InvalidTuning('%s is not a valid tuning' % tuning)

        self.capo = capo

    def get_pitch_range(self):
        '''
        Calculate the pitch range of the guitar model using the number of frets,
        the tuning of the guitar, and the capo position.
        Returns a tuple of Note objects (lowerpitch, upperpitch)
        '''

        lb_pitch = self.strings[-1] + self.capo
        ub_pitch = self.strings[0] + self.num_frets

        return lb_pitch, ub_pitch

    def get_candidate_frets(self, note):
        '''
        Given a note, get all the candidate (string, fret) pairs
        where it could be played given the current guitar properties
        (number of strings, and tuning).
        '''

        candidates = []
        num_chroma = len(Note.pitch_classes)

        # get open string pitches with capo position
        open_strings = [n + self.capo for n in self.strings]

        for i, s in enumerate(open_strings):
            # calculate pitch difference from the open string note
            oct_diff = note.oct - s.oct
            pname_diff = Note.pitch_classes.index(note.pname) - Note.pitch_classes.index(s.pname)
            pitch_diff = pname_diff + num_chroma*oct_diff

            if pitch_diff >= 0 and pitch_diff <= self.num_frets:
                candidates.append(Pluck(i, pitch_diff))

        return candidates

    def get_note(self, string, fret):
        '''
        Given a string and fret, return the pitch name and octave
        of the note that would be produced in the current tuning.
        '''

        if fret < 0 or fret > self.num_frets:
            return None

        num_chroma = len(Note.pitch_classes)
        str_note = self.strings[string]
        oct_diff = int(fret/num_chroma)
        i_str_pname = Note.pitch_classes.index(str_note.pname)
        i_note_pname = (i_str_pname + fret) % num_chroma
        if i_note_pname < i_str_pname:
            oct_diff += 1

        pname = Note.pitch_classes[i_note_pname]
        oct = str_note.oct + oct_diff

        return Note(pname, oct)

    def __str__(self):
        return "<Guitar: %d frets, %s tuning, capo on fret %d>" % (self.num_frets, self.tuning, self.capo)

    def __repr__(self):
        return self.__str__()
