"""

File: lite_score.py

Purpose:  A representation of a score with only one line, instrument, plus a harmonic context track. This class
          is a test scaffold class, primarily used for testing transformations or other new ideas.

"""
from timemodel.event_sequence import EventSequence
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from timemodel.position import Position

from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_conversion import TimeConversion


class LiteScore(object):

    def __init__(self, line, harmonic_context_track=None, instrument=None, tempo_seq=None, ts_seq=None):
        self.__line = line
        self.__hct = HarmonicContextTrack() if harmonic_context_track is None else harmonic_context_track
        self.__instrument = instrument

        self.__tempo_sequence = tempo_seq if tempo_seq is not None else TempoEventSequence()
        self.__time_signature_sequence = ts_seq if ts_seq is not None else EventSequence()

    @property
    def line(self):
        return self.__line

    @property
    def hct(self):
        return self.__hct

    @property
    def instrument(self):
        return self.__instrument

    @property
    def duration(self):
        return self.length()

    @property
    def tempo_sequence(self):
        return self.__tempo_sequence

    @property
    def time_signature_sequence(self):
        return self.__time_signature_sequence

    def get_hc_by_position(self, position):
        return self.hct.get_hc_by_position(position)

    def length(self):
        return max(self.line.duration, self.hct.duration)

    def reset_hct(self, new_hct):
        self.__hct = new_hct

    def reset_line(self, line):
        self.__line = line

    def beat_position(self, position):
        """
        Get the beat position corresponding to given position.
        :param position:
        :return: BeatPosition
        """
        conversion = TimeConversion(self.tempo_sequence, self.time_signature_sequence, Position(self.duration.duration))
        return conversion.position_to_bp(Position(position.position))
