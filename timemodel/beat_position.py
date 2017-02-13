"""

File: beat_poition.py

Purpose: Defines a class for representing a (measure, beat_in_measure) position.
         Proper interpretation of BeatPosition requires a TimeSignature entity.

"""


class BeatPosition(object):
    """
    Class that represents a measure/beat location.  
    """

    def __init__(self, measure_number, beat_number):
        """
        Args:
          measure_number:  An integer representing the measure ordinal
          beat_number: A Fraction representing the beat within the measure.
        """
        self.__measure_number = measure_number
        self.__beat_number = beat_number
        
    @property
    def measure_number(self):
        return self.__measure_number
    
    @property
    def beat_number(self):
        return self.__beat_number
    
    def __lt__(self, other):
        return (self.measure_number < other.measure_number) or \
               (self.measure_number == other.measure_number and self.beat_number < other.beat_number)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.measure_number == other.measure_number and self.beat_number == other.beat_number
       
    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)
           
    def __ne__(self, other):
        if other is None:
            return False
        return self.measure_number != other.measure_number or self.beat_number != other.beat_number
    
    def __gt__(self, other):
        if other is None:
            return False
        return not self.__le__(other)
    
    def __ge__(self, other):
        if other is None:
            return False
        return not self.__lt__(other)
    
    def __str__(self):
        return 'BP[{0}, {1}]'.format(self.measure_number, self.beat_number)
