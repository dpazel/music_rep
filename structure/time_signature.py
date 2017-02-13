"""

File: time_signature.py

Purpose: Defines TimeSignature and TSBeatType

"""
from fractions import Fraction


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


class TimeSignature(object):
    """
    Class representation of time signature.
    self.__beats_per_measure: number of beats per measure
    self.__beat_duration: holds the whole-note value (fraction) for the beat duration.
    """

    def __init__(self, *args, **kwargs):
        # args -- tuple of anonymous arguments
        # kwargs -- dictionary of named arguments
        """
        Constructor
        Args 
          [0] beats_per_measure (int)
          [1] beat_duration (Fraction, int, Duration, TSBeatType)
          
        When TSBeatType is specified for beat duration, its fraction value is retained only.
        """
        from timemodel.duration import Duration
        if len(args) == 2:
            if not isinstance(args[0], int):
                raise Exception('First argument of time signature must be integer')
            self.__beats_per_measure = args[0]
            if isinstance(args[1], Fraction):
                self.__beat_duration = Duration(args[1])
            elif isinstance(args[1], int):
                self.__beat_duration = Duration(Fraction(args[1], 1))
            elif isinstance(args[1], TSBeatType):
                self.__beat_duration = Duration(args[1].to_fraction())
            elif isinstance(args[1], Duration):
                self.__beat_duration = args[1]
            else:
                raise Exception("Second argument of time signature illegal type {0}".format(type(args[1])))
        else:
            raise Exception('TimeSignature takes two arguments')
        
    @property
    def beats_per_measure(self):
        return self.__beats_per_measure
    
    @property
    def beat_duration(self):
        return self.__beat_duration
    
    def __str__(self):
        return 'TS[{0}, {1}]'.format(self.beats_per_measure, self.beat_duration)
