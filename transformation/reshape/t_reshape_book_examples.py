from fractions import Fraction

from function.generic_univariate_pitch_function import GenericUnivariatePitchFunction
from function.piecewise_linear_function import PiecewiseLinearFunction
from function.scalar_range_interpreter import ScalarRangeInterpreter
from function.chromatic_range_interpreter import ChromaticRangeInterpreter
from instruments.instrument_catalog import InstrumentCatalog
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint
from melody.constraints.pitch_range_constraint import PitchRangeConstraint
from melody.constraints.step_sequence_constraint import StepSequenceConstraint
from melody.structure.melodic_form import MelodicForm
from melody.structure.motif import Motif
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.lite_score import LiteScore
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch

import math


from tonalmodel.pitch_range import PitchRange
from tonalmodel.range import Range
from transformation.reshape.min_curve_fit_filter import MinCurveFitFilter
from transformation.reshape.t_reshape import TReshape

BASE = DiatonicPitch.parse('C:4').chromatic_distance


def create_score(grammar_str, instrument, ts):
    lge = LineGrammarExecutor()
    target_line, target_hct = lge.parse(grammar_str)

    tempo_seq = TempoEventSequence()
    ts_seq = EventSequence()
    tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
    ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

    c = InstrumentCatalog.instance()
    violin = c.get_instrument(instrument)

    return LiteScore(target_line, target_hct, violin, tempo_seq, ts_seq)


def duration_ltr(duration):
    if duration.duration == Fraction(1, 16):
        return 's'
    elif duration.duration == Fraction(3, 16):
        return 'i@'
    elif duration.duration == Fraction(1, 8):
        return 'i'
    elif duration.duration == Fraction(3, 8):
        return 'q@'
    elif duration.duration == Fraction(1, 4):
        return 'q'
    elif duration.duration == Fraction(1, 2):
        return 'h'
    elif duration.duration == Fraction(1):
        return 'w'
    return '>'


def str_line(line):
    notes = line.get_all_notes()
    prior_octave = None
    prior_duration = None
    note_annotations = list()
    for note in notes:
        annotation = ''
        d = duration_ltr(note.duration)
        if d != prior_duration:
            annotation += d
            prior_duration = d
        annotation += str(note.diatonic_pitch.diatonic_tone.diatonic_symbol) if note.diatonic_pitch is not None else 'R'
        o = note.diatonic_pitch.octave if note.diatonic_pitch is not None else prior_octave
        if o != prior_octave:
            annotation += ":" + str(o)
            prior_octave = o
        note_annotations.append(annotation)
    s = ' '.join(annotation for annotation in note_annotations)
    return s

def print_line(line):
    print(str_line(line))

def sinasoidal(v):
    """
    Maps v to a chromatic distance.
    :param v:
    :return:
    [0..1] -->[0..2*PI]-->[0..19] with value added to C:4 absolute chromatic distance.
    """
    return BASE + 19 * math.sin(2 * math.pi * v/3)


def three_sin(v):
    return math.sin(2 * math.pi * v/3)


def simple_reshape_cpf():
    print('----- test_simple_reshape_cpf -----')

    line_str = '{<C-Major: I> iE:4 E E E E E E E <:IV> qE ie e <:V> qe ie e <:VI>  qE E iE E E E}'
    score = create_score(line_str, 'violin', (3, 4, 'sww'))

    all_notes = score.line.get_all_notes()

    # 11 scalar notes to C:4 (0) to G:5 (1) with pitch unit 1/19
    interpreter = ChromaticRangeInterpreter(DiatonicPitch.parse('C:4'), 0, Fraction(1, 19))

    pitch_function = GenericUnivariatePitchFunction(three_sin, Position(0), Position(3), interp=interpreter)

    # The first note should have one of 3 values, C:4, E:4, G:4
    constraints = {
        ChordalPitchConstraint(all_notes[0]),
        ChordalPitchConstraint(all_notes[8]),
        ChordalPitchConstraint(all_notes[11]),
        ChordalPitchConstraint(all_notes[14]),
        PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'E:4')),
    }

    # motif = Motif(score.line, constraints, 'A')
    motif = Motif([all_notes[0], all_notes[8], all_notes[11], all_notes[14]], constraints, 'A')
    melodic_form = MelodicForm([motif])
    t_reshape = TReshape(score, pitch_function, Range(0, 3), melodic_form, True)

    results = t_reshape.apply()

    filter = MinCurveFitFilter(pitch_function, results)
    print('{0} filtered results'.format(len(filter.scored_results)))

    for index in range(0, min(5, len(filter.scored_results))):
        result = filter.scored_results[index]
        print('[{0}] {1} ({2})'.format(index, str_line(result[0].line), result[1]))

    print('Chords: {0}'.format(','.join([str(c) for c in score.hct.hc_list()])))


def reshape_with_spf():
    print('----- test_reshape_with_spf -----')

    line_str = '{<C-Major: I> iE:4 E E E E q@E <:IV> qE ie e <:V> qe ie e <:VI>  qE E iE E E E}'

    score = create_score(line_str, 'piano', (3, 4, 'sww'))

    tonality = score.hct.get_hc_by_position(0).tonality
    all_notes = score.line.get_all_notes()

    # 11 scalar notes to C:4 (0) to G:5 (11) with pitch unit 1/11
    interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('C:4'), 0, Fraction(1, 11))

    pitch_function = GenericUnivariatePitchFunction(three_sin, Position(0), Position(3), False, interpreter)

    # The first note should have one of 3 values, C:4, E:4, G:4
    constraints = {
        ChordalPitchConstraint(all_notes[0]),
        ChordalPitchConstraint(all_notes[6]),
        ChordalPitchConstraint(all_notes[9]),
        ChordalPitchConstraint(all_notes[12]),
        PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'E:4')),
    }

    #motif = Motif(score.line, constraints, 'A')
    motif = Motif([all_notes[0], all_notes[6], all_notes[9], all_notes[12]], constraints, 'A')
    melodic_form = MelodicForm([motif])
    t_reshape = TReshape(score, pitch_function, Range(0, 3), melodic_form, True)

    results = t_reshape.apply()

    filter = MinCurveFitFilter(pitch_function, results)
    print('{0} filtered results'.format(len(filter.scored_results)))

    for index in range(0, min(5, len(filter.scored_results))):
        result = filter.scored_results[index]
        print('[{0}] {1} ({2})'.format(index, str_line(result[0].line), result[1]))


    constraints = {
        ChordalPitchConstraint(all_notes[0]),
        ChordalPitchConstraint(all_notes[4]),
        ChordalPitchConstraint(all_notes[6]),
        ChordalPitchConstraint(all_notes[8]),
        ChordalPitchConstraint(all_notes[12]),
        ChordalPitchConstraint(all_notes[14]),
        PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'G:4')),
        #PitchRangeConstraint([all_notes[4]], PitchRange.create('E:5', 'G:5')),
        #PitchRangeConstraint([all_notes[6]], PitchRange.create('C:5', 'G:5')),
        #PitchRangeConstraint([all_notes[8]], PitchRange.create('C:4', 'G:4')),
        #PitchRangeConstraint([all_notes[12]], PitchRange.create('E:2', 'A:2')),
        #PitchRangeConstraint([all_notes[14]], PitchRange.create('E:2', 'G:2')),
    }

    motif = Motif(score.line, constraints, 'A')
    melodic_form = MelodicForm([motif])
    t_reshape = TReshape(score, pitch_function, Range(0, 3), melodic_form, True)

    results = t_reshape.apply()

    filter = MinCurveFitFilter(pitch_function, results)
    print('{0} filtered results'.format(len(filter.scored_results)))

    for index in range(0, min(5, len(filter.scored_results))):
        result = filter.scored_results[index]
        print('[{0}] {1} ({2})'.format(index, str_line(result[0].line), result[1]))

def reshape_to_scale():
    print('----- test_reshape_to_scale -----')

    line_str = '{<C-Major: I> iE:4 E E E E E E E E E E E E E E E E E E E E E E E wE}'

    score = create_score(line_str, 'violin', (4, 4, 'swww'))

    tonality = score.hct.get_hc_by_position(0).tonality
    all_notes = score.line.get_all_notes()

    plf = PiecewiseLinearFunction([(0, 0), (1, 8), (Fraction(3, 2), 4), (2, 8), (3, 0)])
    for i in range(0, 17):
        x = Fraction(1, 8) * i
        y = plf(x)
        print('({0}, {1})'.format(x, y))
    time_range = Range(0, 3)

    interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('C:4'), 0, 1)

    pitch_function = GenericUnivariatePitchFunction(plf, Position(0), Position(3), False, interpreter)

    constraints = {
        ChordalPitchConstraint(all_notes[0]),
        PitchRangeConstraint([all_notes[0]], PitchRange.create('C:4', 'G:4')),
    }

    #motif = Motif(score.line, constraints, 'A')
    motif = Motif([all_notes[0]], constraints, 'A')
    melodic_form = MelodicForm([motif])
    t_reshape = TReshape(score, pitch_function, time_range, melodic_form, False)

    results = t_reshape.apply()

    filter = MinCurveFitFilter(pitch_function, results)
    print('{0} filtered results'.format(len(filter.scored_results)))

    for index in range(0, min(5, len(filter.scored_results))):
        result = filter.scored_results[index]
        print('[{0}] {1} ({2})'.format(index, str_line(result[0].line), result[1]))

def motif_example():
    print('----- motif_example -----')

    line_str = '{<C-Major: I> iC:4 D E D E E E E C D E D E E E E C D E D E E E E wE}'

    score = create_score(line_str, 'piano', (4, 4, 'swww'))
    tonality = score.hct.get_hc_by_position(0).tonality
    all_notes = score.line.get_all_notes()

    constraints = {
        StepSequenceConstraint([all_notes[0], all_notes[1], all_notes[2], all_notes[3]], [1, 1, -1])
    }
    motif = Motif([all_notes[0], all_notes[1], all_notes[2], all_notes[3]], constraints)
    motif1 = motif.copy_to(all_notes[8])
    motif2 = motif.copy_to(all_notes[16])
    form = MelodicForm([motif, motif1, motif2])

    # 11 scalar notes to C:4 (0) to G:5 (11) with pitch unit 1/11
    interpreter = ScalarRangeInterpreter(tonality, DiatonicPitch.parse('C:4'), 0, Fraction(1, 11))

    pitch_function = GenericUnivariatePitchFunction(three_sin, Position(0), Position(3), False, interpreter)
    t_reshape = TReshape(score, pitch_function, Range(0, 3), form, True)

    results = t_reshape.apply()

    filter = MinCurveFitFilter(pitch_function, results)
    print('{0} filtered results'.format(len(filter.scored_results)))

    for index in range(0, min(5, len(filter.scored_results))):
        result = filter.scored_results[index]
        print('[{0}] {1} ({2})'.format(index, str_line(result[0].line), result[1]))


#simple_reshape_cpf()
reshape_with_spf()
#reshape_to_scale()
#motif_example()
