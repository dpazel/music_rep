import unittest

from melody.solver.p_map import PMap
from melody.solver.pitch_constraint_solver import PitchConstraintSolver
from structure.line import Line
from timemodel.offset import Offset
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

from collections import OrderedDict

import logging
import sys
import traceback


class TestPMap(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # Note: add -s --nologcapture to 'additional arguments in configuration to see logging

    def test_compute_simple_scale_tones(self):
        logging.debug('Start test_compute_simple_scale_tones')

        lower_policy_context = TestPMap.policy_creator(ModalityType.Major, DiatonicTone('G'), 'tV',
                                                       'C:2', 'C:8')
        upper_pitch_txts = ['C:5', 'D:5', 'E:5', 'G:5', 'B:5', 'C:6', 'B:5', 'G:5', 'E:5', 'D:5', 'C:5', 'C:5']
        actors = list()
        differentials = [1, 1, 2, 2, 1, -1, -2, -2, -1, -1, 0]
        p_map = OrderedDict()
        for pitch_txt in upper_pitch_txts:
            upper_note = Note(DiatonicPitch.parse(pitch_txt), Duration(1, 8))
            lower_note = ContextualNote(lower_policy_context)
            p_map[upper_note] = lower_note
            actors.append(upper_note)

        policy = StepSequenceConstraint(actors, differentials)
        p_map[actors[2]].note = Note(DiatonicPitch.parse('G:5'), Duration(1, 8))

        solver = PitchConstraintSolver([policy])
        results = None
        try:
            results, _ = solver.solve(p_map)
            if results is None:
                print("Results is None")
            else:
                print("Results is not None")
                if len(results) == 0:
                    print("Results is empty")
                else:
                    print('Results has {0} results.'.format(len(results)))

                    # verify
                    for pm in results:
                        if not policy.verify(pm.p_map):
                            print('Policy failure: {0}'.format(type(policy).__name__))
                            print(pm)
                            continue

                    for pm in results:
                        print(pm)

        except Exception as e:
            print(e)
            # print >> sys.stderr, traceback.format_exc()
            traceback.print_exc()

        assert results is not None
        assert len(results) == 1
        pm = next(iter(results))

        answers = ['E:5', 'F#:5', 'G:5', 'B:5', 'D:6', 'E:6', 'D:6', 'B:5', 'G:5', 'F#:5', 'E:5', 'E:5']
        for i in range(0, len(actors)):
            assert str(pm[actors[i]].note.diatonic_pitch) == answers[i]
        print('-----')

        #  Build a line and test apply on pm
        line = Line()
        begin_note = Note(DiatonicPitch.parse('A:2'), Duration(1, 2))
        end_note = Note(DiatonicPitch.parse('B:2'), Duration(1, 2))
        offset = Offset(0)
        line.pin(begin_note, offset)
        offset = offset + begin_note.duration.duration
        for note in actors:
            line.pin(note, offset)
            offset += note.duration.duration
        line.pin(end_note, offset)

        new_line = pm.apply(line)
        assert new_line is not None
        assert new_line != line

        all_notes = new_line.get_all_notes()
        assert len(all_notes) == 2 + len(actors)

        assert str(all_notes[0].diatonic_pitch) == 'A:2'
        assert str(all_notes[-1].diatonic_pitch) == 'B:2'

        for i in range(1, len(all_notes) - 1):
            assert str(all_notes[i].diatonic_pitch) == answers[i - 1]

    def test_create(self):
        music_line = '{<Ab-Major:I> qC:4 D E F <Db-Major:IV> iDb:4 Eb F Gb <C-Major:IV> qE:4 F G A }'
        pr = PitchRange.create('Ab:3', 'C:5')
        pm = PMap.create(music_line, pr)
        assert pm is not None
        assert len(pm.keys()) == 12
        assert pm.actors[11].diatonic_pitch is not None
        assert str(pm.actors[11].diatonic_pitch) == 'A:4'
        assert pm[pm.actors[11]] is not None
        assert pm[pm.actors[11]].policy_context is not None
        assert pm[pm.actors[11]].policy_context.harmonic_context is not None
        assert pm[pm.actors[11]].policy_context.harmonic_context.tonality is not None
        assert str(pm[pm.actors[11]].policy_context.harmonic_context.tonality) == 'C-Major'

        target_harmonic_list = [('A-Melodic:iv', 1),
                                ('A-Natural:i', Duration(1, 4)),
                                ('A-Melodic:V', 1)]
        pm = PMap.create(music_line, pr, target_harmonic_list)
        assert pm is not None
        assert len(pm.keys()) == 12

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
