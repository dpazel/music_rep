
from transformation.dilation.t_dilation import TDilation
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.position import Position
from structure.lite_score import LiteScore
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from instruments.instrument_catalog import InstrumentCatalog

from fractions import Fraction


def bach_example():
    print('----- Bach example French Suite II BWV 813 -----')

    # Minuet MM 1-4 3/4 T.S. 42-46==dotted half  p.46 Bach text
    title = 'Bach, French Suite II BWV 813, MM 1-4 3/4 T.S. 42-46==dotted half f=2 (False, False)'
    bach_line = '{<C-MelodicMinor:i>iG:4 Eb:5 D C B:4 C:5 <:iv> qAb:5 G F iEb:5 D F Eb D C <:V> B:4 A C:5 B:4 A G}'
    lite_score = create_score(bach_line, 'piano', (42, Duration(3, 4)), (3, Duration(1, 4)))

    trans = TDilation(lite_score)

    #  case 0: apply_to_tempo=False stabilize=False
    new_score = trans.apply(Fraction(2), False, False)
    print_score(title, new_score)

    title = 'Bach, French Suite II BWV 813, MM 1-4 3/4 T.S. 42-46==dotted half f=2 (False, True)'

    #  case 0: apply_to_tempo=False stabilize=False
    new_score = trans.apply(Fraction(2), False, True)
    print_score(title, new_score)


def mozart_example():
    print('----- Mozart example Sonata in A KV331 -----')

    # I MM 1-4 6/8 T.S. 42-46==dotted half  p.46 Bach text
    title = 'Mozart, Sonata in A KV331, I, MM 1-4 6/8 T.S. 60==eighth f=1/2 (True, False)'
    mozart_line = '{<A-Major:I>i@C#:5 sD iC# qE iE <:VDom7> i@B:4 sC#:5 iB:4 qD:5 iD <:viMin7> qA:4 iA <:V>qB:4 iB' \
                  '<:I> qC#:5 sE D qC# <:V>iB:4}'
    lite_score = create_score(mozart_line, 'piano', (60, Duration(3, 8)), (6, Duration(1, 8)))
    print_score(title, lite_score)
    trans = TDilation(lite_score)

    #  case 0: apply_to_bpm=True apply_to_notes=False
    new_score = trans.apply(Fraction(1, 2), True, False)
    print_score(title, new_score)

    #  case 0: apply_to_bpm=True apply_to_notes=True
    title = 'Mozart, Sonata in A KV331, I, MM 1-4 6/8 T.S. 60==eighth f=1/2 (True, True)'
    new_score = trans.apply(Fraction(1, 2), True, True)
    print_score(title, new_score)


def crazy_example():
    print('----- Simple example with odd factor -----')

    title = 'Simple example, 4/4 T.S. 60==eighth f=1/4 (True, False)'
    simple_line = '{<C-Major:i>qG:4 E:5 C B:4 <:IV> iA G B C:5 D E F E <:V> qD C iB:4 A B A <:I> wE}'
    lite_score = create_score(simple_line, 'piano', (60, Duration(1, 4)), (4, Duration(1, 4)))
    trans = TDilation(lite_score)

    new_score = trans.apply(Fraction(4, 7), True, False)
    print_score(title, new_score)

    title = 'Simple example, 4/4 T.S. 60==eighth f=1/4 (True, True)'
    new_score = trans.apply(Fraction(4, 7), True, True)
    print_score(title, new_score)

def crazy_example_1():
    print('----- Second Simple example with odd factor used in book -----')

    title = 'Simple example, 4/4 T.S. 60==eighth f=1/4 (True, False)'
    simple_line = '{<F-Major:i>qF:4 F ig a g Bb <:V> qC:5 C E D <:VI> id c d c a:4 g a f <:V> hG}'
    lite_score = create_score(simple_line, 'piano', (90, Duration(1, 4)), (4, Duration(1, 4)))
    trans = TDilation(lite_score)

    new_score = trans.apply(Fraction(4, 7), True, True)
    print_score(title, new_score)

    new_score = trans.apply(Fraction(4, 7), False, True)
    print_score(title, new_score)

    new_score = trans.apply(Fraction(4, 7), True, False)
    print_score(title, new_score)


def print_score(title, lite_score):

    line = lite_score.line
    hct = lite_score.hct
    tempo_event_sequence = lite_score.tempo_sequence
    time_sig_event_sequence = lite_score.time_signature_sequence

    print("=================================================================")
    print(title)
    print()

    print_line(line)
    print_tempo(tempo_event_sequence)
    print_ts(time_sig_event_sequence)
    print_hct(hct)


def print_line(line):
    notes = line.get_all_notes()
    for i in range(0, len(notes)):
        note = notes[i]
        print('[{0}]  {1}({2})'.format(i, note.diatonic_pitch, note.duration))


def print_tempo(tempo_event_sequence):
    tempi_events = tempo_event_sequence.sequence_list
    count = 0
    for tempo_event in tempi_events:
        tempo = tempo_event.object
        print('[{0}] Tempo({1}, {2})'.format(count, tempo.tempo, tempo.beat_duration))
        count = count + 1


def print_hct(hct):
    hcs = hct.hc_list()
    count = 0
    for hc in hcs:
        print('[{0}] HC({1}, {2}, {3}, {4})'.format(count, hc.tonality, hc.chord, hc.duration, hc.position))


def print_ts(time_sig_event_sequence):
    tss = time_sig_event_sequence.sequence_list
    count = 0
    for tse in tss:
        ts = tse.object
        print('[{0}] TS({1}, {2})'.format(count, ts.beats_per_measure, ts.beat_duration))
        count = count + 1


def create_score(line_text, instrument, tmpo, ts):
    """

    :param line_text:
    :param instrument:
    :param tmpo: (bpm, tempo beat duration)
    :param ts: (num beats, ts beat duration)
    :return:
    """
    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_text)

    tempo_seq = TempoEventSequence()
    ts_seq = EventSequence()
    tempo_seq.add(TempoEvent(Tempo(tmpo[0], tmpo[1]), Position(0)))
    ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], ts[1]), Position(0)))

    c = InstrumentCatalog.instance()
    instrument = c.get_instrument(instrument)

    return LiteScore(source_instance_line, source_instance_hct, instrument, tempo_seq, ts_seq)


#bach_example()
mozart_example()
#crazy_example()
#crazy_example_1()
