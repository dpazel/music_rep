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
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint

import logging
import sys


class TestChordalToneConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_chordal(self):
        logging.debug('Start test_is_chordal')
        upper_policy_context = TestChordalToneConstraint.policy_creator(ModalityType.Major, DiatonicTone('Ab'), 'tIV',
                                                                    'C:2', 'C:8')

        upper_context_note = Note(DiatonicPitch.parse('F:5'), Duration(1, 4))

        lower_policy_context = TestChordalToneConstraint.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                                    'C:2', 'C:8')

        lower_context_note = ContextualNote(lower_policy_context)

        parameter_map = dict([(upper_context_note, lower_context_note)])

        policy = ChordalPitchConstraint(upper_context_note)

        v_result = policy.values(parameter_map, upper_context_note)

        results = {DiatonicTone('D'), DiatonicTone('F#'), DiatonicTone('A')}
        for note in v_result:
            print('test_is_chordal; note = {0}'.format(note))
            tone = note.diatonic_pitch.diatonic_tone
            octave = note.diatonic_pitch.octave
            assert tone in results
            assert octave in range(2, 9)

        assert len(v_result) == 6 * 3

        for note in v_result:
            parameter_map[upper_context_note].note = note
            assert policy.verify(parameter_map) is True
        logging.debug('End test_is_chordal')

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
