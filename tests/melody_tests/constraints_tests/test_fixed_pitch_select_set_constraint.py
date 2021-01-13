import unittest

from melody.constraints.fixed_pitch_select_set_constraint import FixedPitchSelectSetConstraint
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

import logging
import sys


class TestFixedPitchSelectSetConstraint(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_fixed_pitch(self):
        logging.debug('Start test_simple_fixed_pitch')

        note = Note(DiatonicPitch.parse("C:5"), Duration(1, 4))

        select_notes = {
            'A:5',
            'C:4',
            'Eb:2',
            'F#:6'
        }

        constraint = FixedPitchSelectSetConstraint(note, {DiatonicPitch.parse(p) for p in select_notes})

        policy_context = TestFixedPitchSelectSetConstraint.policy_creator(ModalityType.Major, DiatonicTone('C'), 'tIV',
                                                                          'C:2', 'C:8')
        lower_contextual = ContextualNote(policy_context)
        p_map = PMap()
        p_map[note] = lower_contextual

        v_results = constraint.values(p_map, note)
        assert v_results is not None
        assert len(v_results) == len(select_notes)
        for result in v_results:
            print(str(result))

        assert select_notes == {str(n.diatonic_pitch) for n in v_results}

        assert not constraint.verify(p_map)

        lower_contextual.note = Note(DiatonicPitch.parse('Eb:2'), Duration(1, 4))
        assert constraint.verify(p_map)

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
