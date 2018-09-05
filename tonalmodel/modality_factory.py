"""

File: modality_factory.py

Purpose: Defines the static class ModalityFactory and the static method to create a modality
         by ModalityType

"""

from tonalmodel.modality import ModalityType
from tonalmodel.diatonic_modality import DiatonicModality
from tonalmodel.whole_tone_modality import WholeToneModality
from tonalmodel.pentatonic_modality import PentatonicModality
from tonalmodel.octatonic_modality import OctatonicModality
from tonalmodel.blues_modality import BluesModality


class ModalityFactory(object):
    """
    Static class of utility method(s) for Modality, especially modality creation
    """
   
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
        if modality_type == ModalityType.Major:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.NaturalMinor:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.MelodicMinor:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.HarmonicMinor:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.HarmonicMajor:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Ionian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Dorian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Phrygian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Lydian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Myxolydian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Aeolian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.Locrian:
            return DiatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.WholeTone:
            return WholeToneModality(modality_type, modal_index)
        if modality_type == ModalityType.MajorPentatonic:
            return PentatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.EgyptianPentatonic:
            return PentatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.MinorBluesPentatonic:
            return PentatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.MajorBluesPentatonic:
            return PentatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.MinorPentatonic:
            return PentatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.HWOctatonic:
            return OctatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.WHOctatonic:
            return OctatonicModality(modality_type, modal_index)
        if modality_type == ModalityType.MajorBlues:
            return BluesModality(modality_type, modal_index)
        if modality_type == ModalityType.MinorBlues:
            return BluesModality(modality_type, modal_index)
        raise Exception('Unrecognized modality type {0} in create_modality'.format(modality_type))
