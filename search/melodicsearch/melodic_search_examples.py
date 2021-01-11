from search.melodicsearch.global_search_options import GlobalSearchOptions
from search.melodicsearch.melodic_search import MelodicSearch
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.position import Position


def basic_search_example():
    print('----- test simple hct setup -----')

    lge = LineGrammarExecutor()

    pattern = '{<C-Major: I> qC:4 D iE F}'
    target = '{qC:4 D iE F <E-Major: v> qF# hG# <Ab-Minor: ii> qAb:3 Cb:4 iDb F <D-Major: I> qD E F#}'
    target_line, target_hct = lge.parse(target)

    search = MelodicSearch.create(pattern)

    answers = search.search(target_line, target_hct)

    assert answers is not None
    assert 2 == len(answers)
    assert Position(0) == answers[0]
    assert Position(3, 2) == answers[1]

    answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True))

    assert answers is not None
    assert 1 == len(answers)
    assert Position(0) == answers[0]

    target = '{qC:4 D iE F <E-Major: v> qF# hG# <Ab-Minor: ii> qBb:3 Cb:4 iDb Eb <D-Major: I> qD E F#}'
    target_line, target_hct = lge.parse(target)

    answers = search.search(target_line, target_hct, GlobalSearchOptions(note_match_chordal=True))

    assert answers is not None
    assert 2 == len(answers)
    assert Position(0) == answers[0]
    assert Position(3, 2) == answers[1]

def structural_match():
    lge = LineGrammarExecutor()

    # test for non-structural match
    pattern = '{<C-Major: I> [iC:4 G F A] <:V> hB:4}'
    target = '{<F-Minor: v> qF:4 C:5 <C-Major: I> iC:4 G F A <:V> hB:4 }'
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

    pattern = '{<C-Major: I> [iC:4 G F A] <:V> qB:4 (I, 2)[E:5 G C]}'
    target = '{<F-Minor: v> qF:4 C:5 <C-Major: I> [iC:4 G F A] <:V> qB:4 (I, 2)[E:5 G C]}'
    target_line, target_hct = lge.parse(target)
    search = MelodicSearch.create(pattern)
    answers = search.search(target_line, target_hct, GlobalSearchOptions(structural_match=True))

    assert answers is not None
    assert 1 == len(answers)

basic_search_example()
structural_match()