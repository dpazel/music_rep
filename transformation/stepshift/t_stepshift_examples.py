from transformation.stepshift.t_stepshift import TStepShift, SecondaryShiftType
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor



def simple_sequence_example():
    print('----- Simple Sequence Example -----')

    line_text = '{<E-Major:I>iE:5 f# G# F# E f# }'
    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)

    trans = TStepShift(source_instance_line, source_instance_hct)

    new_line, new_hct = trans.apply(-1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(-2)
    print_score('\n[2]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(-3)
    print_score('\n[3]: ', new_line, new_hct)

def standard_modulation_example():
    print('----- Standard Modulation Example -----')

    line_text = '{<C-Major:I> (i, 2)[iC:5 E D] <:V/ii> c#:5 b:4 c#:5 e <:ii> f d b:4 a}'
    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)
    trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Standard)

    new_line, new_hct = trans.apply(1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(2)
    print_score('\n[2]: ', new_line, new_hct)

def tonal_modulation_example():
    print('----- Tonal Modulation Example -----')

    #line_text = '{<C-Major:I> (i, 2)[iC:5 E D] <:V/ii> c# b c# e <:ii> f d b:4 a}'
    line_text = '{<C-Major:I> (i, 2)[iC:5 E D] <:V/ii> c#:5 b:4 c#:5 e <:ii> f d b:4 a}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)
    trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)

    new_line, new_hct = trans.apply(1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(2)
    print_score('\n[2]: ', new_line, new_hct)

def tonal_modulation_CMinor_Tonal_example():
    print('----- Tonal Modulation C-Minor Tonal Example -----')

    #line_text = '{<C-MelodicMinor:I>qC:4 Eb G <:V/ii> a c# e <:ii> d f a}'

    line_text = '{<C-MelodicMinor:I> (i, 2)[iC:5 Eb D] <:V/ii> c# b c# e <:ii> f d b:4 a}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)
    trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)

    new_line, new_hct = trans.apply(1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(2)
    print_score('\n[2]: ', new_line, new_hct)

def tonal_modulation_CNaturalMinor_Tonal_example():
    print('----- Tonal Modulation C-NaturalMinor Tonal Example -----')

    # line_text = '{<C-MelodicMinor:I>qC:4 Eb G <:V/ii> a c# e <:ii> d f a}'

    line_text = '{<C-NaturalMinor:I> (i, 2)[iC:5 Eb D] <:V/ii> c#:5 B:4 c#:5 e <:ii> f d Bb:4 Ab}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)
    trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)

    new_line, new_hct = trans.apply(1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(2)
    print_score('\n[2]: ', new_line, new_hct)

def tonal_modulation_All_NaturalMinor_Tonal_example():
    print('----- Tonal Modulation C-NaturalMinor Tonal Example -----')

    # line_text = '{<C-MelodicMinor:I>qC:4 Eb G <:V/ii> a c# e <:ii> d f a}'

    line_text = '{<C-NaturalMinor:I> (i, 2)[iC:5 Eb D] <:V/ii-Natural> c:5 Bb:4 c:5 e <:ii> f d Bb:4 Ab}'

    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)
    print_score('\n[0]: ', source_instance_line, source_instance_hct)
    trans = TStepShift(source_instance_line, source_instance_hct, SecondaryShiftType.Tonal)

    new_line, new_hct = trans.apply(1)
    print_score('\n[1]: ', new_line, new_hct)

    new_line, new_hct = trans.apply(2)
    print_score('\n[2]: ', new_line, new_hct)

def print_score(separator, line, hct):
    print(separator)
    print_line(line)
    print_hct(hct)
    print()

def print_line(line):
    notes = line.get_all_notes()
    for i in range(0, len(notes)):
        note = notes[i]
        print('[{0}]  {1}({2})'.format(i, note.diatonic_pitch, note.duration))

def print_hct(hct):
    hcs = hct.hc_list()
    count = 0
    for hc in hcs:
        print('[{0}] HC({1}, {2}, {3}, {4})'.format(count, hc.tonality, hc.chord, hc.duration, hc.position))

#simple_sequence_example()
#standard_modulation_example()
#tonal_modulation_example()
#tonal_modulation_CMinor_Tonal_example()
#tonal_modulation_CNaturalMinor_Tonal_example()
tonal_modulation_All_NaturalMinor_Tonal_example()