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
from melody.constraints.pitch_step_constraint import PitchStepConstraint

import logging
import sys


class TestPitchStepConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_major_scale_ascent(self):
        logging.debug('Start test_simple_major_scale_ascent')
        upper_context_notes = list()
        for s in ['C:5', 'D:5', 'E:5', 'F:5', 'G:5', 'A:5', 'B:5', 'C:6']:
            upper_context_notes.append(Note(DiatonicPitch.parse(s), Duration(1, 8)))

        lower_policy_context = TestPitchStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                      'C:2', 'C:8')

        lower_context_notes = list()
        for s in range(0, len(upper_context_notes)):
            lower_context_notes.append(ContextualNote(lower_policy_context))
        lower_context_notes[0].note = Note(DiatonicPitch.parse("E:4"), Duration(1, 8))

        parameter_map = dict()
        policies = []
        for s, sp in zip(upper_context_notes, lower_context_notes):
            parameter_map[s] = sp
        for i in range(0, len(upper_context_notes) - 1):
            policies.append(PitchStepConstraint(upper_context_notes[i], upper_context_notes[i + 1]))

        answers = ['F#:4', 'G:4', 'A:4', 'B:4', 'C:5', 'D:5', 'E:5']
        for policy, answer in zip(policies, answers):
            result = policy.values(parameter_map, policy.note_two)
            note = next(iter(result))
            print(note)

            assert str(note.diatonic_pitch) == answer

            parameter_map[policy.note_two].note = note
            assert policy.verify(parameter_map)

        logging.debug('End test_simple_major_scale_ascent')

    def test_simple_major_scale_descent(self):
        logging.debug('Start test_simple_major_scale_descent')
        upper_context_notes = list()
        for s in ['C:6', 'B:5', 'A:5', 'G:5', 'F:5', 'E:5', 'D:5', 'C:5']:
            upper_context_notes.append(Note(DiatonicPitch.parse(s), Duration(1, 8)))

        lower_policy_context = TestPitchStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                      'C:2', 'C:8')

        lower_context_notes = list()
        for s in range(0, len(upper_context_notes)):
            lower_context_notes.append(ContextualNote(lower_policy_context))
        lower_context_notes[0].note = Note(DiatonicPitch.parse("E:5"), Duration(1, 8))

        parameter_map = dict()
        policies = []
        for s, sp in zip(upper_context_notes, lower_context_notes):
            parameter_map[s] = sp
        for i in range(0, len(upper_context_notes) - 1):
            policies.append(PitchStepConstraint(upper_context_notes[i], upper_context_notes[i + 1], 1,
                                                PitchStepConstraint.Down))

        answers = ['D:5', 'C:5', 'B:4', 'A:4', 'G:4', 'F#:4', 'E:4']
        for policy, answer in zip(policies, answers):
            result = policy.values(parameter_map, policy.note_two)
            note = next(iter(result))
            print(note)

            assert str(note.diatonic_pitch) == answer

            parameter_map[policy.note_two].note = note
            assert policy.verify(parameter_map)

        logging.debug('End test_simple_major_scale_descent')

    def test_simple_major_scale_descent_two_steps(self):
        logging.debug('Start test_simple_major_scale_descent_two_steps')
        upper_context_notes = list()
        for s in ['C:6', 'A:5', 'F:5', 'D:5', 'B:4']:
            upper_context_notes.append(Note(DiatonicPitch.parse(s), Duration(1, 8)))

        lower_policy_context = TestPitchStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                      'C:2', 'C:8')

        lower_context_notes = list()
        for s in range(0, len(upper_context_notes)):
            lower_context_notes.append(ContextualNote(lower_policy_context))
        lower_context_notes[0].note = Note(DiatonicPitch.parse("E:5"), Duration(1, 8))

        parameter_map = dict()
        policies = []
        for s, sp in zip(upper_context_notes, lower_context_notes):
            parameter_map[s] = sp
        for i in range(0, len(upper_context_notes) - 1):
            policies.append(PitchStepConstraint(upper_context_notes[i], upper_context_notes[i + 1], 2,
                                                PitchStepConstraint.Down))

        answers = ['C:5', 'A:4', 'F#:4', 'D:4']
        for policy, answer in zip(policies, answers):
            result = policy.values(parameter_map, policy.note_two)
            note = next(iter(result))
            print(note)

            assert str(note.diatonic_pitch) == answer

            parameter_map[policy.note_two].note = note
            assert policy.verify(parameter_map)

        logging.debug('End test_simple_major_scale_descent_two_steps')

    def test_reverse_arguments(self):
        logging.debug('Start test_reverse_arguments')
        lower_policy_context = TestPitchStepConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                      'C:2', 'C:8')

        upper_context_notes = list()
        for s in ['C:6', 'B5']:
            upper_context_notes.append(Note(DiatonicPitch.parse(s), Duration(1, 8)))

        policy = PitchStepConstraint(upper_context_notes[0], upper_context_notes[1], 1, PitchStepConstraint.Down)

        lower_contextual_note_0 = ContextualNote(lower_policy_context)
        lower_contextual_note_1 = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse("E:5"), Duration(1, 4)))

        parameter_map = dict([(upper_context_notes[0], lower_contextual_note_0),
                              (upper_context_notes[1], lower_contextual_note_1)])

        result = policy.values(parameter_map, policy.note_one)
        note = next(iter(result))
        print(note)
        assert str(note.diatonic_pitch) == 'F#:5'

        logging.debug('End test_reverse_arguments')

    @staticmethod
    def policy_creator(modality_type, modality_tone, tertian_chord_txt, low_pitch_txt, hi_pitch_txt):
        diatonic_tonality = Tonality.create(modality_type, modality_tone)
        chord = TertianChordTemplate.parse(tertian_chord_txt).create_chord(diatonic_tonality)
        hc = HarmonicContext(diatonic_tonality, chord, Duration(1, 2))

        pitch_range = PitchRange(DiatonicPitch.parse(low_pitch_txt).chromatic_distance,
                                 DiatonicPitch.parse(hi_pitch_txt).chromatic_distance)
        return PolicyContext(hc, pitch_range)
