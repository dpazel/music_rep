"""
File: T_shift_example.py
Purpose: examples of t_shift applied to a melody.
"""
from fractions import Fraction

from tonalmodel.interval import Interval as TonalInterval
from tonalmodel.modality import ModalityType
from transformation.shift.t_shift import TShift
from tonalmodel.tonality import Tonality

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

def print_hct(hct):
    hc_annotations = list()
    for hc in hct.hc_list():
        s = '<{0}: {1}>({2})'.format(hc.tonality, hc.chord, hc.duration)
        hc_annotations.append(s)
    hcs = ' '.join(hc_str for hc_str in hc_annotations)
    print(hcs)


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

    print('Shift to modal index 4 (mixolydian)')
    target_line, target_hct = t_shift.apply(modal_index=4)

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift to modal index 3 (lydion) on a melodic minor scale')
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
    print('----- Book example of shifted tonality -----')
    source_expression = '{<D-Major(1): I> iC:4 }'

    t_shift = TShift.create(source_expression,
                            TonalInterval.parse('P:4'))
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.MelodicMinor, modal_index=2)
    print(t_shift.source_hct)
    print(target_hct)

def example1():
    print('----- Book example of shifted secondary tonality tonality -----')
    source_expression = '{<C-Major: V/ii> iC:4 }'

    t_shift = TShift.create(source_expression,
                            TonalInterval.parse('M:3'))
    target_line, target_hct = t_shift.apply(range_modality_type=ModalityType.Major, modal_index=0)
    print(t_shift.source_hct)
    print(target_hct)

def example2():
    print('----- Debug meaning of modal index change and hct -----')

    # example tonality with modal index
    # Create a harmonic minor tonality of some basis root which as Mixolydian has F as the root.
    #       The answer is Bb-HarmonicMinor F(4)
    t = Tonality.create(ModalityType.HarmonicMinor, 'F', 4);
    print(t)

    source_expression = '{<C-Major: I> iC:4}'

    t_shift = TShift.create(source_expression)
    print('Shift examples based on:')
    print_line(t_shift.source_line)
    print()

    print('Shift to modal index 4 (mixolydian)')
    # This makes C the mixolydian of F-Major
    target_line, target_hct = t_shift.apply(modal_index=4)
    print_line(target_line)
    print_hct(target_hct)
    print()

    # if you wanted G mixolydian based on C
    print('Shift as if moving tomodal index 4 (mixolydian) in C')
    target_line, target_hct = t_shift.apply(
           root_shift_interval=TonalInterval.parse('P:5'), modal_index=4)

    print_line(target_line)
    print_hct(target_hct)
    print()


simple_shift_example()
shift_change_modality()
shift_change_modal_index()
shift_change_modal_index_modality_and_shift()
example2()