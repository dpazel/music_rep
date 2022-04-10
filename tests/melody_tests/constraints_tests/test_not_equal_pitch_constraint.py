import unittest

from melody.solver.p_map import PMap
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext
from melody.constraints.policy_context import PolicyContext
from melody.constraints.contextual_note import ContextualNote
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.pitch_range import PitchRange
from structure.note import Note
from melody.constraints.not_equal_pitch_constraint import NotEqualPitchConstraint

import logging
import sys


class TestNotEqualPitchConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_not_equal(self):
        logging.debug('Start test_is_not_equal')
        note1 = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        lower_policy_context = TestNotEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                          'C:2', 'C:8')
        lower_context_note_a = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:6'),
                                                                         Duration(1, 8)))
        p_map = PMap()
        p_map[note1] = lower_context_note_a

        other_source = []
        for tone in ['B:5', 'D:5', 'E:5']:
            n = Note(DiatonicPitch.parse(tone), Duration(1, 8))
            lower_context_note = ContextualNote(lower_policy_context)
            p_map[n] = lower_context_note
            other_source.append(n)

        params = list([note1])
        params.extend(other_source)
        policy = NotEqualPitchConstraint(params)

        for c_note in p_map.unassigned_actors(policy):
            print(c_note)
            v_result = policy.values(p_map, c_note)
            assert v_result is not None

            assert DiatonicPitch.parse('F#:6') not in {n.diatonic_pitch for n in v_result}

        p_map[other_source[1]].note = Note(DiatonicPitch.parse('E:6'), Duration(1, 8))
        for c_note in p_map.unassigned_actors(policy):
            print(c_note)
            v_result = policy.values(p_map, c_note)
            assert v_result is not None
            ret_pitches = {n.diatonic_pitch for n in v_result}
            assert len(ret_pitches.intersection({DiatonicPitch.parse('F#:6'), DiatonicPitch.parse('E:6')})) == 0

        assert policy.verify(p_map) is False

        p_map[other_source[2]].note = Note(DiatonicPitch.parse('F#:6'), Duration(1, 8))
        assert policy.verify(p_map) is False

        p_map[other_source[0]].note = Note(DiatonicPitch.parse('D:6'), Duration(1, 8))
        assert policy.verify(p_map) is False

        p_map[other_source[2]].note = Note(DiatonicPitch.parse('A:6'), Duration(1, 8))
        assert policy.verify(p_map) is True

        logging.debug('End test_is_not_equal')
        return

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
