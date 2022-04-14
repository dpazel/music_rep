import unittest
import logging

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.harmonictranscription.t_harmonic_transcription import THarmonicTranscription
from transformation.patsub.min_contour_filter import MinContourFilter


class TestTHarmonicTranscription(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mozart(self):
        print('----- test mozart c-minor fantasy parse -----')

        source_expression = '{<C-Natural: i> q@C:4 iEb F# G <C-Natural: iv> Ab C <C-Melodic: V> iB:3}'

        t_sub = THarmonicTranscription.create(source_expression)
        target_harmonic_list = [('A-Melodic:iv', Duration(3, 4)),
                                ('A-Natural:i', Duration(1, 4)),
                                ('A-Melodic:V', Duration(1, 8))]
        target_hct = TestTHarmonicTranscription.build_hct(target_harmonic_list)

        tag_map = {0: DiatonicPitch.parse('D:4')}
        results = t_sub.apply(target_hct, 'B:3', tag_map, t_sub.height + 5)

        TestTHarmonicTranscription.print_results(results, t_sub.source_line)

    @staticmethod
    def build_hct(hc_expressed_list):
        parse_str = '{'
        for t in hc_expressed_list:
            parse_str += '<' + t[0] + '> qC:4 '
        parse_str += '}'

        lge = LineGrammarExecutor()

        _, hct = lge.parse(parse_str)
        new_hct = HarmonicContextTrack()
        for hc, t in zip(hct.hc_list(), hc_expressed_list):
            new_hc = HarmonicContext(hc.tonality, hc.chord, t[1])
            new_hct.append(new_hc)
        return new_hct

    @staticmethod
    def print_results(results, pattern_line):
        min_filter = MinContourFilter(pattern_line, results.pitch_results)
        scored_filtered_results = min_filter.scored_results

        print(len(results.pitch_results))
        for i in range(1, len(results.pitch_results) + 1):
            pmap = results.pitch_results[i - 1]
            target_notes = [k for k in pmap.keys()]
            target_notes = sorted(target_notes, key=lambda tn: tn.get_absolute_position())
            pmap_notes = [pmap[key].note for key in target_notes]
            t = ''
            for j in range(0, len(pmap_notes)):
                if j > 0:
                    t = t + ' ' + TestTHarmonicTranscription.comp(pmap_notes[j - 1].diatonic_pitch,
                                                                  pmap_notes[j].diatonic_pitch) + ' '
                t = t + str(pmap_notes[j].diatonic_pitch)
            print('[{0}]   {1}'.format(i, t))

        print(len(scored_filtered_results))
        for i in range(1, len(scored_filtered_results) + 1):
            line = scored_filtered_results[i - 1][0]
            notes = line.get_all_notes()
            t = ''
            for j in range(0, len(notes)):
                if j > 0:
                    t = t + ' ' + \
                        TestTHarmonicTranscription.comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' '
                t = t + str(notes[j].diatonic_pitch)
            print('[{0}]   {1}  score({2})'.format(i, t, scored_filtered_results[i - 1][1]))

    @staticmethod
    def comp(p1, p2):
        p1_d = p1.chromatic_distance
        p2_d = p2.chromatic_distance
        if p1_d < p2_d:
            return '<'
        elif p1_d > p2_d:
            return '>'
        else:
            return '=='
