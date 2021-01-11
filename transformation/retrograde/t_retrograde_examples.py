import logging
from fractions import Fraction

from instruments.instrument_catalog import InstrumentCatalog
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
from transformation.retrograde.t_retrograde import TRetrograde
from misc.interval import Interval as NumericInterval, BoundaryPolicy


def create_score(line_expression, instrument, ts):
    lge = LineGrammarExecutor()
    source_instance_line, source_instance_hct = lge.parse(line_expression)

    tempo_seq = TempoEventSequence()
    ts_seq = EventSequence()
    tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
    ts_seq.add(TimeSignatureEvent(TimeSignature(ts[0], Duration(1, ts[1]), ts[2]), Position(0)))

    c = InstrumentCatalog.instance()
    instrument = c.get_instrument(instrument)

    return LiteScore(source_instance_line, source_instance_hct, instrument, tempo_seq, ts_seq)

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


def simple_melodic_reversal():
    print('----- test simple melodic reversal -----')

    source_instance_expression = '{<C-Major:I> qC:4 D E G <:v> [iD:5 B:4 A G] qC:5 D <:IV> A:4 iF E hC}'

    lite_score = create_score(source_instance_expression, 'piano', (4, 4, 'swww'))

    print('Original Melody: {0}'.format(str_line(lite_score.line)))
    print(lite_score.hct)

    trans = TRetrograde(lite_score)

    print('--- With harmonic reversal ---')
    # melody is reversed, harmony is reversed, so we do not re-fit the melody to harmony
    reversed_line, hct = trans.apply()

    print('With Harmonic Reversal: {0}'.format(str_line(reversed_line)))
    print(str(hct))

    # Keep harmony
    print('--- No harmonic reversal - original harmony ---')
    # melody is reversed, harmony is not; so, we refit melody to harmony.
    reversed_line, hct = trans.apply(False)

    print('Without Harmonic Reversal {0}'.format(str_line(reversed_line)))
    print(str(hct))

    print()

def mozart_kv238_m8_9():
    print('----- test mozart kv238 G-Major reversal -----')

    source_instance_expression = '{<G-Major:I> sD:5 E F# G A B C:6 D <:IV> C B:5 A G <:VDom7> sF# E D C <:I> B:4 D:5 B:4 G <:VDom7> A C:5 A:4 F# }'

    lite_score = create_score(source_instance_expression, 'piano', (3, 4, 'sww'))

    print('Original Melody: {0}'.format(str_line(lite_score.line)))
    print(lite_score.hct)

    trans = TRetrograde(lite_score)
    print('--- With harmonic reversal ---')
    # melody is reversed, harmony is reversed, so we do not re-fit the melody to harmony
    reversed_line, hct = trans.apply()

    print('With Harmonic Reversal {0}'.format(str_line(reversed_line)))
    print(str(hct))

    # Keep harmony
    print('--- No harmonic reversal - original harmony ---')
    # melody is reversed, harmony is not; so, we refit melody to harmony.
    reversed_line, hct = trans.apply(False)

    if reversed_line is None:
        print("No Solution")
        return

    print('Without Harmonic Reversal {0}'.format(str_line(reversed_line)))
    print(str(hct))

    print()


simple_melodic_reversal()
mozart_kv238_m8_9()