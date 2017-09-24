"""

File: octatonic_modality.py

Purpose: Defines the OctatonicModality class, defining 8 tone scales.
    These scales are based on semitone/wholetone offsets and so there are two variations:
    WH - which starts from the root tone to a whole tone for the second tone.
    HW - which starts from the root tone to a semitone tone for the second tone.

"""
from tonalmodel.modality import Modality, ModalityType, ModalitySpec


class OctatonicModality(Modality):
    """
    Defines the octatonic tonality.  The scale is uniform tone-alternating half and whole steps.
    """
    OCTATONIC_MODALITIES = [
                           ModalityType.HWOctatonic, 
                           ModalityType.WHOctatonic,
                           ]
    
    MODALITY_DEFINITION_MAP = {
        ModalityType.HWOctatonic: ModalitySpec(ModalityType.HWOctatonic, ['P:1', 'm:2', 'M:2', 'm:2', 'M:2', 'A:1',
                                                                          'M:2', 'm:2', 'M:2']),
        ModalityType.WHOctatonic: ModalitySpec(ModalityType.WHOctatonic, ['P:1', 'M:2', 'm:2', 'M:2', 'A:1', 'M:2',
                                                                          'm:2', 'M:2', 'm:2']),
        }

    def __init__(self, modality_type):
        """
        Constructor
        """
        if not isinstance(modality_type, int):
            raise Exception('Modality type must be int value of ModalityType')  
        #  Ensure type given is only for these modalities.
        if modality_type not in OctatonicModality.OCTATONIC_MODALITIES:
            raise Exception('Illegal octatonic modality: {0}'.format(modality_type))
        
        Modality.__init__(self, OctatonicModality.MODALITY_DEFINITION_MAP[modality_type])
    
    @staticmethod
    def octatonic_modality_types_as_string_array():
        answer = [ModalityType.to_str(t) for t in OctatonicModality.OCTATONIC_MODALITIES]
        return answer
