import unittest

import logging
import sys

from harmoniccontext.harmonic_context import HarmonicContext
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from melody.constraints.contextual_note import ContextualNote
from melody.constraints.policy_context import PolicyContext
from melody.constraints.scalar_pitch_constraint import ScalarPitchConstraint
from structure.note import Note
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality


class TestScalarPitchConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_scalar(self):
        logging.debug('Start test_is_scalar')

        v_note = Note(DiatonicPitch.parse('F:5'), Duration(1, 4))

        lower_policy_context = TestScalarPitchConstraint.policy_creator(ModalityType.Major,
                                                                        DiatonicToneCache.get_tone('G'), 'tV',
                                                                        'G:5', 'G:7')

        lower_context_note = ContextualNote(lower_policy_context)

        parameter_map = dict([(v_note, lower_context_note)])

        policy = ScalarPitchConstraint(v_note)

        v_result = policy.values(parameter_map, v_note)

        tones = lower_policy_context.harmonic_context.tonality.annotation
        for note in v_result:
            print('test_is_scalar; note = {0}'.format(note))
            tone = note.diatonic_pitch.diatonic_tone
            octave = note.diatonic_pitch.octave
            assert tone in tones
            assert octave in range(5, 8)

        assert len(v_result) == 7 * 2 + 1

        for note in v_result:
            parameter_map[v_note].note = note
            assert policy.verify(parameter_map) is True
        logging.debug('End test_is_scalar')

    def test_is_scalar_with_roles(self):
        logging.debug('Start test_is_scalar_with_roles')

        v_note = Note(DiatonicPitch.parse('F:5'), Duration(1, 4))

        lower_policy_context = TestScalarPitchConstraint.policy_creator(ModalityType.Major,
                                                                        DiatonicToneCache.get_tone('G'), 'tV',
                                                                        'G:5', 'G:7')

        lower_context_note = ContextualNote(lower_policy_context)

        parameter_map = dict([(v_note, lower_context_note)])

        policy = ScalarPitchConstraint(v_note, [3, 5])

        v_result = policy.values(parameter_map, v_note)

        tones = list(lower_policy_context.harmonic_context.tonality.annotation)
        tones = tones[:-1]
        for note in v_result:
            print('test_is_scalar; note = {0}'.format(note))
            tone = note.diatonic_pitch.diatonic_tone
            octave = note.diatonic_pitch.octave
            assert tone in tones
            assert tones.index(tone) in [3, 5]
            assert octave in range(5, 8)

        assert len(v_result) == 2 * 2

        for note in v_result:
            parameter_map[v_note].note = note
            assert policy.verify(parameter_map) is True
        logging.debug('End test_is_scalar_with_roles')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
