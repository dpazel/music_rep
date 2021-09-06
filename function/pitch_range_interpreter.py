"""

File: pitch_range_interpreter.py

Purpose: A PitchRangeInterpreter is an interface for mapping numeric values to pitches.

"""
from abc import ABC, abstractmethod


class PitchRangeInterpreter(ABC):
    """
    A PitchRangeInterpreter is an interface for a function whose utility to to map numeric values to pitches.
    The interface is very abstract on meanin for all of this - but essentially is built around a value to pitch
    mapping.  Reference ScalarRangeInterpreter or ChromaticRangeInterpreter.
    """

    def __init__(self):
        pass

    @abstractmethod
    def eval_as_nearest_pitch(self, v):
        """
        Given a numeric v, find the nearest pitch.
        :param v: A numeric.
        :return: The nearest pitch.
        """
        pass

    @abstractmethod
    def value_for(self, diatonic_pitch):
        """
        The inverse of the pitch to map function - given a pitch, what value maps to it.
        :param diatonic_pitch:
        :return:
        """
        pass

    @abstractmethod
    def eval_as_pitch(self, v):
        """
        For numeric v, find what it maps to.  In some cases, there may be multiple answers if say v's values is
        between 2 nearest pitches.
        :param v:
        :return: A list of nearest pitches.
        """
        pass

    @abstractmethod
    def eval_as_accurate_chromatic_distance(self, v):
        """
        For numeric v, find a 'precise' chromatic distance to which it maps.  'Precise' is an interpretation of
        the implementation class, however it usually means that v is a value in some function range, and we want
        precisely what it maps to in the pitch range. The result can be a real value.
        :param v:
        :return:
        """
        pass