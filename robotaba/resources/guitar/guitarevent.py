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

class GuitarEvent(object):

    def __init__(self, **kwargs):
        # optional timing information
        # timestamp start
        self.ts_start = kwargs.get('ts_start')
        # beat start
        self.beat_start = kwargs.get('beat_start')
        # beat duration
        self.dur = kwargs.get('dur')

class Strum(GuitarEvent):

    def __init__(self, plucks, **kwargs):
        '''
        kwargs is for passing in timing information
        '''
        super(Strum, self).__init__(**kwargs)

        self._set_plucks(plucks)

    def add_pluck(self, pluck):
        self._plucks.append(pluck)

    def del_pluck(self, string, fret):
        pluck = Pluck(string, fret)
        self._plucks = filter(lambda n: n != pluck, self.plucks)

    def _get_plucks(self):
        return self._plucks

    def _set_plucks(self, plucks):
        self._plucks = plucks

    plucks = property(_get_plucks, _set_plucks)

    def distance(self, other):
        '''
        Get the distance between this strum and another pluck or strum
        '''

        if isinstance(other, Strum):
            max_fret = max([p.fret for p in self.plucks])
            other_max_fret = max([p.fret for p in other.plucks])
            if max_fret == 0 or other_max_fret == 0:
                distance = 0
            else:
                distance = max_fret - other_max_fret
        elif isinstance(other, Pluck):
            frets = [p.fret for p in self.plucks]
            min_fret = min(frets)
            max_fret = max(frets)

            if other.fret <= min_fret:
                distance = min_fret - other.fret
            elif other.fret >= max_fret:
                distance = other.fret - max_fret
            else:
                distance = other.fret - (max_fret+min_fret)/2
        else:
            raise ValueError('Must compare to a strum or pluck')

        return abs(distance)

    def is_open(self):
        '''
        True if the strum is all open strings
        '''
        return all([p.fret == 0 for p in self._plucks])

    def __str__(self):
        return '<strum: %s>' % ', '.join([p.__str__() for p in self._plucks])

    def __repr__(self):
        return self.__str__()

class Pluck(GuitarEvent):

    def __init__(self, string, fret, **kwargs):
        super(Pluck, self).__init__(**kwargs)

        self.string = string
        self.fret = fret

    def distance(self, other):
        '''
        Get the distance between this pluck with a pluck or strum
        '''

        if isinstance(other, Pluck):
            if self.fret == 0 or other.fret == 0:
                distance = 0
            else:
                distance = self.fret - other.fret
        elif isinstance(other, Strum):
            other_frets = [p.fret for p in other.plucks]
            min_other_frets = min(other_frets)
            max_other_frets = max(other_frets)

            if self.fret <= min_other_frets:
                distance = min_other_frets - self.fret
            elif self.fret >= max_other_frets:
                distance = self.fret - max_other_frets
            else:
                distance = self.fret - (min_other_frets + max_other_frets)/2
        else:
            raise ValueError('Must compare to a pluck or strum')

        return abs(distance)

    def is_open(self):
        '''
        True if the pluck is an open string
        '''
        return self.fret == 0

    def __eq__(self, other_pluck):
        return self.string == other_pluck.string and self.fret == other_pluck.fret

    def __str__(self):
        return '<pluck: string: %d, fret: %d>' % (self.string+1, self.fret)

    def __repr__(self):
        return self.__str__()
