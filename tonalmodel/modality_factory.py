"""

File: modality_factory.py

Purpose: Defines the static class ModalityFactory and the static method to create a modality
         by ModalityType

"""

from tonalmodel.modality import Modality
from tonalmodel.diatonic_modality import DiatonicModality
from tonalmodel.whole_tone_modality import WholeToneModality
from tonalmodel.pentatonic_modality import PentatonicModality
from tonalmodel.octatonic_modality import OctatonicModality
from tonalmodel.blues_modality import BluesModality


class ModalityFactory(object):
    """
    Static class of utility method for Modality creation, of the system-based modalities.
    """

    ModalityInitDict = dict()

    @staticmethod
    def register_modality(modality_type, modality_spec):
        if modality_type not in ModalityFactory.ModalityInitDict:
            ModalityFactory.ModalityInitDict[modality_type] = modality_spec

    @staticmethod
    def deregister_modality(modality_type):
        if modality_type in ModalityFactory.ModalityInitDict:
            del ModalityFactory.ModalityInitDict[modality_type]

    @staticmethod
    def is_registered(modality_type):
        return modality_type in ModalityFactory.ModalityInitDict
   
    @staticmethod
    def create_modality(modality_type, modal_index=0):
        """
        Create modality by modality type
        
        Args:
        modality_type: type of modality to create.
        
        Returns: The respective modality object.
        Raises: Exception if type is not recognized.
        
        Note: update this method with each new Modality
        """
        if modality_type in ModalityFactory.ModalityInitDict:
            return Modality(ModalityFactory.ModalityInitDict[modality_type], modal_index)
        '''
        if modality_type == ModalityType.Major:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.NaturalMinor:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MelodicMinor:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.HarmonicMinor:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.HarmonicMajor:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Ionian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Dorian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Phrygian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Lydian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Myxolydian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Aeolian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.Locrian:
            return DiatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.WholeTone:
            return WholeToneModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MajorPentatonic:
            return PentatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.EgyptianPentatonic:
            return PentatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MinorBluesPentatonic:
            return PentatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MajorBluesPentatonic:
            return PentatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MinorPentatonic:
            return PentatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.HWOctatonic:
            return OctatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.WHOctatonic:
            return OctatonicModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MajorBlues:
            return BluesModality.create(modality_type, modal_index)
        if modality_type == ModalityType.MinorBlues:
            return BluesModality.create(modality_type, modal_index)
        raise Exception('Unrecognized modality type {0} in create_modality'.format(modality_type))
        '''


# Register all system modalities.
for key, value in DiatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)
ModalityFactory.ModalityInitDict[WholeToneModality.WHOLE_TONE_SPEC.modality_type] = \
    WholeToneModality.WHOLE_TONE_SPEC
for key, value in PentatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)
for key, value in OctatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)
for key, value in BluesModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)
