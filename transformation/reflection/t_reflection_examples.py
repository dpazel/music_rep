"""
File: T_reflection_examples.py
Purpose: examples of t_flip applied to a melody.
"""
from fractions import Fraction

from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType
from transformation.reflection.t_chromatic_reflection import TChromaticReflection
from transformation.reflection.t_diatonic_reflection import TDiatonicReflection
from tonalmodel.interval import Interval as TonalInterval
from transformation.shift.t_shift import TShift


def duration_ltr(duration):
    if duration.duration == Fraction(1, 16):
        return 's'
    elif duration.duration == Fraction(3, 16):
        return 'i@'
    elif duration.duration == Fraction(1, 8):
        return 'i'
    elif duration.duration == Fraction(3, 4):
        return 'q@'
    elif duration.duration == Fraction(3, 8):
        return 'i@'
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
        annotation += str(note.diatonic_pitch.diatonic_tone.diatonic_symbol) if note.diatonic_pitch is not None else 'R'
        o = note.diatonic_pitch.octave if note.diatonic_pitch is not None else prior_octave
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


def simple_flip_example():
    source_expression = '{<C-Major: I> iC:4 C qD E <:IV> iF G hA <:V> ig b qf g <:VI> ie e qd ic d <:I> h@c}'

    t_flip = TDiatonicReflection.create(source_expression, DiatonicPitch.parse('F:4'))

    print('Flip examples based on:')
    print_line(t_flip.source_line)
    print_hct(t_flip.source_hct)
    print()

    print('Flip on F:4')
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    t_reflect = TDiatonicReflection.create(source_expression, DiatonicPitch.parse('A:4'))

    target_line, target_hct = t_reflect.apply()

    print('Flip on A:4')
    print_line(target_line)
    print_hct(target_hct)
    print()


def cue_examples():
    source_expression = '{<Bb-Major: I> sBb:4 A G F qEb D sF g iA i@Bb sF <:IVMaj7> ' \
                        'ir Eb sEb F G A iBb sEb:5 F i@Eb C ' \
                        '<:IIIMin7> sR F:5 Eb D C Bb:4 C:5 D i@Eb sC sr G:4 A G <:I> sG:5 F Eb D D C Bb:4 A ir q@G}'

    t_flip = TDiatonicReflection.create(source_expression, DiatonicPitch.parse('Eb:4'))
    print('Flip examples based on:')
    print_line(t_flip.source_line)
    print_hct(t_flip.source_hct)
    print()

    print('Flip on Eb:4')
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift up an octave:')
    t_shift = TShift(target_line, target_hct, TonalInterval.parse('P:8'))
    final_line, final_hct = t_shift.apply()
    print_line(final_line)
    print_hct(final_hct)

def chromatic_reflection():
    print('Chromatic_Reflection')
    source_expression = '{<Bb-Major: I> sBb:4 A G F iEb D sF g iA i@Bb sF <:IVMaj7> ' \
                        'ir Eb sEb F G A iBb sEb:5 F i@Eb C ' \
                        '<:IIIMin7> sR F:5 Eb D C Bb:4 C:5 D i@Eb sC sr G:4 A G <:I> sG:5 F Eb D D C Bb:4 A ir q@G}'

    t_flip = TChromaticReflection.create(source_expression, DiatonicPitch.parse('G:4'))
    print('Flip examples based on:')
    print_line(t_flip.source_line)
    print_hct(t_flip.source_hct)
    print()

    print('Flip on G:4')
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift up an octave:')
    t_shift = TShift(target_line, target_hct, TonalInterval.parse('P:8'))
    final_line, final_hct = t_shift.apply()
    print_line(final_line)
    print_hct(final_hct)

    # Center-Tone to upper
    t_flip = TChromaticReflection.create(source_expression, DiatonicPitch.parse('G:4'), FlipType.UpperNeighborOfPair)
    print('Flip examples based on:')
    print_line(t_flip.source_line)
    print_hct(t_flip.source_hct)
    print()

    print('Upper Flip on G:4')
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift up an octave:')
    t_shift = TShift(target_line, target_hct, TonalInterval.parse('P:8'))
    final_line, final_hct = t_shift.apply()
    print_line(final_line)
    print_hct(final_hct)

   # Center-Tone to lower
    t_flip = TChromaticReflection.create(source_expression, DiatonicPitch.parse('G:4'), FlipType.LowerNeighborOfPair)
    print('Flip examples based on:')
    print_line(t_flip.source_line)
    print_hct(t_flip.source_hct)
    print()

    print('Lower Flip on G:4')
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()

    print('Shift up an octave:')
    t_shift = TShift(target_line, target_hct, TonalInterval.parse('P:8'))
    final_line, final_hct = t_shift.apply()
    print_line(final_line)
    print_hct(final_hct)

def chromatic_book_example():
    print('Chromatic_Reflection')
    source_expression = '{<C-NaturalMinor: I> qC:4 ieb f g ab <:V> Bb ab gc f eb d <:IV> q@f ig eb d ' \
                        '<:VI> q@Eb id eb d <:I> h@c }'

    t_flip = TChromaticReflection.create(source_expression, DiatonicPitch.parse('Ab:4'))
    target_line, target_hct = t_flip.apply()

    print_line(target_line)
    print_hct(target_hct)
    print()


#simple_flip_example()
#cue_examples()
#chromatic_reflection()
chromatic_book_example()