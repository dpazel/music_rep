"""
Examples for harmonic transcription as found in book.

 Why don't the results match those in the book?
 At the time of writing the book, the constraint engine had a bug wherein correct results were generated randomly. This
 was a result of using Python sets which do not have a stable iteration property (successiver iterations on the same
 set can be different). To stabilize the constraint, all usages of set() were replaced with OrderedSet() which is
 stable on iteration. Consequently, searches over large spaces result in different answers, wherein prior, the searches
 could/would start at random places in the search space, and potentially provide better answers that are in the book.

 A proposal is to add futher constraints to contour analysis that deal with successive intervals and not just
 comparative notes.
"""
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

    for j in range(0, len(notes)):
        if j > 0 and notes[j - 1].diatonic_pitch is not None and notes[j].diatonic_pitch is not None:
            t = t + ' ' + comp(notes[j - 1].diatonic_pitch, notes[j].diatonic_pitch) + ' '
        t = t + (str(notes[j].diatonic_pitch) if notes[j].diatonic_pitch is not None else '')
    return t


def print_filtered_results(scored_filtered_results):
    for i in range(1, len(scored_filtered_results) + 1):
        line = scored_filtered_results[i - 1][0]
        print('[{0}]   {1}  score({2})'.format(i, generate_comparative_line(line), scored_filtered_results[i - 1][1]))


def schubert_D946():
    print('----- test schubert D946 -----')

    source_expression = '{<Eb-Major: I> q@Bb:4 <:I> iBb Eb:5 D <:I> ' \
                        'q@Eb iBb:4 iBb Bb <:I> qG <:IV> iAb <:I> Bb Ab G <:I> q@G <:V> F}'
    t_sub = THarmonicTranscription.create(source_expression)

    target_harmonic_list = [('C-Major:I', Duration(3, 8)),
                            ('C-Major:VDom7', Duration(3, 8)),
                            ('C-Major:IV', Duration(3, 4)),
                            ('C-Major:VI', Duration(1, 4)),
                            ('C-Major:IV', Duration(1, 8)),
                            ('C-Major:I', Duration(3, 8)),
                            ('C-Major:V', Duration(3, 8)),
                            ('C-Major:VI', Duration(1, 4)),
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('G:4')}

    results = t_sub.apply(target_hct, 'A:3', tag_map, t_sub.height + 15, 100, Interval(4, IntervalType.Perfect))

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)


def mozart_c_minor_example_with_italian():
    print('----- test mozart c-minor fantasy with Italian -----')

    source_expression = '{<C-Natural: i> q@C:4 iEb <C-Natural: C-It> F# G Ab C <C-Melodic: V> iB:3}'

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


def schubert_a_major_D959_v1():
    print('----- test schubert D959 A-Major V1 -----')

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


def schubert_a_major_D959_v2():
    print('----- test schubert D959 A-Major V2 -----')

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


def mozart_GMajor_KV283():
    print('----- test mozart KV283 -----')

    #  D:5 < E:5 < G:5 < A:5 < C:6 < D:6 < E:6 < F#:6 > D:6 > C:6 > Bb:5 > A:5 > G:5 > F:5 >
    #  E:5 > D:5 > C#:5 < E:5 > C#:5 > A:4 < B:4 < D:5 > B:4 > G:4 < A:4  score(14)

    source_expression = '{<G-Major: I> sD:5 E F# G A B C:6 D <:IV> sC:6 B:5 A G F# E D C <:I> ' \
                        'sB:4 D:5 B:4 G <:VDom7> A C:5 A:4 F#  <:I> qG}'
    t_sub = THarmonicTranscription.create(source_expression)
    target_harmonic_list = [('G-Melodic:v', Duration(1, 2)),
                            ('D-Natural:i', Duration(1, 2)),
                            ('D-Major:V', Duration(1, 4)),
                            ('D-Major:IV', Duration(1, 4)),
                            ('A-Melodic:i', Duration(1, 4))
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('D:5')}
    results = t_sub.apply(target_hct, 'F#:4', tag_map, t_sub.height + 4, 20, tunnel_half_interval=Interval(3, IntervalType.Major))

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)


def mozart_GMajor_KV283_with_step_sequence_motif():
    print('----- test mozart KV283 with motif-----')
    '''
    The idea is to make the first 8 notes scalar. This cannot be done since the 6th note is flagged to be chordal and
    no chordal pitch on the 6th note lies on a scalar path from the initial D:5 assignment - using G-melodic
    as the tonality.
    '''
    from melody.constraints.step_sequence_constraint import StepSequenceConstraint
    from melody.structure.motif import Motif
    from melody.structure.melodic_form import MelodicForm

    source_expression = '{<G-Major: I> sD:5 E F# G A B C:6 D }'
    lge = LineGrammarExecutor()

    source_line, source_hct = lge.parse(source_expression)

    actors = source_line.get_all_notes()

    c = [
        StepSequenceConstraint(actors[0:8], [1, 1, 1, 1, 1, 1, 1])
    ]

    m = Motif(actors, c, 'A')
    melodic_form = MelodicForm([m])

    t_sub = THarmonicTranscription(source_line, source_hct, melodic_form)

    target_harmonic_list = [('G-Melodic:v', Duration(1, 2)),
                            ]
    target_hct = build_hct(target_harmonic_list)

    tag_map = {0: DiatonicPitch.parse('D:5')}
    results = t_sub.apply(target_hct, 'F#:4', tag_map, t_sub.height + 20, 20,
                          tunnel_half_interval=Interval(3, IntervalType.Major))

    results_filter = MinContourFilter(t_sub.source_line, results.pitch_results)
    scored_filtered_results = results_filter.scored_results

    print('Original line:')
    print('      ' + generate_comparative_line(t_sub.source_line))

    print_filtered_results(scored_filtered_results)

# in text
# schubert_D946()

# Examples
# mozart_c_minor_example_with_italian()
# schubert_a_major_D959_v1()
# schubert_a_major_D959_v2()
# mozart_GMajor_KV283()
# mozart_GMajor_KV283_with_step_sequence_motif()
