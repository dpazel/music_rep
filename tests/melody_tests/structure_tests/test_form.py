import unittest

import logging
import sys

from melody.constraints.equal_pitch_constraint import EqualPitchConstraint
from melody.constraints.not_equal_pitch_constraint import NotEqualPitchConstraint
from melody.constraints.relative_scalar_step_constraint import RelativeScalarStepConstraint
from melody.structure.motif import Motif
from melody.structure.form import Form
from structure.line import Line
from structure.beam import Beam
from structure.note import Note
from structure.tuplet import Tuplet
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.range import Range

from timemodel.duration import Duration


class TestForm(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_form(self):
        line = Line()
        s = Beam()
        s.append(Note(DiatonicPitch.parse('C:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('D:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('E:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('F#:4'), Duration(1, 8)))
        line.pin(s)
        notes = s.get_all_notes()

        c = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        a = Motif(s, c, 'A')

        s1 = [
           Note(DiatonicPitch(4, 'c'), Duration(1, 8)),
           Note(DiatonicPitch(4, 'd'), Duration(1, 8)),
           Note(DiatonicPitch(4, 'e'), Duration(1, 8)),
        ]
        tuplet = Tuplet(Duration(1, 8), 2, s1)
        line.pin(tuplet, Offset(1, 2))
        notes = tuplet.get_all_notes()

        c1 = [
            EqualPitchConstraint([notes[0], notes[2]]),
            RelativeScalarStepConstraint(notes[1], notes[2], -2, 2)
        ]

        b = Motif(tuplet, c1, 'B')

        f = Form([a, b])
        print(f)

        constraints = [
            EqualPitchConstraint([a.actors[0], b.actors[1]])
        ]

        # Ensure a, b cloned for reliability - see comment in Form.
        ff = Form([a, b], constraints)
        print(ff)

        constr = ff.external_constraints
        assert len(constr) == 1

        actors = ff.actors
        assert len(actors) == 7

        assert isinstance(constr[0], EqualPitchConstraint)
        assert constr[0].actors[0] == actors[0]
        assert constr[0].actors[1] == actors[4 + 1]

        all_constr = ff.constraints
        assert len(all_constr) == 5

        # Add more notes to clone ff as:
        s3 = Beam()
        first_note = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        s3.append(first_note)
        s3.append(Note(DiatonicPitch.parse('D:5'), Duration(1, 8)))
        s3.append(Note(DiatonicPitch.parse('E:5'), Duration(1, 8)))
        s3.append(Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))
        line.pin(s3, Offset(3))

        s2 = [
           Note(DiatonicPitch(5, 'c'), Duration(1, 8)),
           Note(DiatonicPitch(5, 'd'), Duration(1, 8)),
           Note(DiatonicPitch(5, 'e'), Duration(1, 8)),
        ]
        tuplet1 = Tuplet(Duration(1, 8), 2, s2)
        line.pin(tuplet1, Offset(7, 2))

        fff = ff.copy_to(first_note)
        assert fff is not None
        print(fff)

        constr = fff.external_constraints
        assert len(constr) == 1
        assert len(fff.constraints) == 5

        actors = fff.actors
        assert len(actors) == 7

        assert isinstance(constr[0], EqualPitchConstraint)
        assert constr[0].actors[0] == actors[0]
        assert constr[0].actors[1] == actors[4 + 1]

        all_constr = fff.constraints
        assert len(all_constr) == 5
