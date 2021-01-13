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
from melody.constraints.equal_pitch_constraint import EqualPitchConstraint

import logging
import sys


class TestEqualPitchConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_equal(self):
        logging.debug('Start test_is_equal')

        upper_context_note_a = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))

        upper_context_note_b = Note(DiatonicPitch.parse('C:5'), Duration(1, 8))

        lower_policy_context = TestEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                   'C:2', 'C:8')

        lower_context_note_a = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:6'),
                                                                         Duration(1, 8)))

        lower_context_note_b = ContextualNote(lower_policy_context)

        parameter_map = dict([(upper_context_note_a, lower_context_note_a),
                              (upper_context_note_b, lower_context_note_b)])
        parameter_map = PMap(parameter_map)

        policy = EqualPitchConstraint([upper_context_note_a, upper_context_note_b])

        result = policy.values(parameter_map, upper_context_note_b)

        actual_note = next(iter(result))
        print('test_is_equal; note = {0}'.format(actual_note))

        assert actual_note.diatonic_pitch == DiatonicPitch.parse("F#:6")
        assert actual_note.base_duration == Duration(1, 8)

        parameter_map[upper_context_note_b].note = actual_note

        assert policy.verify(parameter_map) is True

        logging.debug('End test_is_equal')

    def test_is_not_equal(self):
        logging.debug('Start test_is_not_equal')
        upper_policy_context = TestEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'), 'tIV',
                                                                   'C:2', 'C:8')

        upper_context_note_a = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('C:5'),
                                                                         Duration(1, 8)))

        upper_context_note_b = ContextualNote(upper_policy_context, Note(DiatonicPitch.parse('C:5'),
                                                                         Duration(1, 8)))

        lower_policy_context = TestEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                   'C:2', 'C:8')

        lower_context_note_a = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:6'),
                                                                         Duration(1, 8)))

        lower_context_note_b = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('G:6'),
                                                                         Duration(1, 8)))

        parameter_map = dict([(upper_context_note_a, lower_context_note_a),
                              (upper_context_note_b, lower_context_note_b)])

        policy = EqualPitchConstraint([upper_context_note_a, upper_context_note_b])

        assert policy.verify(parameter_map) is False

        logging.debug('End test_is_not_equal')

    def test_more_than_two(self):
        logging.debug('Start test_more_than_two')

        upper_policy_context = TestEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'), 'tIV',
                                                                   'C:2', 'C:8')
        lower_policy_context = TestEqualPitchConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                   'C:2', 'C:8')

        upper_notes = list()
        for i in range(0, 5):
            upper_notes.append(Note(DiatonicPitch.parse('C:5'), Duration(1, 8)))
        lower_notes = list()
        for i in range(0, 5):
            n = ContextualNote(lower_policy_context, Note(DiatonicPitch.parse('F#:6'),
                                                          Duration(1, 8))) if i == 0 else \
                ContextualNote(lower_policy_context)
            lower_notes.append(n)

        policy = EqualPitchConstraint(upper_notes)

        p_map = PMap()
        for i in range(0, 5):
            p_map[upper_notes[i]] = lower_notes[i]

        for i in range(1, len(upper_notes)):
            v_results = policy.values(p_map, upper_notes[i])
            assert len(v_results) == 1
            note = next(iter(v_results))
            print(note)

            assert str(note.diatonic_pitch) == 'F#:6'

        # Again but assign the received note each time - then call verify.
        for i in range(1, len(upper_notes)):
            v_results = policy.values(p_map, upper_notes[i])
            note = next(iter(v_results))
            p_map[upper_notes[i]].note = note

            assert str(note.diatonic_pitch) == 'F#:6'

        assert policy.verify(p_map)

        logging.debug("End test_more_than_two")

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
