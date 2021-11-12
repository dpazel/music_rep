"""
File: T_shift_example.py
Purpose: examples of t_shift applied to a melody.
"""
from fractions import Fraction

from tonalmodel.interval import Interval as TonalInterval
from tonalmodel.modality import ModalityType
from transformation.shift.t_shift import TShift
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor


def duration_ltr(duration):
    if duration.duration == Fraction(1, 8):
        return 'i'
    elif duration.duration == Fraction(1, 4):
        return 'q'
    elif duration.duration == Fraction(1, 2):
        return 'h'
    elif duration.duration == Fraction(1):
        return 'w'
    return '>'


def print_line(line):
    notes = line.get_all_notes()
    for i in range(0, len(notes)):
        note = notes[i]
        print('[{0}]  {1}({2})'.format(i, note.diatonic_pitch, note.duration))

'''        
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
        annotation += str(note.diatonic_pitch.diatonic_tone.diatonic_symbol)
        o = note.diatonic_pitch.octave
        if o != prior_octave:
            annotation += ":" + str(o)
            prior_octave = o
        note_annotations.append(annotation)
    s = ' '.join(annotation for annotation in note_annotations)
    print(s)
'''


def print_hct(hct):
    hcs = hct.hc_list()
    count = 0
    for hc in hcs:
        print('[{0}] HC({1}, {2}, {3}, {4})'.format(count, hc.tonality, hc.chord, hc.duration, hc.position))

'''        
    hc_annotations = list()
    for hc in hct.hc_list():
        s = '<{0}: {1}>({2})'.format(hc.tonality, hc.chord, hc.duration)
        hc_annotations.append(s)
    hcs = ' '.join(hc_str for hc_str in hc_annotations)
    print(hcs)
'''


def simple_shift_example():
    print('----- Simple Shift Example -----')
    source_expression = '{<C-Major: I> iC:4 C qD E <:IV> iF G hA <:V> ig b qf g <:VI> ie e qd ic d <:I> h@c}'

    t_shift = TShift.create(source_expression, TonalInterval.parse('M:3'))
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift up M:3')
    target_line, target_hct = t_shift.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    t_shift = TShift.create(source_expression, TonalInterval.parse('-m:2'))

    target_line, target_hct = t_shift.apply()

    print('Shift down m:2')
    print_line(target_line)
    print_hct(target_hct)
    print()


def shift_change_modality():
    print('----- Shift Change Modality Example -----')
    source_expression = '{<C-Major: I> iC:4 C qD E <:IV> iF G hA <:V> ig b qf g <:VI> ie e qd ic d <:i> h@c}'

    t_shift = TShift.create(source_expression, TonalInterval.parse('P:4'))
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift up P:4, modality MelodicMinor')
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.MelodicMinor)

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift up P:4, modality NaturalMinor')
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.NaturalMinor)

    print_line(target_line)
    print_hct(target_hct)
    print()


def shift_change_modal_index():
    print('----- Shift Change Modal Index Example -----')
    source_expression = '{<C-Major: I> iC:4 C qD E <:IV> iF G hA <:V> ig b qf g <:VI> ie e qd ic d <:i> h@c}'

    t_shift = TShift.create(source_expression)
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift to modal index 4 (Mixolydian)')
    target_line, target_hct = t_shift.apply(modal_index=4)

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift to C as modal index 3 (lydian) on a melodic minor scale (G)')
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.MelodicMinor, modal_index=3)
    print_line(target_line)
    print_hct(target_hct)
    print()


def shift_change_modal_index_modality_and_shift():
    print('----- Shift Change Modal Index, modality, shift Example -----')
    source_expression = '{<C-Major: I> iC:4 C qD E <:IV> iF G hA <:V> ig b qf g <:VI> ie e qd ic d <:i> h@c}'

    t_shift = TShift.create(source_expression)
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift to modal index 1 (dorian)')
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('M:2'), modal_index=1)

    print_line(target_line)
    print_hct(target_hct)
    print()

    t_shift = TShift(target_line, target_hct)

    print('Shift P:4 to modal index 2 (phrygian) of MelodicMinor')
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('P:4'),
                                            range_modality_type=ModalityType.MelodicMinor, modal_index=2)

    print_line(target_line)
    print_hct(target_hct)
    print()


def example():
    print('----- Book example of shifted tonality on modal not 0 -----')
    source_expression = '{<D-Major(1): I> iE:4 F# G A qE B}'

    t_shift = TShift.create(source_expression,
                            TonalInterval.parse('P:4'))
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.MelodicMinor, modal_index=2)
    print(t_shift.source_hct)
    print(target_line)
    print(target_hct)


def example1():
    print('----- Book example of shifted secondary tonality  -----')
    source_expression = '{<C-Major: V/iii> iD#:4 F# G A qD#:5 B:4}'

    t_shift = TShift.create(source_expression, TonalInterval.parse('P:5'))
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.MelodicMinor)
    print(t_shift.source_hct)
    print(target_line)
    print(target_hct)


def example2():
    print('----- Debug meaning of modal index change and hct -----')

    # example tonality with modal index
    # Create a harmonic minor tonality of some basis root which as Mixolydian has F as the root.
    #       The answer is Bb-HarmonicMinor F(4)

    source_expression = '{<C-Major: I> iC:4}'

    t_shift = TShift.create(source_expression)
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift to modal index 4 (Mixolydian)')
    # This makes C the Mixolydian of F-Major
    target_line, target_hct = t_shift.apply(modal_index=4)
    print_line(target_line)
    print_hct(target_hct)
    print()

    # if you wanted G Mixolydian based on C
    print('Shift as if moving tomodal index 4 (Mixolydian) in C')
    target_line, target_hct = t_shift.apply(
           root_shift_interval=TonalInterval.parse('P:5'), modal_index=4)

    print_line(target_line)
    print_hct(target_hct)
    print()


def shift_sequence_tonal_example():
    print('----- Shift sequence tonal example -----')

    source_expression = '{<C-Major: IV> qf:4 a b C:5 <:V/ii> a:4 e:5 id C# <:ii> qd c b:4 a}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(source_expression)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)

    t_shift = TShift.create(source_expression)
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('M:2'),
                                            range_modality_type=ModalityType.MelodicMinor)
    print(target_line)
    print(target_hct)
    print()

    t_shift = TShift(target_line, target_hct)
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('M:2'),
                                            range_modality_type=ModalityType.MelodicMinor)
    print(target_line)
    print(target_hct)
    print()


def shift_sequence_standard_example():
    print('----- Shift sequence standard example -----')

    source_expression = '{<C-Major: IV> sf:4 a b C:5 <:V/ii> sa:4 e:5 tc# b:4 sC#:5 <:ii> sd tc a:4 sb:4 a}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(source_expression)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)

    t_shift = TShift.create(source_expression)
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('M:2'),
                                            range_modality_type=ModalityType.Major)
    print_score('\n[1]: ', target_line, target_hct)

    t_shift = TShift(target_line, target_hct)
    target_line, target_hct = t_shift.apply(root_shift_interval=TonalInterval.parse('M:2'),
                                            range_modality_type=ModalityType.Major)
    print_score('\n[2]: ', target_line, target_hct)


def print_score(separator, line, hct):
    print(separator)
    print_line(line)
    print_hct(hct)
    print()


# simple_shift_example()
# shift_change_modality()
# shift_change_modal_index()
# shift_change_modal_index_modality_and_shift()
# example2()
# example1()
# shift_sequence_tonal_example()
shift_sequence_standard_example()
