"""

File: harmonic_context.py

Purpose: Defines a tonality and chord that serves as a reference point for harmonic analysis of a section of music.

"""
from timemodel.duration import Duration
from timemodel.position import Position
from misc.interval import Interval


class HarmonicContext(object):
    """
    Class model for harmonic conext that references a chord and tonality.
    """

    def __init__(self, tonality, chord, duration, position=Position(0)):
        """
        Constructor.
        :param tonality: Tonality
        :param chord: Chord
        :param duration: Duration
        :param position: Position
        """
        self._tonality = tonality
        self._chord = chord
        self._duration = Duration(duration.duration)
        self._position = Position(position.position)

    @property
    def tonality(self):
        return self._tonality

    @property
    def chord(self):
        return self._chord

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, new_duration):
        self._duration = new_duration

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def extent(self):
        return Interval(self.position.position, self.position.position + self.duration.duration)

    def __str__(self):
        return 'h.c.[{0}, {1}, {2}]'.format(self.tonality, self.chord, self.duration)
