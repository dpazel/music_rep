"""

File: chord.py

Purpose: Defines an abstract class to represent a chord

"""
from abc import ABCMeta, abstractmethod


class Chord(object):
    """
    Chords have several key ingredients
    1) chord template
    2) diatonic tonality (sometimes not needed or set to None)
    3) chord type
    4) root_tone
    5) tones
    """
    
    __metaclass__ = ABCMeta

    def __init__(self, chord_template, diatonic_tonality=None):
        """
        Constructor
        Args
          chord_template: ChordTemplate behind the chord.
          diatonic_tonality: DiatonicTonality (optional) that could help define the chord, e.g. by scale + scale degree.
        """
        
        self.__chord_template = chord_template
        self.__diatonic_tonality = diatonic_tonality
        
    @property
    def chord_template(self):
        return self.__chord_template
    
    @property
    def diatonic_tonality(self):
        return self.__diatonic_tonality
    
    @property
    @abstractmethod
    def chord_type(self):
        raise Exception('Chord type subclass needs chord_type property') 
    
    @property
    @abstractmethod
    def root_tone(self):
        raise Exception('Chord type subclass needs root_tone property')
    
    @property
    @abstractmethod
    def tones(self):
        raise Exception('Chord type subclass needs tones property')
