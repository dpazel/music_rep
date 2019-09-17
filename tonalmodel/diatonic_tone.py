"""
File: diatonic_tone.py

Purpose: Class defining diatonic tone.

"""
import re


class DiatonicTone(object):
    """
    Class to encapsulate all relevant information to diatonic tone.  This includes
      Parsing the textual representation into tone letter and augmentation.
      Obtaining the semitone offsets for both the letter and the augmentation.
      Obtaining the index of the letter in the diatonic C scale
    """
    
    # Basic diatonic tone letters.
    DIATONIC_LETTERS = list('CDEFGAB')
    
    # Regex used for parsing diatonic pitch.
    DIATONIC_PATTERN_STRING = '([A-Ga-g])(bbb|bb|b|###|##|#)?'
    DIATONIC_PATTERN = re.compile(DIATONIC_PATTERN_STRING)
    
    # Diatonic C scale indices
    DIATONIC_INDEX_MAPPING = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
    # Semitone offsets for all diatonic pitch letters
    CHROMATIC_OFFSETS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    
    # All augmentations in text representation
    AUGMENTATIONS = ('bbb', 'bb', 'b', '', '#', '##', '###')
    AUGMENTATION_OFFSET_MAPPING = {'': 0, 'b': -1, 'bb': -2, 'bbb': -3, '#': 1, '##': 2, '###': 3}

    DIATONIC_OFFSET_ENHARMONIC_MAPPING = {
        0: ['C', 'B#', 'Dbb'],
        1: ['C#', 'B##', 'Db'],
        2: ['D', 'C##', 'Ebb'],
        3: ['D#', 'Eb', 'Fbb'],
        4: ['E', 'D##', 'Fb'],
        5: ['F', 'E#', 'Gbb'],
        6: ['F#', 'E##', 'Gb'],
        7: ['G', 'F##', 'Abb'],
        8: ['G#', 'Ab'],
        9: ['A', 'G##', 'Bbb'],
        10: ['A#', 'Bb', 'Cbb'],
        11: ['B', 'A##', 'Cb']
        }

    def __init__(self, diatonic_name):
        """
        Constructor

        Args:
            diatonic_name: Textual name of the tone.
        """
        diatonic_info = DiatonicTone.parse(diatonic_name)
        if not diatonic_info:
            raise Exception('Illegal diatonic pitch specified {0}'.format(diatonic_name)) 
        
        self.__diatonic_letter = diatonic_info[0]
        self.__augmentation_symbol = diatonic_info[1]
        self.__diatonic_symbol = self.diatonic_letter + self.augmentation_symbol
        
        # diatonic tone offset from C within one octave.
        self.__diatonic_index = DiatonicTone.DIATONIC_INDEX_MAPPING[diatonic_info[0]]

        self.__augmentation_offset = DiatonicTone.AUGMENTATION_OFFSET_MAPPING[self.augmentation_symbol]
        # Full offset from beginning of chromatic partition, this is not the same as placement.
        # Note; This can be < 0 or > 11, , Cb is -1, and B# is 12
        # Note that in DiatonicPitch, this provides the accurate adjustment of chromatic partition (octave) number.
        self.__tonal_offset = DiatonicTone.CHROMATIC_OFFSETS[self.diatonic_letter] + self.augmentation_offset
        
        # This is the absolute tone regardless of chromatic partition, e.g.Cb is 11 or B; B# is 0 or C. 
        self.__placement = (self.tonal_offset if self.tonal_offset >= 0 else self.tonal_offset + 12) % 12
        
    @property
    def diatonic_letter(self):
        return self.__diatonic_letter
    
    @property
    def diatonic_symbol(self):
        return self.__diatonic_symbol
    
    @property
    def augmentation_symbol(self):
        return self.__augmentation_symbol
    
    @property
    def diatonic_index(self):
        return self.__diatonic_index
    
    @property
    def augmentation_offset(self):
        return self.__augmentation_offset
    
    @property
    def tonal_offset(self):
        return self.__tonal_offset
    
    @property
    def placement(self):
        return self.__placement    
    
    def __str__(self):
        return '{0}({1}, {2}, {3}, {4})'.format(self.diatonic_symbol,
                                                self.diatonic_index, self.diatonic_index,
                                                self.tonal_offset, self.augmentation_offset)
    
    def __eq__(self, other):
        if other is None or not isinstance(other, DiatonicTone):
            return False
        return self.diatonic_symbol == other.diatonic_symbol
    
    def __hash__(self):
        return self.diatonic_symbol.__hash__()
    
    def enharmonics(self):
        """
        For this tone, provide a list of enharmonic equivalents.
        
        Args: none
        Return: List of enharmonic diatonic tone names
        """
        offset = self.tonal_offset
        if offset < 0:
            offset += 12
        if offset >= 12:
            offset %= 12
            
        return DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[offset]
     
    @staticmethod
    def enharmonics_for(diatonic_tone):
        """
        Get the enharmonics for a given tone [given as text].
        
        Args:
          diatonic_tone: text represention of diatonic tone.
          
        Return: 
          List of enharmonic diatonic tone names.
        """
        return DiatonicTone(diatonic_tone).enharmonics()    
    
    @staticmethod 
    def get_diatonic_letter(index):
        """
        Get the diatonic letter based in integer index.

        :param index:
        :return:
        """
        return DiatonicTone.DIATONIC_LETTERS[index]  
    
    @staticmethod
    def augmentation(augmentation_dist):
        """
        Get the augmentation symbol based on index based on offset, e.g. _2, _1, 0, 1, 2.

        :param augmentation_dist:
        :return:
        """
        return DiatonicTone.AUGMENTATIONS[augmentation_dist + 3] 
    
    @staticmethod
    def alter_tone_by_augmentation(tone, augmentation_delta):
        """
        Given a tone and a (int) change in augmentation, find the resulting DiatonicTone
        
        Args:
          tone: DiatonicTone
          augmentation_delta: (int) amount of change in augmentation.
          
        Returns:
          DiatonicTone for the altered tone.
        """

        from tonalmodel.diatonic_tone_cache import DiatonicToneCache

        basic_symbol = tone.diatonic_letter
        augmentation = tone.augmentation_offset + augmentation_delta
        basic_symbol, augmentation = DiatonicTone.enharmonic_adjust(basic_symbol, augmentation)
        aug_symbol = DiatonicTone.augmentation(augmentation)
        return DiatonicToneCache.get_cache().get_tone(basic_symbol + aug_symbol)

    @staticmethod
    def enharmonic_adjust(ltr, augmentation):
        '''
        In some cases, symbols like G#### or Abbbbb might come up. This is a check for those rare cases, so
        that enharmonic equivalents can be accessed.
        :param ltr:
        :param augmentation:
        :return:
        '''
        LTRS = 'CDEFGAB'
        POS_INC = [2, 2, 1, 2, 2, 2, 1]
        NEG_INC = [-1, -2, -2, -1, -2, -2, -2]
        if abs(augmentation) <= 3:
            return ltr, augmentation
        if augmentation > 0:
            while augmentation > 2:
                i = LTRS.index(ltr.upper())
                augmentation -= POS_INC[i]
                ltr = LTRS[i + 1] if i < 6 else LTRS[0]
        else:
            while augmentation < -2:
                i = LTRS.index(ltr.upper())
                augmentation -= NEG_INC[i]
                ltr = LTRS[i - 1] if i > 0 else LTRS[6]
        return ltr, augmentation

    
    @staticmethod   
    def parse(diatonic_tone_text):
        """
        Parse a textual representation of diatonic pitch
        
        Args:
          diatonic_tone_text: text representation of diatonic tone.
          
        Returns:
          (letter part upper case, augmentation text)  if no augmentation, return '' for augmentation
        """
        if not diatonic_tone_text:
            return None
        m = DiatonicTone.DIATONIC_PATTERN.match(diatonic_tone_text)
        if not m:
            return None
        return m.group(1).upper(), '' if m.group(2) is None else m.group(2)

    @staticmethod
    def to_upper(diatonic_tone_text):
        parts = DiatonicTone.parse(diatonic_tone_text)
        if parts is None:
            return None
        return parts[0] + parts[1]


    @staticmethod
    def calculate_diatonic_distance(tone1, tone2):
        """
        Diatonic count from tone1 to tone2 (upwards)
        :param tone1:
        :param tone2:
        :return:
        """
        return tone2.diatonic_index - tone1.diatonic_index if tone1.diatonic_index <= tone2.diatonic_index else \
            tone2.diatonic_index - tone1.diatonic_index + 7
