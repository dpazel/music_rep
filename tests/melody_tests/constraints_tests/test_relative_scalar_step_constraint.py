import unittest

from tonalmodel.pitch_scale import PitchScale
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
from melody.constraints.relative_scalar_step_constraint import RelativeScalarStepConstraint

import logging
import sys


class TestRelativeScalarStepConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_closest_scale_tones(self):
        logging.debug('Start test_compute_closest_scale_tones')

        tonality = Tonality.create(ModalityType.Major, DiatonicTone('Ab'))
        test_pitches = ['A:4', 'B:4', 'C:4', 'D:4', 'E:4', 'F:4', 'G:4', 'Ab:4', 'Bb:4', 'Db:4', 'Eb:4',
                        'C#:4', 'D#:4', 'G#:4', 'A#:4', 'B#:4', 'Cb:4', 'B##:4', 'Cbb:4']
        answers = [
            '[Ab:4,Bb:4]',
            '[Bb:4,C:5]',
            '[C:4]',
            '[Db:4,Eb:4]',
            '[Eb:4,F:4]',
            '[F:4]',
            '[G:4]',
            '[Ab:4]',
            '[Bb:4]',
            '[Db:4]',
            '[Eb:4]',
            '[Db:4]',
            '[Eb:4]',
            '[Ab:4]',
            '[Bb:4]',
            '[C:5]',
            '[Bb:3,C:4]',
            '[Db:5]',
            '[Bb:3]',
        ]
        for pitch_str, answer in zip(test_pitches, answers):
            pitch = DiatonicPitch.parse(pitch_str)
            closest = PitchScale.compute_closest_scale_tones(tonality, pitch)
            # print('{0} ==> [{1}]'.format(pitch, ','.join(str(p) for p in closest)))
            test_answer = '[' + (','.join(str(p) for p in closest)) + ']'
            assert answer == test_answer

        #  Do again for C major
        tonality = Tonality.create(ModalityType.HarmonicMinor, DiatonicTone('C'))
        test_pitches = ['C:4', 'D:4', 'E:4', 'F:4', 'G:4', 'A:4', 'B:4', 'Eb:4', 'Ab:4', 'Db:4',
                        'Gb:4', 'Bb:4', 'Cb:4', 'B#:4'
                        ]
        answers = [
            '[C:4]',
            '[D:4]',
            '[Eb:4,F:4]',
            '[F:4]',
            '[G:4]',
            '[Ab:4,B:4]',
            '[B:4]',
            '[Eb:4]',
            '[Ab:4]',
            '[C:4,D:4]',
            '[F:4,G:4]',
            '[Ab:4,B:4]',
            '[B:3]',
            '[C:5]',
        ]
        for pitch_str, answer in zip(test_pitches, answers):
            pitch = DiatonicPitch.parse(pitch_str)
            closest = PitchScale.compute_closest_scale_tones(tonality, pitch)
            test_answer = '[' + (','.join(str(p) for p in closest)) + ']'
            assert answer == test_answer

        logging.debug('End test_compute_closest_scale_tones')

    def test_compute_tonal_pitch_range(self):
        logging.debug('Start test_compute_tonal_pitch_range')

        tonality = Tonality.create(ModalityType.Major, DiatonicTone('Ab'))

        pitch = DiatonicPitch(4, 'B#')
        pitches = PitchScale.compute_tonal_pitch_range(tonality, pitch, 5, 7)
        for p in reversed(pitches):
            print(p)

        test_pitches = ['A:4', 'B:4', 'C:4', 'D:4', 'E:4', 'F:4', 'G:4', 'Ab:4', 'Bb:4', 'Db:4', 'Eb:4',
                        'C#:4', 'D#:4', 'G#:4', 'A#:4', 'B#:4', 'Cb:4', 'B##:4', 'Cbb:4']

        ranges = [[0, 5], [-5, 0], [-4, 2], [-5, -3], [5, 7]]

        answers = [
            '[Ab:4,Bb:4,C:5,Db:5,Eb:5,F:5,G:5]',
            '[C:4,Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[C:4,Db:4,Eb:4]',
            '[G:5,Ab:5,Bb:5]',
            '[Bb:4,C:5,Db:5,Eb:5,F:5,G:5,Ab:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5,Db:5,Eb:5]',
            '[Db:4,Eb:4,F:4]',
            '[Ab:5,Bb:5,C:6]',
            '[C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[Eb:3,F:3,G:3,Ab:3,Bb:3,C:4]',
            '[F:3,G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4]',
            '[Eb:3,F:3,G:3]',
            '[Ab:4,Bb:4,C:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[F:3,G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4,G:4]',
            '[F:3,G:3,Ab:3]',
            '[C:5,Db:5,Eb:5]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4]',
            '[Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[G:3,Ab:3,Bb:3]',
            '[Db:5,Eb:5,F:5]',
            '[F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4]',
            '[Bb:3,C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[Ab:3,Bb:3,C:4]',
            '[Db:5,Eb:5,F:5]',
            '[G:4,Ab:4,Bb:4,C:5,Db:5,Eb:5]',
            '[Bb:3,C:4,Db:4,Eb:4,F:4,G:4]',
            '[C:4,Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[Bb:3,C:4,Db:4]',
            '[Eb:5,F:5,G:5]',
            '[Ab:4,Bb:4,C:5,Db:5,Eb:5,F:5]',
            '[C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[C:4,Db:4,Eb:4]',
            '[F:5,G:5,Ab:5]',
            '[Bb:4,C:5,Db:5,Eb:5,F:5,G:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[Db:4,Eb:4,F:4]',
            '[G:5,Ab:5,Bb:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[F:3,G:3,Ab:3,Bb:3,C:4,Db:4]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4]',
            '[F:3,G:3,Ab:3]',
            '[Bb:4,C:5,Db:5]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4]',
            '[Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4,G:4]',
            '[G:3,Ab:3,Bb:3]',
            '[C:5,Db:5,Eb:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[F:3,G:3,Ab:3,Bb:3,C:4,Db:4]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4]',
            '[F:3,G:3,Ab:3]',
            '[Bb:4,C:5,Db:5]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4]',
            '[Ab:3,Bb:3,C:4,Db:4,Eb:4,F:4,G:4]',
            '[G:3,Ab:3,Bb:3]',
            '[C:5,Db:5,Eb:5]',
            '[Ab:4,Bb:4,C:5,Db:5,Eb:5,F:5]',
            '[C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[C:4,Db:4,Eb:4]',
            '[F:5,G:5,Ab:5]',
            '[Bb:4,C:5,Db:5,Eb:5,F:5,G:5]',
            '[Db:4,Eb:4,F:4,G:4,Ab:4,Bb:4]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[Db:4,Eb:4,F:4]',
            '[G:5,Ab:5,Bb:5]',
            '[C:5,Db:5,Eb:5,F:5,G:5,Ab:5]',
            '[Eb:4,F:4,G:4,Ab:4,Bb:4,C:5]',
            '[F:4,G:4,Ab:4,Bb:4,C:5,Db:5,Eb:5]',
            '[Eb:4,F:4,G:4]',
            '[Ab:5,Bb:5,C:6]',
            '[Bb:3,C:4,Db:4,Eb:4,F:4,G:4,Ab:4]',
            '[Db:3,Eb:3,F:3,G:3,Ab:3,Bb:3,C:4]',
            '[Eb:3,F:3,G:3,Ab:3,Bb:3,C:4,Db:4,Eb:4]',
            '[Db:3,Eb:3,F:3]',
            '[Ab:4,Bb:4,C:5]',
            '[Db:5,Eb:5,F:5,G:5,Ab:5,Bb:5]',
            '[F:4,G:4,Ab:4,Bb:4,C:5,Db:5]',
            '[G:4,Ab:4,Bb:4,C:5,Db:5,Eb:5,F:5]',
            '[F:4,G:4,Ab:4]',
            '[Bb:5,C:6,Db:6]',
            '[Bb:3,C:4,Db:4,Eb:4,F:4,G:4]',
            '[Db:3,Eb:3,F:3,G:3,Ab:3,Bb:3]',
            '[Eb:3,F:3,G:3,Ab:3,Bb:3,C:4,Db:4]',
            '[Db:3,Eb:3,F:3]',
            '[G:4,Ab:4,Bb:4]',

        ]

        answer_idx = 0
        for pitch_str in test_pitches:
            for r in ranges:
                pitch = DiatonicPitch.parse(pitch_str)
                pitches = PitchScale.compute_tonal_pitch_range(tonality, pitch, r[0], r[1])
                answer_str = '[' + (','.join(str(p) for p in pitches)) + ']'
                # print '\'[' + (','.join(str(p) for p in pitches)) + ']\','
                answer = answers[answer_idx]
                answer_idx = answer_idx + 1
                print('{0} [{1}, {2}]: {3}'.format(pitch, r[0], r[1], answer_str))

                assert answer == answer_str

        logging.debug('End test_compute_tonal_pitch_range')

    def test_basic_policy(self):
        logging.debug('Start test_basic_policy')
        upper_policy_context = TestRelativeScalarStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'),
                                                                               'tIV',
                                                                               'C:2', 'C:8')
        lower_policy_context = TestRelativeScalarStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                               'tV',
                                                                               'C:2', 'C:8')
        upper_note_1 = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('C:5'), Duration(1, 8)))
        upper_note_2 = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('D:5'), Duration(1, 8)))
        lower_note_1 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:5'), Duration(1, 8)))
        lower_note_2 = ContextualNote(lower_policy_context)

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        # F#:5 --> G Major two below and 3 above
        policy = RelativeScalarStepConstraint(upper_note_1, upper_note_2, -2, 3)

        v_result = policy.values(p_map, upper_note_2)
        pitches = [n.diatonic_pitch for n in v_result]
        assert len(pitches) == 6
        for s in ['D:5', 'E:5', 'F#:5', 'G:5', 'A:5', 'B:5']:
            assert DiatonicPitch.parse(s) in pitches

        for note in v_result:
            logging.debug(note)

        # Check verify for each answer
        for n in v_result:
            lower_note_2.note = n
            assert policy.verify(p_map)

        logging.debug('End test_basic_policy')

    def test_reversal_on_policy(self):
        logging.debug('Start test_reversal_on_policy')
        upper_policy_context = TestRelativeScalarStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'),
                                                                               'tIV',
                                                                               'C:2', 'C:8')
        lower_policy_context = TestRelativeScalarStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'),
                                                                               'tV',
                                                                               'C:2', 'C:8')
        upper_note_1 = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('C:5'), Duration(1, 8)))
        upper_note_2 = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('D:5'), Duration(1, 8)))
        lower_note_1 = ContextualNote(lower_policy_context)
        lower_note_2 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('C:5'), Duration(1, 8)))

        p_map = dict([(upper_note_1, lower_note_1),
                      (upper_note_2, lower_note_2)])

        # F#:5 --> G Major two below and 3 above
        policy = RelativeScalarStepConstraint(upper_note_1, upper_note_2, -2, 3)

        result = policy.values(p_map, upper_note_1)
        pitches = [n.diatonic_pitch for n in result]

        for pitch in pitches:
            logging.debug(pitch)

        # Check that each returned verifies
        for n in result:
            lower_note_1.note = n
            assert policy.verify(p_map)

        logging.debug('End test_reversal_on_policy')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)

    if __name__ == "__main__":
        unittest.main()
