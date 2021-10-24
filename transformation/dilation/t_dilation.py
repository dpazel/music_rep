from transformation.transformation import Transformation

from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmoniccontext.harmonic_context import HarmonicContext
from structure.lite_score import LiteScore
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event_sequence import TimeSignatureEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from timemodel.tempo_event import TempoEvent

from fractions import Fraction

from structure.line import Line
from structure.note import Note
from structure.beam import Beam
from structure.tuplet import Tuplet
from timemodel.duration import Duration


class TDilation(Transformation):
    """
    Class that supports dilation of musical structures.
    """

    def __init__(self, score):
        """
        Constructor.
        :param score: Score containing the melody line to be reversed. (LiteScore)
        """

        self.__score = score
        self.__apply_to_bpm = None
        self.__apply_to_notes = None
        self.__dilation_factor = None

        Transformation.__init__(self)

    @property
    def score(self):
        return self.__score

    @property
    def apply_to_bpm(self):
        return self.__apply_to_bpm

    @property
    def apply_to_notes(self):
        return self.__apply_to_notes

    @property
    def dilation_factor(self):
        return self.__dilation_factor

    def apply(self, dilation_factor=Fraction(1), apply_to_bpm=False, apply_to_notes=False):
        """
        Apply dilation to score.
        :param dilation_factor:  Must be Fraction or int
        :param apply_to_bpm: Apply dilation_factor to BPM
        :param apply_to_notes: If true, apply dilation_factor to all note durations including tempo and ts.
        :return:
        """
        if dilation_factor is None or not (isinstance(dilation_factor, Fraction) or
                                           not isinstance(dilation_factor, int)):
            raise Exception('Illegal dilation factor - must be Fraction or int')

        self.__dilation_factor = dilation_factor
        self.__apply_to_bpm = apply_to_bpm
        self.__apply_to_notes = apply_to_notes

        dilated_hct = self.dilate_hct(self.score.hct)
        dilated_line = self.dilate_line(self.score.line)
        new_tempo_seq = self.dilate_tempo_sequence(self.score.tempo_sequence)
        new_ts_seq = self.dilate_ts_sequence(self.score.time_signature_sequence)

        return LiteScore(dilated_line, dilated_hct, self.score.instrument, new_tempo_seq, new_ts_seq)

    def dilate_hct(self, hct):
        new_hct = HarmonicContextTrack()

        for hc in hct.hc_list():
            new_hc = HarmonicContext(hc.tonality, hc.chord,
                                     hc.duration if not self.apply_to_notes else hc.duration * self.dilation_factor)
            new_hct.append(new_hc)

        return new_hct

    def dilate_tempo_sequence(self, tempo_event_sequence):
        if tempo_event_sequence is None:
            return None
        new_tes = TempoEventSequence()
        tempi_events = tempo_event_sequence.sequence_list
        for tempo_event in tempi_events:
            tempo = tempo_event.object
            t = Tempo(tempo.tempo / self.dilation_factor if self.apply_to_bpm else tempo.tempo,
                      tempo.beat_duration if not self.apply_to_notes
                      else tempo.beat_duration * self.dilation_factor)
            new_te = TempoEvent(t, tempo_event.time * self.dilation_factor if self.apply_to_notes else tempo_event.time)
            new_tes.add(new_te)

        return new_tes

    def dilate_ts_sequence(self, tses_sequence):
        if tses_sequence is None:
            return None
        new_tses = TimeSignatureEventSequence()
        tss = tses_sequence.sequence_list
        for tse in tss:
            ts = tse.object
            t = TimeSignature(ts.beats_per_measure,
                              ts.beat_duration * self.dilation_factor if self.apply_to_notes else ts.beat_duration,
                              ts.beat_pattern if ts.beat_pattern is not None else None)
            new_tse = TimeSignatureEvent(t, tse.time * self.dilation_factor if self.apply_to_notes else tse.time)
            new_tses.add(new_tse)

        return new_tses

    def dilate_line(self, line):
        if self.dilation_factor == Fraction(1) or not self.apply_to_notes:
            return line.clone()

        return self.recursive_dilate(line, dict())

    def recursive_dilate(self, strct, new_to_old_map):
        if isinstance(strct, Note):
            d = strct.base_duration.duration / strct.contextual_reduction_factor
            n = Note(strct.diatonic_pitch,  Duration(d * self.dilation_factor), strct.num_dots)
            new_to_old_map[n] = strct
            return n
        else:
            collect = list()
            for s in strct.sub_notes:
                collect.append(self.recursive_dilate(s, new_to_old_map))

            if isinstance(strct, Beam):
                b = Beam(collect)
                new_to_old_map[b] = strct
                return b
            elif isinstance(strct, Tuplet):
                t = Tuplet(strct.unit_duration * self.dilation_factor, strct.unit_duration_factor, collect)
                new_to_old_map[t] = strct
                return t
            elif isinstance(strct, Line):
                l = Line()
                new_to_old_map[l] = strct
                for s in collect:
                    l.pin(s, new_to_old_map[s].relative_position * self.dilation_factor)
                return l
