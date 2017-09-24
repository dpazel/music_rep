"""

File: tonality.py

Purpose: to define the Tonality class.

"""
from tonalmodel.modality_factory import ModalityFactory


class Tonality(object):
    """
    Tonality is a class that is based on a modality and a root diatonic tone.  So whereas modality might be 'Ionian', 
        tonality would be that, but rooted (first tone) at a given diatonic tone.
    """

    def __init__(self, modality_type, diatonic_tone):
        """
        Constructor
        
        Args:
          modality_type: ModalityType being used
          diatonic_tone: DiatonicTone being used
        """
        self.__modality_type = modality_type
        self.__modality = ModalityFactory.create_modality(self.modality_type)
        self.__diatonic_tone = diatonic_tone
        self.__annotation = self.modality.get_tonal_scale(self.diatonic_tone)

    @property
    def modality_type(self):
        return self.__modality_type
         
    @property 
    def modality(self):
        return self.__modality
  
    @property
    def diatonic_tone(self):
        return self.__diatonic_tone
  
    @property
    def annotation(self):
        return self.__annotation  
    
    def get_tone(self, index):
        if index < 0 or index >= len(self.annotation):
            return None
        return self.annotation[index]
    
    def __str__(self):
        return '{0}-{1}'.format(self.diatonic_tone, self.modality)
    
    def get_tone_by_letter(self, letter):
        tones = []
        for tone in self.annotation:
            if tone.diatonic_letter == letter:
                tones.append(tone)
        return tones
