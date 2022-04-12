import unittest

from search.melodicsearch.global_search_options import GlobalSearchOptions
from search.melodicsearch.melodic_search import MelodicSearch
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.position import Position


class TestMelodicSearch(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_hct_setup(self):
        print('----- test simple hct setup -----')

        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> qC:4 D}'
        target = '{qC:4 D <E-Major: v> F# <Ab-Minor: ii> Bb C Db <D-Major: I> D E F#}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search_hct(target_hct, GlobalSearchOptions())

        assert answers is not None
        assert 3 == len(answers)
        assert 'C-Major' == str(answers[0][0].tonality)
        assert 'Ab-MelodicMinor' == str(answers[1][0].tonality)
        assert 'D-Major' == str(answers[2][0].tonality)

        for hc in answers:
            print('({0}, {1})'.format(hc[0], hc[1]))
        print('-----')

        answers = search.search_hct(target_hct, GlobalSearchOptions(hct_match_tonality_modality=True))

        assert answers is not None
        assert 2 == len(answers)

        for hc in answers:
            print('({0}, {1})'.format(hc[0], hc[1]))
        print('-----')

        assert 'C-Major' == str(answers[0][0].tonality)
        assert 'D-Major' == str(answers[1][0].tonality)

    def test_multi_hc_pattern_hct(self):
        print('----- test multi hc pattern hct setup -----')

        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> qC:4 D <F-Minor: iv> iBb:5 Db F}'

        # Test one hit
        target = '{qC:4 D <F-Minor: v> C G <Ab-Minor: ii> Bb C Db <D-Major: I> D E F#}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search_hct(target_hct, GlobalSearchOptions(hct_match_tonality_key_tone=True))

        assert answers is not None
        assert 1 == len(answers)
        assert 'C-Major' == str(answers[0][0].tonality)

        # Test two hits
        target = '{qC:4 D <F-Minor: v> C G <Ab-Minor: ii> Bb C Db <D-Major: I> D E F# ' \
                 '<C-Major: I> qC:4 D <F-Minor: v> C G <Ab-Minor: ii> Bb C Db}'
        target_line, target_hct = lge.parse(target)

        answers = search.search_hct(target_hct, GlobalSearchOptions(hct_match_tonality_key_tone=True))

        assert answers is not None
        assert 2 == len(answers)
        assert 'C-Major' == str(answers[0][0].tonality)
        assert 'C-Major' == str(answers[1][0].tonality)

        # Test 3-hc pattern
        pattern = '{<C-Major: I> qC:4 D <F-Minor: iv> iBb:5 Db F <A-Minor: iii> qA:5 C}'
        search = MelodicSearch.create(pattern)

        target = '{qC:4 D <F-Minor: v> C G <Ab-Minor: ii> Bb C Db <C-Major: I> D E F# ' \
                 '<F-Major: I> iC:4 D E <A-Minor: v> qC G A <Ab-Minor: ii> Bb C Db}'
        target_line, target_hct = lge.parse(target)

        answers = search.search_hct(target_hct, GlobalSearchOptions(hct_match_tonality_key_tone=True))

        assert answers is not None
        assert 1 == len(answers)
        assert 'C-Major' == str(answers[0][0].tonality)
        assert Position(7, 4) == answers[0][0].position

    def test_single_hc_pattern_search(self):
        print('----- test_single_hc_pattern_search -----')
        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> qC:4 G iB E:5 C}'
        target = '{<F-Minor: v> qF:4 C:5 iE Ab:5  F C Db <D-Major: I> qD:3 A iC#:4 F#:6 D}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions())
        assert answers is not None
        for i, a in zip(range(1, len(answers) + 1), answers):
            print('[{0}] {1}'.format(i, a))

        assert 2 == len(answers)

        assert Position(0) == answers[0]
        assert Position(9, 8) == answers[1]

    def test_multi_hc_pattern_search(self):
        print('----- test_multi_hc_pattern_search -----')
        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> B:4 E:5 G C}'
        target = '{<F-Minor: v> qF:4 C:5 <C-Major: I> [iC:4 G F A] <G-Major: I> B:4 E:5 G C D}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions())
        assert answers is not None

        print('test_multi_hc_pattern_search - test 1')
        for i, a in zip(range(1, len(answers) + 1), answers):
            print('[{0}] {1}'.format(i, a))

        assert 1 == len(answers)
        assert Position(1, 2) == answers[0]

    def test_structural_match(self):
        print('----- test_structural_match -----')
        lge = LineGrammarExecutor()

        # Used in book
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 F# C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Major: I> qE:5 (I, 2)[iA:5 C:6 F:5]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions())
        assert answers is not None

        print('test_multi_hc_pattern_search - test 2')
        for i, a in zip(range(1, len(answers) + 1), answers):
            print('[{0}] {1}'.format(i, a))

        assert 1 == len(answers)
        assert Position(1, 2) == answers[0]

        # test for non-structural match
        pattern = '{<C-Major: I> iC:4 G F A <G-Major: I> qB:4 (1:12)E:5 G C}'
        target = '{<F-Minor: v> qF:4 C:5 <C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[E:5 G C]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(structural_match=False))
        assert answers is not None
        assert 1 == len(answers)
        assert Position(1, 2) == answers[0]

        # test for illegal non-structural match
        answers = search.search(target_line, target_hct, GlobalSearchOptions(structural_match=True))
        assert answers is not None
        assert 0 == len(answers)

    def test_hct_match_tonality_key_tone(self):
        print('----- test_hct_match_tonality_key_tone book -----')
        lge = LineGrammarExecutor()

        # hct_match_tonality_key_tone=True, and pattern/target are different keys.
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 F# C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Major: I> qE:5 (I, 2)[iA:6 C:7 F:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_tonality_key_tone=True))
        assert answers is not None
        assert 0 == len(answers)

        # Used in book
        # hct_match_tonality_key_tone=True, and pattern/target are same keys.
        target = '{<F-Minor: I> qF:4 C:5 <C-Major: I> [iF:4 C:5 B:4 D:5] <G-Major: I> qE:5 (I, 2)[iA:6 C:7 F#:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_tonality_key_tone=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_hct_match_tonality_modality(self):
        print('----- test_hct_match_tonality_modality -----')
        lge = LineGrammarExecutor()

        # hct_match_tonality_modality=True, and pattern/target are different modalities.
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 G C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Minor: I> qE:5 (I, 2)[iA:6 C:7 F:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_tonality_modality=True))
        assert answers is not None
        assert 0 == len(answers)

        # hct_match_tonality_key_tone=True, and pattern/target are same modalities.
        target = '{<F-Minor: v> qF:4 C:5 <C-Major: I> [iF:4 C:5 B:4 D:5] <A-Major: I> qC#:6 (I, 2)[iF#:6 A D]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_tonality_modality=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_hct_match_relative_chord(self):

        print('----- test_hct_match_relative_chord -----')
        lge = LineGrammarExecutor()

        # hct_match_relative_chord=True, and pattern/target are different chords.
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 G C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Minor: ii> qE:5 (I, 2)[iA:6 C:7 F:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_relative_chord=True))
        assert answers is not None
        assert 0 == len(answers)

        # hct_match_relative_chord=True, and pattern/target are same chords.
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 G C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Minor: i> qEb:5 (I, 2)[iA:6 C:7 F:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(hct_match_relative_chord=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_note_match_scalar_precision(self):

        print('----- test_note_match_scalar_precision -----')
        lge = LineGrammarExecutor()

        # note_match_scalar_precision=True, and pattern/target are different scale degrees on one note.
        pattern = '{<C-Major: I> [iC:4 G F A] <G-Major: I> qB:4 (I, 2)[iE:5 G C]}'
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Minor: ii> qEb:5 (I, 2)[iA:6 C:7 G:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_scalar_precision=True))
        assert answers is not None
        assert 0 == len(answers)

        # note_match_scalar_precision=True, and pattern/target note corrected.
        target = '{<F-Minor: v> qF:4 C:5 <F-Major: I> [iF:4 C:5 Bb:4 D:5] <C-Minor: ii> qEb:5 (I, 2)[iA:6 C:7 F:6]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_scalar_precision=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_note_match_chordal(self):

        print('----- test_note_match_chordal -----')
        lge = LineGrammarExecutor()

        # note_match_chordal=True, and pattern has a chordal note that is not chordal in the pattern.
        #  G in pattern is chordal but A in pattern is not
        pattern = '{<C-Major: I> [iD:4 A G F]}'
        target = '{<F-Minor: v> [iE:4 G A F]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True))
        assert answers is not None
        assert 0 == len(answers)

        target = '{<F-Minor: v> [iE:4 G E D]}'
        target_line, target_hct = lge.parse(target)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_note_match_chordal_precision(self):

        print('----- test_note_match_chordal_precision -----')
        lge = LineGrammarExecutor()

        # note_match_chordal=True, and pattern has a chordal note that is not chordal in the pattern.
        #  E in pattern is chordal @ 3rd but C in target is choral @ 5th is
        pattern = '{<C-Major: I> [iD:4 G   E C:5]}'
        target = '{<F-Minor: v> [iAb:3 G:4 C C:5]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True,
                                                                             note_match_chordal_precision=True))
        assert answers is not None
        assert 0 == len(answers)

        # C --> Ab: both 3rds
        target = '{<F-Minor: v> [iAb:3 G:4 E C:5]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True,
                                                                             note_match_chordal_precision=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_note_match_non_scalar_precision(self):

        print('----- test_note_match_non_scalar_precision -----')
        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> [iD:4 G  F Ab]}'
        target = '{<G-Major: v> [iA:3 D:4 C F]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_non_scalar_precision=True))
        assert answers is not None
        assert 0 == len(answers)

        target = '{<G-Major: v> [iA:3 D:4 C Eb]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_non_scalar_precision=True))
        assert answers is not None
        assert 1 == len(answers)

    def test_note_match_non_scalar_to_scalar(self):

        print('----- test_note_match_non_scalar_to_scalar -----')
        lge = LineGrammarExecutor()

        pattern = '{<C-Major: I> [iC:4 Eb  G B]}'
        target = '{<C-Minor: i> [iC:5 Eb:5 G B]}'
        target_line, target_hct = lge.parse(target)

        search = MelodicSearch.create(pattern)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_non_scalar_to_scalar=False))
        assert answers is not None
        assert 0 == len(answers)

        answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_non_scalar_to_scalar=True))
        assert answers is not None
        assert 1 == len(answers)
