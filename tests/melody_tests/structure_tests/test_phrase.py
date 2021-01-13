import unittest

import logging
import sys

from melody.constraints.equal_pitch_constraint import EqualPitchConstraint
from melody.constraints.not_equal_pitch_constraint import NotEqualPitchConstraint
from melody.structure.phrase import Phrase
from structure.line import Line
from structure.note import Note
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch

from timemodel.duration import Duration


class TestPhrase(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_motif(self):
        line = Line()
        notes = [
            Note(DiatonicPitch.parse('C:4'), Duration(1, 4)),
            Note(DiatonicPitch.parse('D:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('E:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('F#:4'), Duration(1, 2)),
        ]

        line.pin(notes)

        c = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        nm = Phrase(notes, c, 'B')

        print(nm)

        assert nm.name == 'B'
        actors = nm.actors

        assert len(actors) == 4

        cc = nm.constraints
        assert isinstance(cc[0], EqualPitchConstraint)
        cc_a = cc[0].actors
        assert len(cc_a) == 2
        assert cc_a[0] == actors[0]
        assert cc_a[1] == actors[2]

        assert isinstance(cc[1], NotEqualPitchConstraint)
        cc_b = cc[1].actors
        assert len(cc_a) == 2
        assert cc_b[0] == actors[1]
        assert cc_b[1] == actors[3]
        assert 'F#:4' == str(actors[3].diatonic_pitch)

        # More notes for copy to:
        first_note = Note(DiatonicPitch.parse('C:3'), Duration(1, 4))
        notes1 = [
            first_note,
            Note(DiatonicPitch.parse('D:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('E:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('F#:3'), Duration(1, 2)),
        ]
        line.pin(notes1, Offset(2))

        nm_clone = nm.copy_to(first_note)
        assert isinstance(nm_clone, Phrase)
        assert nm_clone.name == 'B'
        c_actors = nm_clone.actors

        assert len(c_actors) == 4
        assert 'F#:3' == str(c_actors[3].diatonic_pitch)
