"""

File: time_signature.py

Purpose: Defines TimeSignature and TSBeatType

"""
from fractions import Fraction
from enum import Enum


class TSBeatType:
    """
    Enum class for standard beat types/durations.
    Standard duration notes are Whole, Half, Quarter, Eighth, Sixteenth
    """
    Whole, Half, Quarter, Eighth, Sixteenth = range(5)
    
    def __init__(self, btype):
        self.value = btype
        
    def __str__(self):
        if self.value == TSBeatType.Whole:
            return 'Whole'
        if self.value == TSBeatType.Half:
            return 'Half'
        if self.value == TSBeatType.Quarter:
            return 'Quarter'
        if self.value == TSBeatType.Eighth:
            return 'Eighth'
        if self.value == TSBeatType.Sixteenth:
            return 'Sixteenth'
    
    # convert to fractional value.    
    def to_fraction(self):
        if self.value == TSBeatType.Whole:
            return Fraction(1, 1)
        if self.value == TSBeatType.Half:
            return Fraction(1, 2)
        if self.value == TSBeatType.Quarter:
            return Fraction(1, 4)
        if self.value == TSBeatType.Eighth:
            return Fraction(1, 8)
        if self.value == TSBeatType.Sixteenth:
            return Fraction(1, 16)
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return self.__str__().__hash__()
    
    @staticmethod
    def get_fraction_for(ts_beat_type):
        """
        Static method to get beat fraction value for a ts beat type.
        Args:
          ts_beat_type: if integer, turned into TSBeatType based on int.  Otherwise must be a TSBeatType.
          
        Returns: Range for type.
        Exception: on bad argument type.
        """
        if isinstance(ts_beat_type, int):
            ts_beat_type = TSBeatType(ts_beat_type)
        elif not isinstance(ts_beat_type, TSBeatType):
            raise Exception('Illegal argument type for get_fraction_for {0}'.format(type(ts_beat_type)))
        return ts_beat_type.to_fraction()


class BeatType(Enum):
    """
    Enum to provide characterization of beat as strong or weak.
    """
    Strong = 'S'
    Weak = 'W'

    @staticmethod
    def to_beat_type(ltr):
        if ltr == 'S':
            return BeatType.Strong
        if ltr == 'W':
            return BeatType.Weak
        else:
            raise Exception('Illegal BeatType designation \'{0}\''.format(ltr))



class TimeSignature(object):
    """
    Class representation of time signature.
    self.__beats_per_measure: number of beats per measure
    self.__beat_duration: holds the whole-note value (fraction) for the beat duration.
    self.__beat_pattern: string of S, B's length beats_per_measure indicating strong/weak beats (optional)
    """

    S = 'S'  # Strong beat designation
    W = 'W'  # Weak beat designation

    def __init__(self, beats_per_measure, beat_duration, beat_pattern=None):
        """
        Constructor
        Args 
          [0] beats_per_measure (int)
          [1] beat_duration (Fraction, int, Duration, TSBeatType)
          
        When TSBeatType is specified for beat duration, its fraction value is retained only.
        """
        from timemodel.duration import Duration

        if not isinstance(beats_per_measure, int):
            raise Exception('First argument of time signature must be integer')
        self.__beats_per_measure = beats_per_measure
        if isinstance(beat_duration, Fraction):
            self.__beat_duration = Duration(beat_duration)
        elif isinstance(beat_duration, int):
            self.__beat_duration = Duration(Fraction(beat_duration, 1))
        elif isinstance(beat_duration, TSBeatType):
            self.__beat_duration = Duration(beat_duration.to_fraction())
        elif isinstance(beat_duration, Duration):
            self.__beat_duration = beat_duration
        else:
            raise Exception("Second argument of time signature illegal type {0}".format(type(beat_duration)))

        if beat_pattern is not None:
            if not isinstance(beat_pattern, str):
                raise Exception("Beat pattern must be string, not {0}.".format(type(beat_pattern)))
            bp = beat_pattern.upper()
            if len(bp) != beats_per_measure:
                raise Exception("beat pattern must match beats_per_measure as length {0}.".format(beats_per_measure))
            for bt in bp:
                if bt != TimeSignature.S and bt != TimeSignature.W:
                    raise Exception('Beat pattern must only contain \'S\' or \'W\'')
            self.__beat_pattern = bp
        else:
            self.__beat_pattern = None
        
    @property
    def beats_per_measure(self):
        return self.__beats_per_measure
    
    @property
    def beat_duration(self):
        return self.__beat_duration

    @property
    def beat_pattern(self):
        return self.__beat_pattern

    def beats_matching(self, beat_type):
        beat_list = list()
        ltr = beat_type.value
        for i in range(0, len(self.beat_pattern)):
            if self.beat_pattern[i] == ltr:
                beat_list.append(i)
        return beat_list

    def beat_type(self, beat_index):
        if self.beat_pattern is None:
            return None
        if beat_index >= self.beats_per_measure:
            return None
        return BeatType.to_beat_type(self.beat_pattern[beat_index])
    
    def __str__(self):
        return 'TS[{0}, {1}]'.format(self.beats_per_measure, self.beat_duration)
