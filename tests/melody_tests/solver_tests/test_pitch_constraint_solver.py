import unittest
from tonalmodel.tonality import Tonality
from harmoniccontext.harmonic_context import HarmonicContext
from melody.constraints.policy_context import PolicyContext
from melody.constraints.contextual_note import ContextualNote
from tonalmodel.modality import ModalityType
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.pitch_range import PitchRange
from structure.note import Note
from melody.constraints.pitch_step_constraint import PitchStepConstraint
from melody.solver.pitch_constraint_solver import PitchConstraintSolver
from collections import OrderedDict
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from melody.constraints.pitch_range_constraint import PitchRangeConstraint
from melody.constraints.equal_pitch_constraint import EqualPitchConstraint
from melody.constraints.relative_diatonic_constraint import RelativeDiatonicConstraint
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint
from tonalmodel.interval import IntervalType, Interval

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from melody.constraints.step_sequence_constraint import StepSequenceConstraint

import logging
import sys
import traceback


class TestPitchConstraintSolver(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    tone_cache = DiatonicToneCache.get_cache()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_for_book_example_1(self):
        print('----- test for book example 1 -----')

        source_instance_expression = '{<A-Major:i> [sA:4 A A A] qA:4 [iA:4 A] <:iv> qA:4 [sA:4 A A A] qA:4}'
        target_instance_expression = '{<G-Major:i> wA:4 <:iv> wA:4}'
        lge = LineGrammarExecutor()

        source_instance_line, source_instance_hct = lge.parse(source_instance_expression)

        actors = source_instance_line.get_all_notes()
        for a in actors:
            print("{0}".format(a))

        target_instance_line, target_instance_hct = lge.parse(target_instance_expression)
        target_hcs = target_instance_hct.hc_list()
        for hc in target_hcs:
            print("{0}".format(hc))

        pitch_range = PitchRange(DiatonicPitch.parse('C:4').chromatic_distance,
                                    DiatonicPitch.parse('C:6').chromatic_distance)
        p_map = OrderedDict()
        for i in range(len(actors)):
            a = actors[i]
            pc = PolicyContext(target_hcs[0] if i < 7 else target_hcs[1], pitch_range)
            lower_cn = ContextualNote(pc)
            p_map[a] = lower_cn

        policies = set()
        policies.add(StepSequenceConstraint([actors[0], actors[1], actors[2], actors[3]], [1, 1, 1]))
        policies.add(ChordalPitchConstraint(actors[0]))
        policies.add(ChordalPitchConstraint(actors[4]))
        policies.add(ChordalPitchConstraint(actors[8]))
        policies.add(StepSequenceConstraint([actors[8], actors[9], actors[10], actors[11]], [1, -1, -1]))
        policies.add(EqualPitchConstraint([actors[0], actors[12]]))
        policies.add(EqualPitchConstraint([actors[4], actors[7]]))
        policies.add(RelativeDiatonicConstraint(actors[4], actors[5], Interval(3, IntervalType.Major), Interval(1, IntervalType.Perfect)))
        policies.add(StepSequenceConstraint([actors[5], actors[6]], [-1]))

        solver = PitchConstraintSolver(policies)

        full_results, partial_results = solver.solve(p_map)
        print('Results has {0} results.'.format(len(full_results)))

        for pm in full_results:
            print("{0}".format(pm))

    def test_for_book_example_2(self):
        print('----- test for book example 2 -----')

        source_instance_expression = '{<C-Major:IV> [sC:5 B:4 A G] qF:4 [sA:4 B C:5 D] qD:5}'
        target_instance_expression = '{<G-Major:V> wA:4}'

        lge = LineGrammarExecutor()

        source_instance_line, source_instance_hct = lge.parse(source_instance_expression)

        actors = source_instance_line.get_all_notes()
        for a in actors:
            print("{0}".format(a))

        target_instance_line, target_instance_hct = lge.parse(target_instance_expression)
        target_hcs = target_instance_hct.hc_list()
        for hc in target_hcs:
            print("{0}".format(hc))

        pitch_range = PitchRange(DiatonicPitch.parse('C:2').chromatic_distance,
                                DiatonicPitch.parse('C:8').chromatic_distance)

        p_map = OrderedDict()
        for i in range(len(actors)):
            a = actors[i]
            pc = PolicyContext(target_hcs[0], pitch_range)
            lower_cn = ContextualNote(pc)
            p_map[a] = lower_cn

        policies = set()
        policies.add(PitchStepConstraint(actors[0], actors[1], 1, PitchStepConstraint.Down))
        policies.add(PitchStepConstraint(actors[1], actors[2], 1, PitchStepConstraint.Down))
        policies.add(PitchStepConstraint(actors[2], actors[3], 1, PitchStepConstraint.Down))
        policies.add(PitchStepConstraint(actors[5], actors[6], 1, PitchStepConstraint.UP))
        policies.add(PitchStepConstraint(actors[6], actors[7], 1, PitchStepConstraint.UP))
        policies.add(PitchStepConstraint(actors[7], actors[8], 1, PitchStepConstraint.UP))
        policies.add(EqualPitchConstraint([actors[3], actors[4]]))
        policies.add(EqualPitchConstraint([actors[8], actors[9]]))
        policies.add(RelativeDiatonicConstraint(actors[4], actors[5], Interval(3, IntervalType.Major), Interval(1, IntervalType.Perfect)))
        policies.add(RelativeDiatonicConstraint(actors[3], actors[8], Interval(5, IntervalType.Perfect), Interval(1, IntervalType.Perfect)))
        policies.add(ChordalPitchConstraint(actors[4]))
        policies.add(ChordalPitchConstraint(actors[9]))

        solver = PitchConstraintSolver(policies)

        full_results, partial_results = solver.solve(p_map)
        print('Results has {0} results.'.format(len(full_results)))

        for pm in full_results:
            print("{0}".format(pm))

    def atest_for_debugging(self):
        logging.debug('Start test_for_debugging')

        p_map, policies = TestPitchConstraintSolver.generate_generic_sample(TestPitchConstraintSolver.example_2)

        solver = PitchConstraintSolver(policies)
        try:
            full_results, partial_results = solver.solve(p_map)
            if full_results is None:
                print("Full Results is None")
            else:
                print("Full Results is not None")
                if len(full_results) == 0:
                    print("Results is empty")
                else:
                    print('Results has {0} results.'.format(len(full_results)))

                    # verify
                    for pm in full_results:
                        for p in policies:
                            if not p.verify(pm.p_map):
                                print('Policy failure: {0}'.format(type(p).__name__))
                                print(pm)
                                continue

                    for pm in full_results:
                        print(pm)
        except Exception as e:
            print(e)
            # print >> sys.stderr, traceback.format_exc()
            traceback.print_exc()

        logging.debug('End test_for_debugging')

    example_1 = [
        [ModalityType.Major, tone_cache.get_tone('C'), 'tIV', 'C:2', 'C:8'],
        [ModalityType.Major, tone_cache.get_tone('G'), 'tV', 'C:2', 'C:8'],
        [['C:6', 'B:5', 'A:5', 'G:5'], ['e', 'e', 'e', 'e']],
        [
            [PitchStepConstraint, [0, 1], 1, PitchStepConstraint.Down],
            [PitchStepConstraint, [1, 2], 1, PitchStepConstraint.Down],
            [PitchStepConstraint, [2, 3], 1, PitchStepConstraint.Down],
            [PitchRangeConstraint, {3}, PitchRange.create('C:4', 'F:4')]
        ]
    ]

    example_2 = [
        [ModalityType.Major, tone_cache.get_tone('C'), 'tIV', 'C:2', 'C:8'],
        [ModalityType.Major, tone_cache.get_tone('G'), 'tV', 'C:2', 'C:8'],
        [['C:5', 'B:4', 'A:4', 'G:4', 'F:4', 'A:4', 'B:4', 'C:5', 'D:5', 'D:5'],
         ['s', 's', 's', 's', 'q', 's', 's', 's', 's', 'q']],
        [
            [PitchStepConstraint, [0, 1], 1, PitchStepConstraint.Down],
            [PitchStepConstraint, [1, 2], 1, PitchStepConstraint.Down],
            [PitchStepConstraint, [2, 3], 1, PitchStepConstraint.Down],
            [PitchStepConstraint, [5, 6], 1, PitchStepConstraint.UP],
            [PitchStepConstraint, [6, 7], 1, PitchStepConstraint.UP],
            [PitchStepConstraint, [7, 8], 1, PitchStepConstraint.UP],
            [EqualPitchConstraint, {3, 4}],
            [EqualPitchConstraint, {8, 9}],
            [RelativeDiatonicConstraint, [4, 5], Interval(3, IntervalType.Major), Interval(1, IntervalType.Perfect)],
            [RelativeDiatonicConstraint, [3, 8], Interval(5, IntervalType.Perfect), Interval(1, IntervalType.Perfect)],
            [ChordalPitchConstraint, [4]],
            [ChordalPitchConstraint, [9]]
        ]
    ]

    @staticmethod
    def generate_generic_sample(sample):
        upper_policy_context = TestPitchConstraintSolver.policy_creator(sample[0][0], sample[0][1],
                                                                        sample[0][2], sample[0][3], sample[0][4])

        lower_policy_context = TestPitchConstraintSolver.policy_creator(sample[1][0], sample[1][1],
                                                                        sample[1][2], sample[1][3], sample[0][4])

        upper_notes = TestPitchConstraintSolver.create_plain_notes(sample[2][0], sample[2][1], upper_policy_context)

        p_map = TestPitchConstraintSolver.create_pmap(upper_notes, lower_policy_context)

        policies = set()
        for i in range(0, len(sample[3])):
            spec = sample[3][i]
            args = []
            if isinstance(spec[1], list):
                for j in range(0, len(spec[1])):
                    args.append(upper_notes[spec[1][j]])
            elif isinstance(spec[1], set):
                actors = list()
                for j in spec[1]:
                    actors.append(upper_notes[j])
                args.append(actors)

            for j in range(2, len(spec)):
                args.append(spec[j])

            # args = [upper_notes[spec[1][0]], upper_notes[spec[1][1]], spec[2], spec[3]]
            policy = (spec[0])(*tuple(args))
            policies.add(policy)

        return p_map, policies

    @staticmethod
    def generate_sample():
        upper_policy_context = \
            TestPitchConstraintSolver.policy_creator(ModalityType.Major,
                                                     TestPitchConstraintSolver.tone_cache.get_tone('C'), 'tIV',
                                                     'C:2', 'C:8')
        lower_policy_context = \
            TestPitchConstraintSolver.policy_creator(ModalityType.Major,
                                                     TestPitchConstraintSolver.tone_cache.get_tone('G'), 'tV',
                                                     'C:2', 'C:8')

        upper_notes = TestPitchConstraintSolver.create_plain_notes(['C:6', 'B:5', 'A:5', 'G:5'], ['e', 'e', 'e', 'e'],
                                                                   upper_policy_context)

        p_map = TestPitchConstraintSolver.create_pmap(upper_notes, lower_policy_context)

        policies = set()
        for i in range(0, len(upper_notes) - 1):
            policies.add(PitchStepConstraint(upper_notes[i], upper_notes[i + 1], 1, PitchStepConstraint.Down))

        return p_map, policies

    @staticmethod
    def create_pmap(upper_notes, lower_policy_context):
        p_map = OrderedDict()
        for s in upper_notes:
            lower_cn = ContextualNote(lower_policy_context)
            p_map[s] = lower_cn
        return p_map

    @staticmethod
    def create_contextual_notes(pitch_list, duration_list, policy_context):
        assert len(pitch_list) == len(duration_list)
        assert len(pitch_list) > 0

        result = []
        for pitch_str, duration_str in zip(pitch_list, duration_list):
            pitch = DiatonicPitch.parse(pitch_str)
            duration = TestPitchConstraintSolver.parse_duration(duration_str)
            note = Note(pitch, duration)
            cn = ContextualNote(policy_context, note)
            result.append(cn)

        return result

    @staticmethod
    def create_plain_notes(pitch_list, duration_list, policy_context):
        assert len(pitch_list) == len(duration_list)
        assert len(pitch_list) > 0

        result = []
        for pitch_str, duration_str in zip(pitch_list, duration_list):
            pitch = DiatonicPitch.parse(pitch_str)
            duration = TestPitchConstraintSolver.parse_duration(duration_str)
            note = Note(pitch, duration)
            result.append(note)

        return result

    @staticmethod
    def parse_duration(txt):
        cap_txt = txt.upper()
        if cap_txt == 'W':
            return Duration(1)
        if cap_txt == 'H':
            return Duration(1, 2)
        if cap_txt == 'Q':
            return Duration(1, 4)
        if cap_txt == 'E':
            return Duration(1, 8)
        if cap_txt == 'S':
            return Duration(1, 16)
        raise Exception('Illegal duration text: {0}'.format(txt))

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
