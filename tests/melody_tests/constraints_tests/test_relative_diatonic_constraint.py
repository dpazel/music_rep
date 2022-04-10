import unittest
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext
from melody.constraints.policy_context import PolicyContext
from melody.constraints.contextual_note import ContextualNote
from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.interval import Interval, IntervalType
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.pitch_range import PitchRange
from structure.note import Note
from melody.constraints.relative_diatonic_constraint import RelativeDiatonicConstraint

import logging
import sys


class TestRelativeDiatonicConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_diatonic_test(self):
        logging.debug('Start test_simple_diatonic_test')
        lower_policy_context = TestRelativeDiatonicConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                             'tV', 'C:2', 'C:8')
        upper_note_1 = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        upper_note_2 = Note(DiatonicPitch.parse('D:5'), Duration(1, 8))
        lower_note_1 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))
        lower_note_2 = ContextualNote(lower_policy_context)

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        policy = RelativeDiatonicConstraint(upper_note_1, upper_note_2,
                                            Interval(3, IntervalType.Minor),
                                            Interval(3, IntervalType.Major)
                                            )

        v_result = policy.values(p_map, upper_note_2)

        for note in v_result:
            logging.debug(note)

        pitches = [note.diatonic_pitch for note in v_result]
        assert {str(p) for p in pitches} == {'D:5', 'E:5', 'F#:5', 'G:5', 'A:5'}

        # test for determining note 1
        logging.debug('Determining note 1')
        lower_note_2.note = lower_note_1.note
        lower_note_1.note = None

        v_result = policy.values(p_map, upper_note_1)

        for note in v_result:
            logging.debug(note)

        pitches = [note.diatonic_pitch for note in v_result]
        assert {str(p) for p in pitches} == {'A:5', 'G:5', 'F#:5', 'E:5'}

        logging.debug('End test_simple_diatonic_test')

    def test_across_tonalities(self):
        logging.debug('Start test_across_tonalities.')
        lower_policy_context_1 = TestRelativeDiatonicConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                               'tV', 'C:2', 'C:8')
        lower_policy_context_2 = TestRelativeDiatonicConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'),
                                                                               'tI', 'C:2', 'C:8')

        upper_note_1 = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        upper_note_2 = Note(DiatonicPitch.parse('D:5'), Duration(1, 8))
        lower_note_1 = ContextualNote(lower_policy_context_1, Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))
        lower_note_2 = ContextualNote(lower_policy_context_2)

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        policy = RelativeDiatonicConstraint(upper_note_1, upper_note_2,
                                            Interval(3, IntervalType.Minor),
                                            Interval(3, IntervalType.Major)
                                            )

        v_result = policy.values(p_map, upper_note_2)

        for note in v_result:
            logging.debug(note)

        pitches = [note.diatonic_pitch for note in v_result]
        assert {str(p) for p in pitches} == {'Eb:5', 'F:5', 'G:5', 'Ab:5'}

        logging.debug('End test_across_tonalities.')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
