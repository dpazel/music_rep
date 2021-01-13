import unittest
import logging

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.patsub.hc_expression import HCExpression
from transformation.patsub.min_contour_filter import MinContourFilter
from transformation.patsub.t_patsub import TPatSub


class TestTPatSub(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mozart(self):
        print('----- test mozart c-minor fantasy parse -----')

        source_instance_expression = '{<A-Major:i> qD:4 E F# <A-Melodic:iv> F# G# A}'
        lge = LineGrammarExecutor()

        source_instance_line, source_instance_hct = lge.parse(source_instance_expression)

        tpat_sub = TPatSub.create('{<C-Major:i> qC:4 D E <C-Melodic:iv> Eb F G}',
                       '{<C-Natural: iv> q@C:4 iEb F# G <C-Natural: vi> Ab C <C-Melodic: V> iB:3}',
                        ['@0-Natural:iv', '@1-Natural:vi', '@1-Melodic:V'])

        tag_map = {0: DiatonicPitch.parse('D:4')}
        results, target_instance_hct = tpat_sub.apply(source_instance_line, source_instance_hct, 'B:3', tag_map, tpat_sub.target_height + 5)

        self.print_results(results, tpat_sub.substitution_pattern.target_pattern_line)

    def print_results(self, results, pattern_line):
        filter = MinContourFilter(pattern_line, results.pitch_results)
        scored_filtered_results = filter.scored_results

        """
        print(len(results.pitch_results))
        for i in range(1, len(results.pitch_results) + 1):
            pmap = results.pitch_results[i - 1]
            target_notes = [k for k in pmap.keys()]
            target_notes = sorted(target_notes, key=lambda tn: tn.get_absolute_position())
            pmap_notes = [pmap[key].note for key in target_notes]
            t = ''
            for j in range(0, len(pmap_notes)):
                if j > 0:
                    t = t + ' ' + self.comp(pmap_notes[j - 1].diatonic_pitch, pmap_notes[j].diatonic_pitch) + ' '
                t = t + str(pmap_notes[j].diatonic_pitch)
            print('[{0}]   {1}'.format(i, t))
        """

        print(len(scored_filtered_results))
        for i in range(1, len(scored_filtered_results) + 1):
            line = scored_filtered_results[i - 1][0]
            notes = line.get_all_notes()
            t = ''
            for j in range(0, len(notes)):
                if j > 0:
                    t = t + ' ' + self.comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' '
                t = t + str(notes[j].diatonic_pitch)
            print('[{0}]   {1}  score({2})'.format(i, t, scored_filtered_results[i - 1][1]))

    def comp(self, p1, p2):
        p1_d = p1.chromatic_distance
        p2_d = p2.chromatic_distance
        if p1_d < p2_d:
            return '<'
        elif p1_d > p2_d:
            return '>'
        else:
            return '=='