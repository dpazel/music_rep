"""
File: diatonic_pitch.py

Purpose: contains the definition of DiatonicPitch as a class.  

"""
import re

from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache


class DiatonicPitch(object):
    """
    Class that encapuslates the idea of a diatonic pitch along with its position on 
      tonal scale.  That is it takes an octave plus a diatonic tone.
      
      Class properties:
      octave:  The octave for this pitch
      diatonic_tone:  The DiatonicTone for this pitch
    """
    
    # Regex used for parsing diatonic pitch.
    DIATONIC_PATTERN = re.compile(r'([A-Ga-g])(bbb|bb|b|###|##|#)?:?([0-8])')

    def __init__(self, octave, diatonic_tone):
        """
        Constructor
      
        Args:
          octave:  integer >=0
          diatonic_tone: tone or letter representation of the diatonic tone, e.g. D#
          
          Note: 
            The tone is relative to the partition based on tonal_offset.  
            So, Cb:4 is really B:3 - however we retain 4 as the partition as Cb is relative to the 4th.
                Same with B#4 which is really C:5, we retain the 4.
            So the partition is not the actual partition, but the relative partition number.
        """
        self.__octave = octave
        
        if isinstance(diatonic_tone, DiatonicTone):
            self.__diatonic_tone = diatonic_tone
        else:
            self.__diatonic_tone = DiatonicFoundation.get_tone(diatonic_tone)
        self.__chromatic_distance = 12 * octave + self.diatonic_tone.tonal_offset
    
    @property
    def octave(self):
        return self.__octave
    
    @property
    def diatonic_tone(self):
        return self.__diatonic_tone
    
    @property
    def chromatic_distance(self):
        return self.__chromatic_distance

    def enharmonics(self):
        return DiatonicFoundation.map_to_diatonic_scale(self.chromatic_distance)
    
    def diatonic_distance(self):
        """
        Note letter distance on the diatonic scale.
        """
        return self.octave * 7 + self.diatonic_tone.diatonic_index
    
    def __str__(self):
        return '{0}:{1}'.format(self.diatonic_tone.diatonic_symbol, self.octave)
    
    def __eq__(self, other):
        if other is None or not isinstance(other, DiatonicPitch):
            return False
        return self.octave == other.octave and self.diatonic_tone == other.diatonic_tone
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if other is None:
            return False
        return self.chromatic_distance < other.chromatic_distance

    def __le__(self, other):
        if other is None:
            return False
        if self.__eq__(other):
            return True
        return self.__lt__(other)
    
    def __hash__(self):
        return self.__str__().__hash__()
    
    @staticmethod   
    def parse(diatonic_pitch_text):
        """
        Parse a textual representation of diatonic pitch
        
        Args:
          diatonic_pitch_text: text representation of diatonic pitch;
          
        Returns:
          (diatonic_tone, octave)
        """
        if not diatonic_pitch_text:
            return None
        m = DiatonicPitch.DIATONIC_PATTERN.match(diatonic_pitch_text)
        if not m:
            return None
        diatonic_tone = DiatonicToneCache.get_tone(m.group(1).upper() + ('' if m.group(2) is None else m.group(2)))
        if not diatonic_tone:
            return None

        return DiatonicPitch(0 if m.group(3) is None else int(m.group(3)), diatonic_tone)

    LTRS = 'CDEFGAB'

    @staticmethod
    def crosses_c(t1, t2, up_down=True):
        """
        Utility method to determine if two tones (within octave) cross C, implying a different octaves.
        :param t1: 
        :param t2: 
        :param up_down: t1 goes to t2 either in increasing (True) or decreasing (False) manner.
        :return: 
        """
        ltr = t1.diatonic_letter.upper() if isinstance(t1, DiatonicTone) else t1.upper()
        i1 = DiatonicPitch.LTRS.index(ltr)
        ltr = t2.diatonic_letter.upper() if isinstance(t2, DiatonicTone) else t2.upper()
        i2 = DiatonicPitch.LTRS.index(ltr)
        if i1 == i2:
            return False
        return up_down if i1 > i2 else not up_down
