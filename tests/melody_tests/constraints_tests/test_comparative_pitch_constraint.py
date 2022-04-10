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
from tonalmodel.pitch_range import PitchRange
from structure.note import Note
from melody.constraints.comparative_pitch_constraint import ComparativePitchConstraint
from operator import attrgetter

import logging
import sys


class TestComparativePitchConstraint(unittest.TestCase):
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def test_basic_policy(self):
        logging.debug('Start test_basic_policy')

        lower_policy_context = TestComparativePitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                             'tV', 'C:4', 'C:6')
        upper_note_1 = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        upper_note_2 = Note(DiatonicPitch.parse('D:5'), Duration(1, 8))
        lower_note_1 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))
        lower_note_2 = ContextualNote(lower_policy_context)

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.LESS_THAN)
        result = policy.values(p_map, upper_note_2)

        pitches = sorted([note.diatonic_pitch for note in result])

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') not in pitches
        assert len(pitches) == 4
        for pitch in pitches:
            assert pitch.chromatic_distance > DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} <= {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_2.note = note
            assert policy.verify(p_map) is True
        lower_note_2.note = None

        # Do less than
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.GREATER_THAN)
        result = policy.values(p_map, upper_note_2)

        pitches = sorted([note.diatonic_pitch for note in result])
        for pitch in pitches:
            logging.debug(pitch)

        assert DiatonicPitch.parse('F#:5') not in pitches
        assert len(pitches) == 10

        for pitch in pitches:
            assert pitch.chromatic_distance < DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} >= {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_2.note = note
            assert policy.verify(p_map) is True
        lower_note_2.note = None

        # Do greater than or equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.LESS_EQUAL)
        result = policy.values(p_map, upper_note_2)

        pitches = sorted([note.diatonic_pitch for note in result])
        for pitch in pitches:
            logging.debug(pitch)

        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 5

        for pitch in pitches:
            assert pitch.chromatic_distance >= DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} < {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_2.note = note
            assert policy.verify(p_map) is True
        lower_note_2.note = None

        # Do less than or equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.GREATER_EQUAL)
        result = policy.values(p_map, upper_note_2)

        pitches = sorted([note.diatonic_pitch for note in result])
        for pitch in pitches:
            logging.debug(pitch)

        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 11

        for pitch in pitches:
            assert pitch.chromatic_distance <= DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} > {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_2.note = note
            assert policy.verify(p_map) is True
        lower_note_2.note = None

        # Do equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.EQUAL)
        result = policy.values(p_map, upper_note_2)

        pitches = sorted([note.diatonic_pitch for note in result])
        for pitch in pitches:
            logging.debug(pitch)

        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 1

        for pitch in pitches:
            assert pitch.chromatic_distance == DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} != {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_2.note = note
            assert policy.verify(p_map) is True
        lower_note_2.note = None

        logging.debug('End test_basic_policy')

    def test_comparative_reversal(self):
        logging.debug('Start test_comparative_reversal')

        lower_policy_context = TestComparativePitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                             'tV', 'C:4', 'C:6')
        upper_note_1 = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))
        upper_note_2 = Note(DiatonicPitch.parse('D:5'), Duration(1, 8))
        lower_note_1 = ContextualNote(lower_policy_context)
        lower_note_2 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        policy = ComparativePitchConstraint(upper_note_1, upper_note_2,
                                            ComparativePitchConstraint.LESS_THAN)
        result = policy.values(p_map, upper_note_1)

        pitches = sorted([note.diatonic_pitch for note in result], key=attrgetter('chromatic_distance'))

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') not in pitches
        assert len(pitches) == 10
        for pitch in pitches:
            assert pitch.chromatic_distance < DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} => {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_1.note = note
            assert policy.verify(p_map) is True
        lower_note_1.note = None

        # Test Less than
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.GREATER_THAN)
        result = policy.values(p_map, upper_note_1)

        pitches = sorted([note.diatonic_pitch for note in result], key=attrgetter('chromatic_distance'))

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') not in pitches
        assert len(pitches) == 4
        for pitch in pitches:
            assert pitch.chromatic_distance > DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} <= {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_1.note = note
            assert policy.verify(p_map) is True
        lower_note_1.note = None

        # Test greater than or equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.LESS_EQUAL)
        result = policy.values(p_map, upper_note_1)

        pitches = sorted([note.diatonic_pitch for note in result], key=attrgetter('chromatic_distance'))

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 11
        for pitch in pitches:
            assert pitch.chromatic_distance <= DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} > {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_1.note = note
            assert policy.verify(p_map) is True
        lower_note_1.note = None

        # Test less than or equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.GREATER_EQUAL)
        result = policy.values(p_map, upper_note_1)

        pitches = sorted([note.diatonic_pitch for note in result], key=attrgetter('chromatic_distance'))

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 5
        for pitch in pitches:
            assert pitch.chromatic_distance >= DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} < {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_1.note = note
            assert policy.verify(p_map) is True
        lower_note_1.note = None

        # Test equal
        logging.debug('------')
        policy = ComparativePitchConstraint(upper_note_1, upper_note_2, ComparativePitchConstraint.EQUAL)
        result = policy.values(p_map, upper_note_1)

        pitches = sorted([note.diatonic_pitch for note in result], key=attrgetter('chromatic_distance'))

        for pitch in pitches:
            logging.debug(pitch)

        # validate
        assert DiatonicPitch.parse('F#:5') in pitches
        assert len(pitches) == 1
        for pitch in pitches:
            assert pitch.chromatic_distance == DiatonicPitch.parse('F#:5').chromatic_distance, \
                "{0} != {1}".format(pitch,  DiatonicPitch.parse('F#:5'))

        for note in result:
            lower_note_1.note = note
            assert policy.verify(p_map) is True
        lower_note_1.note = None
        logging.debug('End test_comparative_reversal')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)

