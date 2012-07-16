import os
import re
from pymei import XmlImport

def meitoalphatex(mei_path):
    alphatex = ''

    # read in the mei document
    meidoc = XmlImport.read(mei_path)
    mei = meidoc.getRootElement()

    ###########################
    #         MetaData        #
    ###########################
    title = mei.getDescendantsByName('title')
    if len(title):
        tex_title = "\\title \"%s\"\n" % title[0].getValue()
        alphatex += tex_title

    pers_name = mei.getDescendantsByName('persName')
    if len(pers_name):
        for p in pers_name:
            role = p.getAttribute('role').value
            if role == 'artist':
                tex_artist = "\\artist \"%s\"\n" % p.getValue()
                alphatex += tex_artist
            elif role == 'tabber':
                tex_copywrite = "\\copyright \"%s\"\n" % p.getValue()
                alphatex += tex_copywrite
            elif role == 'lyricist':
                tex_words = "\\words \"%s\"\n" % p.getValue()
                alphatex += tex_words

    # guitar tuning
    pnames = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    staff_def = mei.getDescendantsByName('staffDef')
    if len(staff_def) and staff_def[0].hasAttribute('tab.strings'):
        strings = staff_def[0].getAttribute('tab.strings').value.split(' ')
        # in alpha tab the ordering is backwards
        strings.reverse()
        if len(strings) != 6:
            raise ValueError('Invalid number of strings: should be 6')

        # convert pitch names to those used in alphatab (flats vs. sharps)
        for i in range(len(strings)):
            pattern = re.compile('^([a-zA-z][#s])')
            match = pattern.match(strings[i])
            if match:
                mei_pname = match.group()
                alpha_pname = pnames[pnames.index(mei_pname[0])+1 % len(pnames)] + 'b'
                oct = strings[i][-1]
                # replace string
                strings[i] = alpha_pname + oct

        alphatex += '\\tuning %s\n' % ' '.join(strings)

    # set midi instrument to play the tab with
    # 27 is Electric Guitar Clean
    alphatex += '\\instrument 27\n'
        
    # in alphatex the metadata and body are separated by a period character
    alphatex += '.\n'

    ###########################
    #           Body          #
    ###########################

    measures = mei.getDescendantsByName('measure')
    alpha_measures = []
    for m in measures:
        measure_events = []
        # only parse first staff (instrument), the instrument display 
        staff = m.getChildrenByName('staff')[0]
        # only parse first layer (assume only one voice)
        layer = staff.getChildrenByName('layer')[0]
        score_events = layer.getChildren()
        for e in score_events:
            if e.getName() == 'chord':
                # get notes in this chord
                notes = e.getChildrenByName('note')
                alpha_notes = [n.getAttribute('tab.fret').value + '.' + n.getAttribute('tab.string').value for n in notes]
                alpha_chord = '(' + ' '.join(alpha_notes) + ')'
                measure_events.append(alpha_chord)
            elif e.getName() == 'note':
                alpha_note = e.getAttribute('tab.fret').value + '.' + e.getAttribute('tab.string').value
                measure_events.append(alpha_note)

        alpha_measures.append(' '.join(measure_events))

    alphatex += ' |\n'.join(alpha_measures)

    return alphatex
