"""

File: tonality.py

Purpose: to define the Tonality class.

"""
from tonalmodel.modality import ModalityType, Modality
from tonalmodel.modality_factory import ModalityFactory
from tonalmodel.diatonic_tone_cache import DiatonicToneCache


class Tonality(object):
    """
    Tonality is a class that is based on a modality and a root diatonic tone.  So whereas modality might be 'Ionian', 
        tonality would be that, but rooted (first tone) at a given diatonic tone.
    """

    def __init__(self, modality, diatonic_tone):
        """
        Constructor.
        :param modality_type: ModalityType being used.
        :param diatonic_tone: DiatonicTone being used as root.

        diatonic_tone is the modal_index tone into some tonality based on the given modality.

        Note: (Using E Major as an example)
              self.basis_tone: is the tonality first tone, as if modal_index==0. (E)
              self.root_tone: is the tonality first tone with modal_index taken into account. (F#)
        """
        if isinstance(diatonic_tone, str):
            self.__diatonic_tone = DiatonicToneCache.get_tone(diatonic_tone)
        else:
            self.__diatonic_tone = diatonic_tone

        self.__modality_type = modality.modality_type
        self.__modality = modality
        self.__annotation = self.modality.get_tonal_scale(self.diatonic_tone)

        self.__basis_tone = (self.annotation[:-1])[-self.modal_index]

    @staticmethod
    def create(modality_type, diatonic_tone, modal_index=0):
        """
        Constructor.
        :param modality_type: ModalityType being used.
        :param diatonic_tone: DiatonicTone being used as root.
        :param modal_index: (origin 0), which of the tonality's tone is the actual root_tone.
        """
        if isinstance(diatonic_tone, str):
            base_diatonic_tone = DiatonicToneCache.get_tone(diatonic_tone)
        else:
            base_diatonic_tone = diatonic_tone
        return Tonality(ModalityFactory.create_modality(modality_type, modal_index), base_diatonic_tone)

    @staticmethod
    def create_on_basis_tone(basis_tone, modality_type, modal_index=0):
        diatonic_tone = DiatonicToneCache.get_tone(basis_tone) if isinstance(basis_tone, str) else basis_tone

        raw_modality = ModalityFactory.create_modality(modality_type, 0)
        scale = raw_modality.get_tonal_scale(diatonic_tone)
        return Tonality.create(modality_type, scale[modal_index], modal_index)

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
    def root_tone(self):
        return self.__diatonic_tone

    @property
    def basis_tone(self):
        return self.__basis_tone

    @property
    def modal_index(self):
        return self.__modality.modal_index
  
    @property
    def annotation(self):
        return self.__annotation

    @property
    def cardinality(self):
        return self.modality.get_number_of_tones()
    
    def get_tone(self, index):
        if index < 0 or index >= len(self.annotation):
            return None
        return self.annotation[index]
    
    def __str__(self):
        root_info = ' {0}({1})'.format(self.root_tone.diatonic_symbol, self.modal_index) \
            if self.modal_index != 0 else ''
        return '{0}-{1}{2}'.format(self.basis_tone.diatonic_symbol, self.modality.modality_type, root_info)
    
    def get_tone_by_letter(self, letter):
        tones = []
        for tone in self.annotation:
            if tone.diatonic_letter == letter:
                tones.append(tone)
        return tones

    @staticmethod
    def find_tonality(tones):
        modalities = Modality.find_modality(tones)
        answers = list()
        for modality in modalities:
            answers.append(Tonality.create(modality.modality_type, tones[0], modality.modal_index))
        return answers
