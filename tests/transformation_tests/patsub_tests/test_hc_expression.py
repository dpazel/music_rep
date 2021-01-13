import unittest
import logging

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.duration import Duration
from transformation.patsub.hc_expression import HCExpression


class TestHCExpression(unittest.TestCase):
    logging.basicConfig(level=logging.INFO)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_parse(self):
        print('----- test simple parse -----')

        hce = TestHCExpression.print_hce('a##')

        assert 'a##' == hce.key
        assert 'Major' == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('a##-Minor')

        assert 'a##' == hce.key
        assert 'MelodicMinor' == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('a##-@3')

        assert 'a##' == hce.key
        assert 3 == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('a##-(@3)')

        assert 'a##' == hce.key
        assert 3 == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('a##-(@3)(5)')

        assert 'a##' == hce.key
        assert 3 == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert '5' == hce.modality_index
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('a##-(@3)(@6)')

        assert 'a##' == hce.key
        assert 3 == hce.key_modality
        assert 'i' == hce.chord_numeral
        assert hce.key_modifier is None
        assert 6 == hce.modality_index
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('C#-Minor:v')

        assert 'C#' == hce.key
        assert 'MelodicMinor' == hce.key_modality
        assert 'v' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('@3-Minor')

        assert 3 == hce.key
        assert 'MelodicMinor' == hce.key_modality
        assert 3 == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert 3 == hce.chord_type

        hce = TestHCExpression.print_hce('@3-Minor:vi')

        assert 3 == hce.key
        assert 'MelodicMinor' == hce.key_modality
        assert 'vi' == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert hce.chord_type is None

        hce = TestHCExpression.print_hce('@3-Minor:@5')

        assert 3 == hce.key
        assert 'MelodicMinor' == hce.key_modality
        assert 5 == hce.chord_numeral
        assert hce.key_modifier is None
        assert hce.modality_index is None
        assert 5 == hce.chord_type

    def test_interpret(self):
        print('----- test interpret -----')
        lge = LineGrammarExecutor()

        s = '{<C-Minor: I> C:4 <D-Major:IV> F A <Bb-Major:V> G D <C-Major:VI> a c b a}'
        line, hct = lge.parse(s)

        hce = TestHCExpression.print_hce('(@1)M:6-(@0)')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'B' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'MelodicMinor' == str(hc.tonality.modality.modality_type)
        assert 4 == hc.chord.chord_template.scale_degree
        assert 'Maj' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('a##-@3')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'A##' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'Major' == str(hc.tonality.modality.modality_type)
        assert 1 == hc.chord.chord_template.scale_degree
        assert 'Maj' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('aM:6-@2')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'F#' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'Major' == str(hc.tonality.modality.modality_type)
        assert 1 == hc.chord.chord_template.scale_degree
        assert 'Maj' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('@0')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'C' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'MelodicMinor' == str(hc.tonality.modality.modality_type)
        assert 1 == hc.chord.chord_template.scale_degree
        assert 'Min' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('@3-Minor:vi')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'C' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'MelodicMinor' == str(hc.tonality.modality.modality_type)
        assert 6 == hc.chord.chord_template.scale_degree
        assert 'Dim' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('@3-Minor:@2')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'C' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'MelodicMinor' == str(hc.tonality.modality.modality_type)
        assert 5 == hc.chord.chord_template.scale_degree
        assert 'Maj' == str(hc.chord.chord_type)

        hce = TestHCExpression.print_hce('@3-Minor:@2Dom7Flat5')
        hc = hce.interpret(hct.hc_list(), Duration(1, 2))
        print(hc)

        assert 'C' == hc.tonality.diatonic_tone.diatonic_symbol
        assert 'MelodicMinor' == str(hc.tonality.modality.modality_type)
        assert 5 == hc.chord.chord_template.scale_degree
        assert 'Dom7Flat5' == str(hc.chord.chord_type)

    @staticmethod
    def print_hce(expression):
        hce = HCExpression.create(expression)
        print('{0} ==> {1}'.format(expression, hce))
        print()
        return hce
