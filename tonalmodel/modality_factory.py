"""

File: modality_factory.py

Purpose: Defines the static class ModalityFactory and the static method to create a modality
         by ModalityType

"""

from tonalmodel.modality import Modality

from tonalmodel.diatonic_modality import DiatonicModality
from tonalmodel.blues_modality import BluesModality
from tonalmodel.whole_tone_modality import WholeToneModality
from tonalmodel.pentatonic_modality import PentatonicModality
from tonalmodel.octatonic_modality import OctatonicModality


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

        raise Exception('Unrecognized modality type {0} in create_modality'.format(modality_type))


for key, value in DiatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)


for key, value in BluesModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)


ModalityFactory.ModalityInitDict[WholeToneModality.WHOLE_TONE_SPEC.modality_type] = \
    WholeToneModality.WHOLE_TONE_SPEC


for key, value in PentatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)


for key, value in OctatonicModality.MODALITY_DEFINITION_MAP.items():
    ModalityFactory.register_modality(key, value)
