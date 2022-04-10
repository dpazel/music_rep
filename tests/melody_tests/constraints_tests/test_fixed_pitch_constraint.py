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
from melody.constraints.fixed_pitch_constraint import FixedPitchConstraint

import logging
import sys


class TestFixedPitchConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_fixed_pitch(self):
        logging.debug('Start test_simple_fixed_pitch')
        policy_context = TestFixedPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
                                                                 'C:2', 'C:8')
        note = Note(DiatonicPitch.parse("C:5"), Duration(1, 4))

        policy = FixedPitchConstraint(note, DiatonicPitch.parse("A:5"))

        contextual_note = ContextualNote(policy_context)
        p_map = PMap()
        p_map[note] = contextual_note

        v_result = policy.values(p_map, note)
        result = next(iter(v_result))
        print('test_simple_fixed_pitch note = {0}'.format(result))

        assert result.diatonic_pitch == DiatonicPitch.parse("A:5")
        assert result.base_duration == Duration(1, 4)

        contextual_note.note = result

        result = policy.verify(p_map)
        assert result is True

        logging.debug('End test_simple_fixed_pitch')

    def test_scale_enharmonic_map(self):
        logging.debug('Start test_scale_enharmonic_map')

        note = Note(DiatonicPitch.parse("Db:4"), Duration(1, 4))
        policy = FixedPitchConstraint(note, DiatonicPitch.parse("Ab:5"))

        policy_context = TestFixedPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('F#'), 'tIV',
                                                                 'C:2', 'C:8')
        contextual_note = ContextualNote(policy_context)
        p_map = PMap()
        p_map[note] = contextual_note

        v_result = policy.values(p_map, note)

        result = next(iter(v_result))
        print('test_scale_enharmonic_map note= {0}'.format(note))

        assert result.diatonic_pitch == DiatonicPitch.parse("G#:5")
        assert result.base_duration == Duration(1, 4)

        contextual_note.note = result
        result = policy.verify(p_map)
        assert result is True

        logging.debug('end test_scale_enharmonic_map')

    def test_non_scale_note(self):
        logging.debug('Start test_non_scale_note')

        note = Note(DiatonicPitch.parse("Bb:4"), Duration(1, 4))
        policy = FixedPitchConstraint(note, DiatonicPitch.parse("Ab:5"))

        policy_context = TestFixedPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
                                                                 'C:2', 'C:8')
        contextual_note = ContextualNote(policy_context)
        p_map = PMap()
        p_map[note] = contextual_note

        v_result = policy.values(p_map, note)

        result = next(iter(v_result))
        print('test_non_scale_note note= {0}'.format(result))

        assert result.diatonic_pitch == DiatonicPitch.parse("Ab:5")
        assert result.base_duration == Duration(1, 4)

        contextual_note.note = result

        result = policy.verify(p_map)
        assert result is True

        logging.debug('end test_non_scale_note')

    def test_non_diatonic_scale_note(self):
        logging.debug('Start test_non_diatonic_scale_note')

        note = Note(DiatonicPitch.parse("A:4"), Duration(1, 4))
        policy = FixedPitchConstraint(note, DiatonicPitch.parse("Ab:5"))

        policy_context = TestFixedPitchConstraint.policy_creator(ModalityType.MajorPentatonic, DiatonicTone('C'),
                                                                 'tIV',
                                                                 'C:2', 'C:8')
        contextual_note = ContextualNote(policy_context)
        p_map = PMap()
        p_map[note] = contextual_note

        v_result = policy.values(p_map, note)

        result = next(iter(v_result))
        print('test_non_scale_note note= {0}'.format(result))

        assert result.diatonic_pitch == DiatonicPitch.parse("Ab:5")
        assert result.base_duration == Duration(1, 4)

        contextual_note.note = result

        result = policy.verify(p_map)
        assert result is True

        logging.debug('end test_non_diatonic_scale_note')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
