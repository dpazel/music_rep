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
from melody.constraints.pitch_range_constraint import PitchRangeConstraint

import logging
import sys


class TestPitchRangeConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_in_range(self):
        logging.debug('Start test_in_range')

        upper_policy_context = TestPitchRangeConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
                                                                   'C:2', 'C:8')
        lower_policy_context = TestPitchRangeConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                   'C:2', 'C:8')

        v_notes = []
        p_map = PMap()
        for s in ['C:5', 'B:4', 'D:5', 'G:4']:
            v_note = Note(DiatonicPitch.parse(s), Duration(1, 8))
            v_notes.append(v_note)
            p_map[v_note] = ContextualNote(lower_policy_context)

        policy = PitchRangeConstraint(v_notes, PitchRange.create('G:3', 'A:4'))

        values = policy.values(p_map, v_notes[0])

        assert values is not None
        assert len(values) is not 0
        pitches = set()
        for v in values:
            print(v.diatonic_pitch)
            pitches.add(v.diatonic_pitch)

        answers_str = {'G:3', 'A:3', 'B:3', 'C:4', 'D:4', 'E:4', 'F#:4', 'G:4', 'A:4'}
        answers = {DiatonicPitch.parse(s) for s in answers_str}
        assert pitches == answers

        index = 0
        it = iter(values)
        for v_note in v_notes:
            p_map[v_note].note = next(it)
            index = index + 1
        assert policy.verify(p_map) is True

        # Change one and get false
        p_map[v_notes[0]].note = Note(DiatonicPitch.parse('B:4'), Duration(1, 8))
        assert policy.verify(p_map) is False

        logging.debug('End test_in_range')

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
