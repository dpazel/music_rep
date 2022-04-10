import unittest
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext
from melody.constraints.policy_context import PolicyContext
from melody.constraints.contextual_note import ContextualNote
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.pitch_range import PitchRange
from structure.note import Note
from melody.constraints.fixed_tone_constraint import FixedToneConstraint

import logging
import sys


class TestFixedToneConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_fixed_tone(self):
        logging.debug('Start test_simple_fixed_tone')
        note = Note(DiatonicPitch.parse("C:5"), Duration(1, 4))
        lower_policy_context = TestFixedToneConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
                                                                      'C:2', 'C:8')

        policy = FixedToneConstraint(note, DiatonicToneCache.get_tone("Ab"))

        lower_contextual_note = ContextualNote(lower_policy_context)
        m = dict([(note, lower_contextual_note)])

        v_result = policy.values(m, note)

        assert len(v_result) == 6
        for note in v_result:
            print('test_simple_fixed_tone pitch = {0}'.format(note.diatonic_pitch))

            assert note.diatonic_pitch.diatonic_tone == DiatonicToneCache.get_tone('Ab')
            assert note.base_duration == Duration(1, 4)

            lower_contextual_note.note = note

            result = policy.verify(m)
            assert result is True

            lower_contextual_note.note = None

        logging.debug('End test_simple_fixed_tone')

    def test_enharmonic_fixed_tone(self):
        logging.debug('Start test_enharmonic_fixed_tone')
        note = Note(DiatonicPitch.parse("C:5"), Duration(1, 4))

        policy = FixedToneConstraint(note, DiatonicToneCache.get_tone("Bbb"))

        lower_policy_context = TestFixedToneConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                      'C:2', 'C:8')
        lower_contextual_note = ContextualNote(lower_policy_context)
        m = dict([(note, lower_contextual_note)])

        v_result = policy.values(m, note)

        assert len(v_result) == 6
        for note in v_result:
            print('test_simple_fixed_tone pitch = {0}'.format(note.diatonic_pitch))

            assert note.diatonic_pitch.diatonic_tone == DiatonicToneCache.get_tone('A')
            assert note.base_duration == Duration(1, 4)

            lower_contextual_note.note = note

            result = policy.verify(m)
            assert result is True

            lower_contextual_note.note = None

        logging.debug('End test_enharmonic_fixed_tone')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
