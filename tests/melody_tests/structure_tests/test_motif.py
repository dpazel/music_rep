import unittest

import logging
import sys

from melody.constraints.equal_pitch_constraint import EqualPitchConstraint
from melody.constraints.not_equal_pitch_constraint import NotEqualPitchConstraint
from melody.structure.motif import Motif
from structure.line import Line
from structure.beam import Beam
from structure.note import Note
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch

from timemodel.duration import Duration


class TestMotif(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_motif(self):
        s = Beam()
        s.append(Note(DiatonicPitch.parse('C:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('D:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('E:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('F#:4'), Duration(1, 8)))
        notes = s.get_all_notes()

        c = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        m = Motif(s, c, 'A')
        actors = m.actors

        assert 'A' == m.name
        assert len(actors) == len(notes)

        cc = m.constraints
        assert len(cc) == len(c)

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

        print(m)

        cs = Beam()
        first_note = Note(DiatonicPitch.parse('C:3'), Duration(1, 8))
        cs.append(first_note)
        cs.append(Note(DiatonicPitch.parse('D:3'), Duration(1, 8)))
        cs.append(Note(DiatonicPitch.parse('E:3'), Duration(1, 8)))
        cs.append(Note(DiatonicPitch.parse('F#:3'), Duration(1, 8)))

        c_motif = m.copy_to(first_note)
        c_actors = c_motif.actors

        assert 'A' == c_motif.name
        assert len(c_actors) == len(notes)

        ccc = c_motif.constraints
        assert len(ccc) == len(c)

        assert isinstance(ccc[0], EqualPitchConstraint)
        ccc_a = ccc[0].actors
        assert len(ccc_a) == 2
        assert ccc_a[0] == c_actors[0]
        assert ccc_a[1] == c_actors[2]

        assert isinstance(ccc[1], NotEqualPitchConstraint)
        ccc_b = ccc[1].actors
        assert len(ccc_a) == 2
        assert ccc_b[0] == c_actors[1]
        assert ccc_b[1] == c_actors[3]
        assert 'F#:3' == str(c_actors[3].diatonic_pitch)

        print(c_motif)

    def test_richer_structure(self):
        line = Line()
        s = Beam()
        s.append(Note(DiatonicPitch.parse('C:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('D:4'), Duration(1, 8)))
        line.pin(s)

        q1 = Note(DiatonicPitch.parse('E:4'), Duration(1, 4))
        line.pin(q1, Offset(1, 4))
        q2 = Note(DiatonicPitch.parse('F#:4'), Duration(1, 4))
        line.pin(q2, Offset(1, 2))

        cs = Beam()
        first_note = Note(DiatonicPitch.parse('C:3'), Duration(1, 8))
        cs.append(first_note)
        cs.append(Note(DiatonicPitch.parse('D:3'), Duration(1, 8)))
        line.pin(cs, Offset(2))

        cq1 = Note(DiatonicPitch.parse('E:3'), Duration(1, 4))
        line.pin(cq1, Offset(9, 4))
        cq2 = Note(DiatonicPitch.parse('F#:3'), Duration(1, 4))
        line.pin(cq2, Offset(5, 2))

        notes = line.get_all_notes()

        c = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        m = Motif([s, q1, q2], c, 'A')
        print(m)

        actors = m.actors

        assert 'A' == m.name
        assert len(actors) == 4

        cc = m.constraints
        assert len(cc) == len(c)

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

        c_motif = m.copy_to(first_note)
        assert c_motif is not None
        c_actors = c_motif.actors

        assert 'A' == c_motif.name
        assert len(c_actors) == 4

        ccc = c_motif.constraints
        assert len(ccc) == len(c)

        assert isinstance(ccc[0], EqualPitchConstraint)
        ccc_a = ccc[0].actors
        assert len(ccc_a) == 2
        assert ccc_a[0] == c_actors[0]
        assert ccc_a[1] == c_actors[2]

        assert isinstance(ccc[1], NotEqualPitchConstraint)
        ccc_b = ccc[1].actors
        assert len(ccc_a) == 2
        assert ccc_b[0] == c_actors[1]
        assert ccc_b[1] == c_actors[3]
        assert 'F#:3' == str(c_actors[3].diatonic_pitch)

        print(c_motif)

    def test_motif_book_example(self):

        s = Beam()
        s.append(Note(DiatonicPitch.parse('C:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('D:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('E:4'), Duration(1, 8)))
        s.append(Note(DiatonicPitch.parse('F#:4'), Duration(1, 8)))
        notes = s.get_all_notes()

        c = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        m = Motif(s, c, 'A')
        cs = Beam()

        cs.append(Note(DiatonicPitch.parse('C:3'), Duration(1, 8)))
        cs.append(Note(DiatonicPitch.parse('D:3'), Duration(1, 8)))
        cs.append(Note(DiatonicPitch.parse('E:3'), Duration(1, 8)))
        cs.append(Note(DiatonicPitch.parse('F#:3'), Duration(1, 8)))

        c_motif = m.copy_to(cs.get_all_notes()[0])

        assert 'A' == c_motif.name
        assert len(c_motif.actors) == len(notes)
        assert len(c_motif.constraints) == len(c)

        assert isinstance(c_motif.constraints[0], EqualPitchConstraint)
        assert c_motif.constraints[0].actors[0] == c_motif.actors[0]
        assert c_motif.constraints[0].actors[1] == c_motif.actors[2]

        assert isinstance(c_motif.constraints[1], NotEqualPitchConstraint)
        assert c_motif.constraints[1].actors[0] == c_motif.actors[1]
        assert c_motif.constraints[1].actors[1] == c_motif.actors[3]


