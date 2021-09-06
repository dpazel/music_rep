import unittest

import logging
import sys

from melody.constraints.equal_pitch_constraint import EqualPitchConstraint
from melody.constraints.not_equal_pitch_constraint import NotEqualPitchConstraint
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from melody.structure.melodic_form import MelodicForm
from melody.structure.motif import Motif
from melody.structure.phrase import Phrase
from structure.line import Line
from structure.note import Note
from timemodel.offset import Offset
from tonalmodel.diatonic_pitch import DiatonicPitch

from timemodel.duration import Duration

from fractions import Fraction


class TestMelodicForm(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_form(self):
        line = Line()

        notes = [
            Note(DiatonicPitch.parse('C:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('D:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('E:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('F:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('G:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('A:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('B:4'), Duration(1, 8)),
            Note(DiatonicPitch.parse('C:4'), Duration(1, 4)),

            Note(DiatonicPitch.parse('C:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('D:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('E:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('F:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('G:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('A:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('B:3'), Duration(1, 8)),
            Note(DiatonicPitch.parse('C:3'), Duration(1, 4)),
        ]

        f = Fraction(0)
        for n in notes:
            line.pin(n, Offset(f))
            f = f + n.duration.duration

        ca = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        cb = [
            NotEqualPitchConstraint([notes[4], notes[5]]),
            EqualPitchConstraint([notes[6], notes[7]])
        ]

        a = Motif([notes[0], notes[1], notes[2], notes[3]], ca, 'A')
        b = Motif([notes[4], notes[5], notes[6], notes[7]], cb, 'B')

        p1_constraints = [
            EqualPitchConstraint([notes[4], notes[5]]),
        ]
        p1 = Phrase([notes[2], notes[3], notes[4], notes[5]], p1_constraints, 'P1')

        mf_constraints = [
            EqualPitchConstraint([notes[2], notes[5]]),
        ]

        mf = MelodicForm([a, b], [p1], mf_constraints, 'MF1')
        actors = mf.actors
        assert actors is not None
        assert len(actors) == 8
        assert actors[0] == notes[0]

        motifs = mf.motifs
        assert motifs is not None
        assert len(motifs) == 2
        assert motifs[0].name == 'A'
        assert motifs[1].name == 'B'

        p_constraints = mf.phrase_constraints
        assert p_constraints is not None
        assert len(p_constraints) == 1
        assert type(p_constraints[0]) == EqualPitchConstraint

        p_actors = mf.phrase_actors
        assert p_actors is not None
        assert len(p_actors) == 4

        mf1 = mf.copy_to(notes[8])
        assert mf1 is not None
        actors = mf1.actors
        assert actors is not None
        assert len(actors) == 8
        assert actors[0] == notes[8]

        motifs = mf1.motifs
        assert motifs is not None
        assert len(motifs) == 2
        assert motifs[0].name == 'A'
        assert motifs[1].name == 'B'

        p_constraints = mf1.phrase_constraints
        assert p_constraints is not None
        assert len(p_constraints) == 1
        assert type(p_constraints[0]) == EqualPitchConstraint

        p_actors = mf1.phrase_actors
        assert p_actors is not None
        assert len(p_actors) == 4

        phs = mf1.phrases
        assert phs is not None
        assert len(phs) == 1
        assert phs[0].actors[0] == notes[10]

    def test_book_example(self):
        line_str = '{<C-Major: I> iC:4 D E F G A B qC iC:3 D E F G A B qC}'
        lge = LineGrammarExecutor()
        target_line, _ = lge.parse(line_str)
        notes = target_line.get_all_notes()

        ca = [
            EqualPitchConstraint([notes[0], notes[2]]),
            NotEqualPitchConstraint([notes[1], notes[3]])
        ]

        cb = [
            NotEqualPitchConstraint([notes[4], notes[5]]),
            EqualPitchConstraint([notes[6], notes[7]])
        ]

        a = Motif([notes[0], notes[1], notes[2], notes[3]], ca, 'A')
        b = Motif([notes[4], notes[5], notes[6], notes[7]], cb, 'B')

        phrase_constraints = [
            EqualPitchConstraint([notes[4], notes[5]]),
        ]
        phrase = Phrase([notes[2], notes[3], notes[4], notes[5]], phrase_constraints, 'P1')

        mf_constraints = [
            EqualPitchConstraint([notes[2], notes[5]]),
        ]

        mf = MelodicForm([a, b], [phrase], mf_constraints, 'MF1')
        print('[{0}]'.format(','.join([str(n.diatonic_pitch) for n in mf.actors])))


        mf_dup = mf.copy_to(notes[8])
        print('[{0}]'.format(','.join([str(n.diatonic_pitch) for n in mf_dup.actors])))

