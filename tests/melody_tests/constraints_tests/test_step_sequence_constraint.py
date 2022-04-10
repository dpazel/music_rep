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
from melody.constraints.step_sequence_constraint import StepSequenceConstraint

import logging
import sys


class TestStepSequenceConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_compute_simple_scale_tones(self):
        print('Start test_compute_simple_scale_tones')

        # upper_policy_context = TestStepSequenceConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'),
        # 'tIV',
        #                                                            'C:2', 'C:8')
        lower_policy_context = TestStepSequenceConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                         'C:2', 'C:8')
        upper_pitch_txts = ['C:5', 'D:5', 'E:5', 'G:5', 'B:5', 'C:6', 'B:5', 'G:5', 'E:5', 'D:5', 'C:5', 'C:5']
        actors = list()
        differentials = [1, 1, 2, 2, 1, -1, -2, -2, -1, -1, 0]
        p_map = PMap()
        for pitch_txt in upper_pitch_txts:
            upper_note = Note(DiatonicPitch.parse(pitch_txt), Duration(1, 8))
            lower_note = ContextualNote(lower_policy_context)
            p_map[upper_note] = lower_note
            actors.append(upper_note)

        policy = StepSequenceConstraint(actors, differentials)

        notes = policy.values(p_map, actors[2])

        print('uninitialized: {0} notes'.format(len(notes)))
        for note in notes:
            print(note.diatonic_pitch)
        print('-----')

        assert len(notes) == 7 * 6 + 1
        assert str(next(iter(notes)).diatonic_pitch) == 'C:2'
        note = None
        for n in notes:
            note = n
        assert note is not None
        assert str(note.diatonic_pitch) == 'C:8'

        p_map[actors[0]].note = Note(DiatonicPitch.parse('F#:4'), Duration(1, 8))
        answers = ['F#:4', 'G:4', 'A:4', 'C:5', 'E:5', 'F#:5', 'E:5', 'C:5', 'A:4', 'G:4', 'F#:4', 'F#:4']
        for i in range(1, len(actors)):
            notes = policy.values(p_map, actors[i])
            for note in notes:
                print(note.diatonic_pitch)
            assert str(next(iter(notes)).diatonic_pitch) == answers[i]
        print('-----')

        p_map[actors[-1]].note = Note(DiatonicPitch.parse('F#:4'), Duration(1, 8))
        p_map[actors[0]].note = None
        answers = ['F#:4', 'G:4', 'A:4', 'C:5', 'E:5', 'F#:5', 'E:5', 'C:5', 'A:4', 'G:4', 'F#:4', 'F#:4']
        for i in range(1, len(actors)):
            notes = policy.values(p_map, actors[i])
            for note in notes:
                print(note.diatonic_pitch)
            assert str(next(iter(notes)).diatonic_pitch) == answers[i]
        print('-----')

        p_map[actors[6]].note = Note(DiatonicPitch.parse('E:5'), Duration(1, 8))
        p_map[actors[-1]].note = None
        answers = ['E:5', 'G:4', 'A:4', 'C:5', 'E:5', 'F#:5', 'E:5', 'C:5', 'A:4', 'G:4', 'F#:4', 'F#:4']
        for i in range(1, len(actors)):
            notes = policy.values(p_map, actors[i])
            for note in notes:
                print(note.diatonic_pitch)
            assert str(next(iter(notes)).diatonic_pitch) == answers[i]
        print('-----')

        logging.debug('End test_compute_simple_scale_tones')

    def test_simple_cross_tonality(self):
        logging.debug('Start test_simple_cross_tonality')

        # upper_policy_context = TestStepSequenceConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
        #                                                             'C:2', 'C:8')
        lower_policy_context_1 = TestStepSequenceConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                           'C:2', 'C:8')
        lower_policy_context_2 = TestStepSequenceConstraint.policy_creator(ModalityType.Major, DiatonicTone('B'), 'tV',
                                                                           'C:2', 'C:8')
        upper_pitch_txts = ['C:5', 'D:5', 'E:5', 'F:5']
        tonalities = [lower_policy_context_1, lower_policy_context_1, lower_policy_context_2, lower_policy_context_2]
        differentials = [1, 1, 1]
        actors = list()
        p_map = dict()
        for i in range(0, len(upper_pitch_txts)):
            upper_note = Note(DiatonicPitch.parse(upper_pitch_txts[i]), Duration(1, 8))
            lower_note = ContextualNote(tonalities[i])
            actors.append(upper_note)
            p_map[upper_note] = lower_note

        policy = StepSequenceConstraint(actors, differentials)

        p_map[actors[0]].note = Note(DiatonicPitch.parse('B:5'), Duration(1, 8))
        answers = ['B:6', 'C:6', 'C#:6', 'D#:6']
        for i in range(1, len(actors)):
            notes = policy.values(p_map, actors[i])
            for note in notes:
                print(note.diatonic_pitch)
            assert str(next(iter(notes)).diatonic_pitch) == answers[i]
        print("------")

        upper_pitch_txts = ['F#:5', 'E:5', 'D:5', 'C:5']
        tonalities = [lower_policy_context_1, lower_policy_context_1, lower_policy_context_2, lower_policy_context_2]
        differentials = [-1, -1, -1]
        actors = list()
        p_map = dict()
        for i in range(0, len(upper_pitch_txts)):
            upper_note = Note(DiatonicPitch.parse(upper_pitch_txts[i]), Duration(1, 8))
            lower_note = ContextualNote(tonalities[i])
            actors.append(upper_note)
            p_map[upper_note] = lower_note

        policy = StepSequenceConstraint(actors, differentials)

        p_map[actors[0]].note = Note(DiatonicPitch.parse('F#:6'), Duration(1, 8))
        answers = ['F#:6', 'E:6', 'D#:6', 'C#:6']
        for i in range(1, len(actors)):
            notes = policy.values(p_map, actors[i])
            for note in notes:
                print(note.diatonic_pitch)
            assert str(next(iter(notes)).diatonic_pitch) == answers[i]
        print("------")

        logging.debug('End test_simple_cross_tonality')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
