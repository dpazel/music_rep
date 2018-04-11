"""

File: instrument.py

Purpose: Defines a particular instrument. 

"""
from tonalmodel.diatonic_pitch import DiatonicPitch
from instruments.instrument_base import InstrumentBase
from tonalmodel.pitch_range import PitchRange


class Instrument(InstrumentBase):
    """
    Class defining a particular instrument, including it written and sounding pitch ranges.
    """

    def __init__(self, name, key, low, high, transpose_up, transpose_interval, parent=None):
        """
        Constructor
        
        Args:
        name:  (String)
        key:   (String) key of the instrument
        low:   (String) low written pitch
        high:  (String) high written pitch
        transpose_up: (boolean) transpose up if true
        transpose_interval: (interval) transpose interval to the diatonic foundation.
        parent:  (InstrumentBase) parent node in tree.
        """
        InstrumentBase.__init__(self, name, parent)
        
        self.__written_low = DiatonicPitch.parse(low)
        self.__written_high = DiatonicPitch.parse(high)
        self.__key = key if key else '' 
        self.__transpose_up = transpose_up 
        self.__transpose_interval = transpose_interval 
        
        # Compute the sounding range for this instrument.
        if self.transpose_interval:
            self.__sounding_low = self.transpose_interval.get_end_pitch(self.written_low) if self.transpose_up else \
                self.transpose_interval.get_start_pitch(self.written_low)
            self.__sounding_high = self.transpose_interval.get_end_pitch(self.written_high) if self.transpose_up else \
                self.transpose_interval.get_start_pitch(self.written_high)
        else:
            self.__sounding_low = self.written_low
            self.__sounding_high = self.written_high
    
    @property
    def key(self):
        return self.__key
    
    @property
    def written_low(self):
        return self.__written_low
    
    @property
    def transpose_up(self):
        return self.__transpose_up
    
    @property
    def transpose_interval(self):
        return self.__transpose_interval
    
    @property
    def written_high(self):
        return self.__written_high
    
    @property
    def sounding_low(self):
        return self.__sounding_low
    
    @property
    def sounding_high(self):
        return self.__sounding_high

    def sounding_pitch_range(self):
        return PitchRange(self.sounding_low.chromatic_distance,
                          self.sounding_high.chromatic_distance)

    def written_pitch_range(self):
        return PitchRange(self.written_low.chromatic_distance,
                          self.written_high.chromatic_distance)

    def __str__(self):
        first = '{0} [{1}-{2}]'.format(self.name, self.written_low, self.written_high)
        
        if self.transpose_interval:
            second = ' {0} {1} [{2}-{3}]'.format(('up' if self.transpose_up else 'down'), self.transpose_interval,
                                                 self.sounding_low, self.sounding_high)
        else:
            second = ''
            
        return first + second
