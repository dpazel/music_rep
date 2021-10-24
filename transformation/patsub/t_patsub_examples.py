from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.patsub.min_contour_filter import MinContourFilter
from transformation.patsub.substitution_pattern import SubstitutionPattern
from transformation.patsub.t_patsub import TPatSub


def print_hct(hct):
    hc_list = hct.hc_list()

    for i in range(0, len(hc_list)):
        print('[{0}] {1}'.format(i, hc_list[i]))

def comp(p1, p2):
    p1_d = p1.chromatic_distance
    p2_d = p2.chromatic_distance
    if p1_d < p2_d:
        return '<'
    elif p1_d > p2_d:
        return '>'
    else:
        return '=='


def print_results(results, pattern_line):
    if results is None or len(results) == 0:
        print("There are no results")
        return

    print(len(results))
    for i in range(1, len(results) + 1):
        line = results[i - 1][0]
        notes = line.get_all_notes()
        t = ''
        for j in range(0, len(notes)):
            if j > 0:
                t = t + ' ' + comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' '
            t = t + str(notes[j].diatonic_pitch)
        print('[{0}]   {1}  score({2})'.format(i, t, results[i - 1][1]))


def explanation_pattern_example():
    print('----- test explanation pattern example -----')

    pattern_expression = '{<Bb-Major: i> qBb:3 Bb:4 ia sg eb qf <:iv> qEb:4 Eb:5 iD sEb F i@G sG <:iv> sF:5 Eb D C:4 D:5 C:4 G A <:i> hBb}'
    #replacement_expression = '{<Bb-Major: i> qBb:4 Bb:3 <:vi> iD:4 sEb G qf <:v> qF:5 F:4 <:i> iF:5 sEb D i@Bb:4 sG:5}'
    replacement_expression = '{<Bb-Major: i> qBb:4 Bb:3 <:vi> iD:4 sEb G qf <:v> qF:5 F:4 <:i> iF:5 sEb D i@Bb:4 sG:5 <:iv> sEb:4 Eb:5 D C Bb:4 A G F <:I> hBb:3}'

    replacement_hc_expressions = [
        '@0:i',
        '@0:vi',
        '@0:v',
        '@0:i',
        '@0:iv',
        '@0:i',
    ]

    t_pat_sub = TPatSub.create(pattern_expression, replacement_expression, replacement_hc_expressions)

    source_instance_expression = '{<G-Major: i> D:4 D:5 ib:4 sa f qG <:v> qF#:4 F#:5 iB:4 sC:5 D i@F# sF# <:iii> sE D C B:4 C:5 B:4 G B <:V> hC:5}'

    lge = LineGrammarExecutor()
    replacement_instance_line, replacement_instance_hct = lge.parse(source_instance_expression)

    tag_map = {0: DiatonicPitch.parse('D:5')}

    results, replacement_instance_hct = t_pat_sub.apply(replacement_instance_line, replacement_instance_hct, 'C:4', tag_map, t_pat_sub.target_height, 200)

    filter = MinContourFilter(t_pat_sub.substitution_pattern.target_pattern_line, results.pitch_results)
    scored_filtered_results = filter.scored_results

    print_hct(replacement_instance_hct)

    print_results(scored_filtered_results, replacement_instance_line)

def example_pattern_example():
    print('----- test explanation pattern example -----')

    source_expression = '{<C-Major: i> iC:4 C E F hE <:v> iD:4 D G A hB <:VI> iC:5 C B:4 A <:IV> iA:4 A G F <:II> iF:4 F E D <:I> hC:4}'

    replacement_expression = '{<C-Major: i> q@C:4 iD qE <:iv> q@F:4 iG qA <:v> qG:4 D F <G-Melodic:i> q@G:4 iA qBb <:V> qD:5 E F# ' \
                        '<G-Natural:IV> qG:5 Eb C <C-Major:V> q@B:4 iA qG <:VI> q@a iG qE <:IV> qC:4 F D <:I> h@C}'

    replacement_hc_expressions = [
        '@0:i',
        '@0:iv',
        '@0:v',
        '(@0)P:5-Melodic:i',
        '(@0)P:5-Melodic:v',
        '(@0)P:5-Natural:iv',
        '@0:v',
        '@0:vi',
        '@0:iv',
        '@0:i',
    ]

    t_pat_sub = TPatSub.create(source_expression, replacement_expression, replacement_hc_expressions)

    source_instance_expression = '{<F-Major: i> iF:4 F G A hG <:VDom7> iG:4 G A Bb hC <:I> iF:5 F D C <:III> iC:5 C Bb:4 A <:I> iA:4 A G F <:VI> hD:4}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(source_instance_expression)

    tag_map = {0: DiatonicPitch.parse('F:4')}

    results, replacement_instance_hct = t_pat_sub.apply(source_instance_line, source_instance_hct, 'C:4', tag_map, t_pat_sub.target_height + 5, 300)

    filter = MinContourFilter(t_pat_sub.substitution_pattern.target_pattern_line, results.pitch_results)
    scored_filtered_results = filter.scored_results

    print_hct(replacement_instance_hct)

    print_results(scored_filtered_results, source_instance_line)




#explanation_pattern_example()
example_pattern_example()

