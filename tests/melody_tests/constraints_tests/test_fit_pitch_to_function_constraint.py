import unittest

import math

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from melody.constraints.contextual_note import ContextualNote
from melody.constraints.fit_pitch_to_function_constraint import FitPitchToFunctionConstraint
from melody.solver.p_map import PMap
from structure.line import Line
from structure.note import Note
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.offset import Offset
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext
from melody.constraints.policy_context import PolicyContext

import logging
import sys


class TestFitPitchToFunctionConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sample(self):

        # index = min(enumerate(self.candidate_pitches), key=lambda x: abs(x[0] - self.function_value))[0]

        p = [(32, True), (25, True)]
        lll = min(enumerate(p), key=lambda x: abs(x[1][0]))
        index = lll[0]
        print('---v={0}'.format(index))

    def test_compute_simple_function_tone(self):
        print('--- test_compute_simple_function_tone ---')
        line = Line()

        f = GenericUnivariatePitchFunction(TestFitPitchToFunctionConstraint.sinasoidal, Position(0), Position(2))
        v_note = Note(DiatonicPitch.parse('A:4'), Duration(1, 32))
        line.pin(v_note, Offset(0))

        constraint, lower_policy_context = TestFitPitchToFunctionConstraint.build_simple_constraint(v_note, f,
                                                                                                    ModalityType.Major,
                                                                                                    'G', 'tV')
        p_map = PMap()
        p_map[v_note] = ContextualNote(lower_policy_context)

        results = constraint.values(p_map, v_note)
        assert results is not None
        assert len(results) == 1
        print(next(iter(results)).diatonic_pitch)
        assert 'C:4' == str(next(iter(results)).diatonic_pitch)

        v_note = Note(DiatonicPitch.parse('A:4'), Duration(1, 32))
        line.pin(v_note, Offset(1, 32))

        constraint, lower_policy_context = TestFitPitchToFunctionConstraint.build_simple_constraint(v_note, f,
                                                                                                    ModalityType.Major,
                                                                                                    'G', 'tV')
        p_map = PMap()
        p_map[v_note] = ContextualNote(lower_policy_context)

        results = constraint.values(p_map, v_note)
        assert results is not None
        assert len(results) == 1
        print(next(iter(results)).diatonic_pitch)
        assert 'E:4' == str(next(iter(results)).diatonic_pitch)

        p_map[v_note].note = next(iter(results))
        assert constraint.verify(p_map)

    def test_compute_with_minor_key(self):
        print('-- test_compute_with_minor_key ---')
        line = Line()

        f = GenericUnivariatePitchFunction(TestFitPitchToFunctionConstraint.sinasoidal, Position(0), Position(2))
        v_notes = [Note(DiatonicPitch.parse('A:4'), Duration(1, 16)) for _ in range(0, 33)]
        for i in range(0, 33):
            line.pin(v_notes[i], Offset(i, 16))

        constraint, lower_policy_context = \
            TestFitPitchToFunctionConstraint.build_simple_constraint(v_notes[0], f, ModalityType.NaturalMinor,
                                                                     'C', 'tV')
        constraints = list()
        constraints.append(constraint)
        for i in range(1, 33):
            c, _ = \
                TestFitPitchToFunctionConstraint.build_simple_constraint(v_notes[i], f, ModalityType.NaturalMinor,
                                                                         'C', 'tV')
            constraints.append(c)

        p_map = PMap()
        p_map[v_notes[0]] = ContextualNote(lower_policy_context)

        results = constraint.values(p_map, v_notes[0])
        assert results is not None
        assert len(results) == 1
        print(next(iter(results)).diatonic_pitch)
        assert 'C:4' == str(next(iter(results)).diatonic_pitch)

        result_pitches = []
        for i in range(0, 33):
            p_map = PMap()
            p_map[v_notes[i]] = ContextualNote(lower_policy_context)
            results = constraints[i].values(p_map, v_notes[i])
            result_pitches.append(next(iter(results)).diatonic_pitch)

        assert len(result_pitches) == 33
        for i in range(0, 33):
            print('[{0}] {1}'.format(i, str(result_pitches[i])))

        # checks = ['C:4', 'Ab:4', 'D:5', 'F:5', 'G:5', 'F:5', 'D:5', 'Ab:4', 'C:4']
        checks = ['C:4', 'G:4', 'D:5', 'F:5', 'G:5', 'F:5', 'D:5', 'G:4', 'C:4']
        for i in range(0, len(checks)):
            assert checks[i] == str(result_pitches[i])

    BASE = DiatonicPitch.parse('C:4').chromatic_distance

    @staticmethod
    def sinasoidal(v):
        return TestFitPitchToFunctionConstraint.BASE + 19 * math.sin(2 * math.pi * v)

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)

    @staticmethod
    def build_simple_constraint(v_note, f, modality_type, key_str, chord_str):
        lower_policy_context = TestFitPitchToFunctionConstraint.policy_creator(modality_type, DiatonicTone(key_str),
                                                                               chord_str, 'C:2', 'C:8')

        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))

        return FitPitchToFunctionConstraint(v_note, f, tempo_seq, ts_seq), lower_policy_context

    if __name__ == "__main__":
        unittest.main()
