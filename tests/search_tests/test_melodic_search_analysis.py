import unittest

from search.melodicsearch.melodic_search_analysis import MelodicSearchAnalysis, NotePairInformation
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.duration import Duration


class TestMelodicSearchAnalysis(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_setup(self):
        print('----- test simple setup -----')

        l = LineGrammarExecutor()

        s = '{qC:4 D:4 [<E-Major: A-Maj> G F A B]}'
        line, hct = l.parse(s)

        analysis = MelodicSearchAnalysis(line, hct)
        hct_annotation = analysis.hct_annotation
        assert hct_annotation is not None
        assert isinstance(hct_annotation, list)
        assert 2 == len(hct_annotation)
        hc_list = hct.hc_list()
        assert hc_list[0] == hct_annotation[0].hc
        assert hc_list[1] == hct_annotation[1].hc
        assert 1 == hct_annotation[0].relative_chord_degree
        assert 4 == hct_annotation[1].relative_chord_degree
        assert Duration(1, 2) == hct_annotation[0].span
        assert Duration(1, 2) == hct_annotation[1].span

        for na in hct_annotation:
            print(na)

        note_annotation_list = analysis.note_annotation
        assert note_annotation_list is not None

        for na in note_annotation_list:
            print(na)

        assert 6 == len(note_annotation_list)
        assert note_annotation_list[0].is_scalar
        assert note_annotation_list[0].is_chordal
        assert note_annotation_list[1].is_scalar
        assert not note_annotation_list[1].is_chordal
        assert not note_annotation_list[2].is_scalar
        assert not note_annotation_list[2].is_chordal
        assert not note_annotation_list[3].is_scalar
        assert not note_annotation_list[3].is_chordal
        assert note_annotation_list[4].is_scalar
        assert note_annotation_list[4].is_chordal
        assert note_annotation_list[5].is_scalar
        assert not note_annotation_list[5].is_chordal
        assert 4 == note_annotation_list[5].scale_degree

        note_pair_annotation_list = analysis.note_pair_annotation
        assert note_pair_annotation_list is not None

        for npa in note_pair_annotation_list:
            print(npa)

        assert 5 == len(note_pair_annotation_list)
        assert '<' == NotePairInformation.rel_pair_symbol(note_pair_annotation_list[0].relationship)
        assert '<' == NotePairInformation.rel_pair_symbol(note_pair_annotation_list[1].relationship)
        assert '>' == NotePairInformation.rel_pair_symbol(note_pair_annotation_list[2].relationship)
        assert '<' == NotePairInformation.rel_pair_symbol(note_pair_annotation_list[3].relationship)
        assert '<' == NotePairInformation.rel_pair_symbol(note_pair_annotation_list[4].relationship)