"""

File: position_delta_info.py

Purpose: Contextual object used by BeatCoverageEngine to solve OnBeatConstraints.

"""
from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from structure.abstract_note_collective import AbstractNoteCollective
from structure.line import Line
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from timemodel.event_sequence import EventSequence


class PositionDeltaInfo(object):
    """
    This class hold information about the movement of various note structures in a line that in sum
    make all the OnBeat constraints work. This class not only records those movements, but is able to either
    create an image of the orignal line with movements made, or alter the original with the movements.
    """

    def __init__(self, coverage_node_list, tempo_seq, ts_seq, hct, line):
        """
        Constructor
        :param coverage_node_list: List of note structures that are affected by on beat constraints.
        :param tempo_seq: TempoEventSequence
        :param ts_seq: EventSequence of TimeSignatures
        :param hct: HarmonicContextTrack
        :param line: Line
        """
        self.__coverage_node_list = coverage_node_list

        self.__coverage_node_aggregates = dict()
        self.__coverage_node_deltas = dict()

        # duplicate time signature event sequence
        new_ts_list = []
        for e in ts_seq.sequence_list:
            new_ts_list.append(TimeSignatureEvent(TimeSignature(e.object.beats_per_measure, e.object.beat_duration,
                                                                e.object.beat_pattern),
                                                  e.time))
        self.__ts_event_sequence = EventSequence(new_ts_list)

        # duplicate tempo event sequence
        new_tempo_list = []
        for e in tempo_seq.sequence_list:
            new_tempo_list.append(TempoEvent(Tempo(e.object.tempo, e.object.beat_duration), e.time))
        self.__tempo_event_sequence = TempoEventSequence(new_tempo_list)

        self.__line = line

        self.__hct = HarmonicContextTrack()
        for hc in hct.hc_list():
            self.__hct.append(HarmonicContext(hc.tonality, hc.chord, Duration(hc.duration), Position(hc.position)))

        for n in self.coverage_node_list:
            self.__coverage_node_aggregates[n] = 0
            self.__coverage_node_deltas[n] = 0

    @property
    def coverage_node_list(self):
        return self.__coverage_node_list

    @property
    def line(self):
        return self.__line

    @property
    def hct(self):
        return self.__hct

    @property
    def ts_event_sequence(self):
        return self.__ts_event_sequence

    @property
    def tempo_event_sequence(self):
        return self.__tempo_event_sequence

    @property
    def coverage_node_deltas(self):
        return self.__coverage_node_deltas

    def line_duration(self):
        return Duration(self.correct_position(self.line.duration).position)

    def correct_position(self, position):
        # Adjust position by the set aggregates on structure.
        p_prime = Position(position)
        for cover in self.coverage_node_list:
            if cover.get_absolute_position() > p_prime:
                break
            p_prime = p_prime + self.coverage_node_deltas[cover]
        return p_prime

    def alter_at(self, cover, delta):
        self.coverage_node_deltas[cover] = delta.duration

        changed = list()
        for tse in self.ts_event_sequence.sequence_list:
            if tse.time >= self.correct_position(cover.get_absolute_position()) - delta.duration:
                changed.append(tse)

        for tse in changed:
            self.ts_event_sequence.remove(tse)
            tse.time += delta
            self.ts_event_sequence.add(tse)

        changed = list()
        for te in self.tempo_event_sequence.sequence_list:
            if te.time >= self.correct_position(cover.get_absolute_position()) - delta.duration:
                changed.append(te)

        for te in changed:
            self.tempo_event_sequence.remove(te)
            te.time += delta
            self.tempo_event_sequence.add(te)

        cover_start_position = self.correct_position(cover.get_absolute_position()) - delta.duration
        hc = self.hct[cover_start_position]
        if hc is not None:
            hc.duration = hc.duration + delta
            hc_list = self.hct.hc_list()
            index = hc_list.index(hc)
            for i in range(index + 1, len(hc_list)):
                hc_list[i].position = hc_list[i].position + delta
            self.hct.reset()

    def apply(self, line_copy=True):
        if line_copy:
            line = self.line.clone()
            line_map = self.map_lines(dict(), self.line, line)
        else:
            line = self.line
            line_map = None

        all_notes = sorted(self.line.get_all_notes(), key=lambda z: z.get_absolute_position())
        delta_sum = 0
        index = 0
        while index < len(all_notes):
            note = all_notes[index]
            cover = PositionDeltaInfo._compute_cover(note)
            if cover in self.coverage_node_list:
                delta_sum += self.coverage_node_deltas[cover]

            if delta_sum != 0:
                cover_prime = line_map[cover] if line_copy else cover
                new_rel_pos = cover_prime.relative_position + delta_sum
                parent = cover_prime.parent
                parent.unpin(cover_prime)
                parent.pin(cover_prime, new_rel_pos)
            index += len(cover.get_all_notes())

        return line

    @staticmethod
    def _compute_cover(note):
        c = note
        while not isinstance(c.parent, Line):
            c = c.parent
        return c

    def map_lines(self, line_map, p1, p2):
        line_map[p1] = p2
        if isinstance(p1, AbstractNoteCollective):
            for from_note, to_note in zip(p1.sub_notes, p2.sub_notes):
                self.map_lines(line_map, from_note, to_note)
        return line_map

    def clone(self):
        c = PositionDeltaInfo(self.coverage_node_list, self.tempo_event_sequence, self.ts_event_sequence,
                              self.hct, self.line)
        for n in self.coverage_node_list:
            c.__coverage_node_aggregates[n] = self.__coverage_node_aggregates[n]
            c.__coverage_node_deltas[n] = self.__coverage_node_deltas[n]
        return c

    def __str__(self):
        str_list = list()
        for key, value in self.coverage_node_deltas.items():
            str_list.append('{0} ==> {1}'.format(key, value))
        return '\n'.join(s for s in str_list)
