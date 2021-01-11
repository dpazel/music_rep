from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from transformation.harmonictranscription.t_harmonic_transcription import THarmonicTranscription
from timemodel.duration import Duration
from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.patsub.min_contour_filter import MinContourFilter
from tonalmodel.interval import Interval, IntervalType


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


def comp(p1, p2):
    p1_d = p1.chromatic_distance
    p2_d = p2.chromatic_distance
    if p1_d < p2_d:
        return '<'
    elif p1_d > p2_d:
        return '>'
    else:
        return '=='


def generate_comparative_line(line):
    notes = line.get_all_notes()
    t = ''

    #s = ' '.join(comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' ' + str(notes[j].diatonic_pitch) for j in range(0, len(notes)) if j > 0 and notes[j - 1].diatonic_pitch is not None and notes[j].diatonic_pitch is not None)
    #return s

    for j in range(0, len(notes)):
        if j > 0 and notes[j - 1].diatonic_pitch is not None and notes[j].diatonic_pitch is not None:
            t = t + ' ' + comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' '
        t = t + (str(notes[j].diatonic_pitch) if notes[j].diatonic_pitch is not None else '')
    return t


def print_filtered_results(scored_filtered_results):
    for i in range(1, len(scored_filtered_results) + 1):
        line = scored_filtered_results[i - 1][0]
        print('[{0}]   {1}  score({2})'.format(i, generate_comparative_line(line), scored_filtered_results[i - 1][1]))


def mozart_c_minor_example():
    print('----- test mozart c-minor fantasy parse -----')

    source_expression = '{<C-Natural: i> q@C:4 iEb F# G <C-Natural: iv> Ab C <C-Melodic: V> iB:3}'

    t_sub = THarmonicTranscription.create(source_expression)
    target_harmonic_list = [('A-Melodic:iv', Duration(3, 4)),
                            ('A-Natural:i', Duration(1, 4)),
                            ('A-Melodic:V', Duration(1, 8))]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('D:4')}
    results = t_sub.apply(target_hct, 'B:3', tag_map, t_sub.height + 5, 100)

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)


def schubert_a_major_v1():
    print('----- test schubert A-Major V1 -----')

    source_expression = '{<A-Major: I> qC#:4 hE qa <:V> qA G# <:I> hA <:ii> q@B iB ' \
                        '<E-Major :viiHalfDim7> qC#:5 A:4 <A-Major:I> hA ig# f# e d}'

    t_sub = THarmonicTranscription.create(source_expression)

    target_harmonic_list = [('C-Major:I', Duration(1)),
                            ('C-Major:IV', Duration(1, 2)),
                            ('C-Major:V', Duration(1, 2)),
                            ('C-Major:vi', Duration(1, 2)),
                            ('C-Major:V', Duration(1, 2)),
                            ('C-Major:I', Duration(1)),
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('C:4')}

    results = t_sub.apply(target_hct, 'B:3', tag_map, t_sub.height + 5, 100)

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)


def schubert_a_major_v2():
    print('----- test schubert A-Major V2 -----')

    source_expression = '{<A-Major: I> qC#:4 hE qa <:V> qA G# <:I> hA <:ii> q@B iB ' \
                        '<E-Major :viiHalfDim7> qC#:5 A:4 <A-Major:I> hA ig# f# e d}'

    t_sub = THarmonicTranscription.create(source_expression)

    target_harmonic_list = [('C-Major:V', Duration(3, 4)),
                            ('C-Major:IV', Duration(1, 4)),
                            ('C-Major:I', Duration(1)),
                            ('C-Major:IV', Duration(1, 2)),
                            ('C-Major:I', Duration(1, 2)),
                            ('C-Major:V', Duration(1)),
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('D:4')}

    results = t_sub.apply(target_hct, 'B:3', tag_map, t_sub.height + 5, 100)

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)

def schubert_piece():
    print('----- test schubert piece -----')

    source_expression = '{<Eb-Major: I> q@Bb:4 <:I> iBb Eb:5 D <:I> q@Eb iBb:4 iBb Bb <:I> qG <:IV> iAb <:I> Bb Ab G <:I> q@G <:V> F}'
    t_sub = THarmonicTranscription.create(source_expression)

    target_harmonic_list = [('C-Major:I', Duration(3, 8)),
                            ('C-Major:VDom7', Duration(3, 8)),
                            ('C-Major:IV', Duration(3, 4)),
                            ('C-Major:VI', Duration(1, 4)),
                            ('C-Major:IV', Duration(1, 8)),
                            ('C-Major:I', Duration(3, 8)),
                            ('C-Major:V', Duration(3, 8)),
                            ('C-Major:I', Duration(1, 4)),
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('G:4')}

    results = t_sub.apply(target_hct, 'A:3', tag_map, t_sub.height + 15, 100, Interval(4, IntervalType.Perfect))

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)

#mozart_c_minor_example()
#schubert_a_major_v1()
#schubert_a_major_v2()
schubert_piece()
