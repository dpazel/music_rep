"""

File: pentatonic_modality.py

Purpose: Defines the PentatonicModality class, defining the range of 
         pentatonic scales and their variations.

"""
from modality import Modality, ModalityType, ModalitySpec


class PentatonicModality(Modality):
    """
    This class represents 5 pentatonic modalities - scales with 5 tones over the 12 tone chromatic partition.
    With circular succession, each is a rotation of the prior.
    """
    PENTATONIC_MODALITIES = [
                           ModalityType.MajorPentatonic, 
                           ModalityType.EgyptianPentatonic,
                           ModalityType.MinorBluesPentatonic,
                           ModalityType.MajorBluesPentatonic,
                           ModalityType.MinorPentatonic,
                           ]
    
    MODALITY_DEFINITION_MAP = {
        ModalityType.MajorPentatonic: ModalitySpec(ModalityType.MajorPentatonic, ['P:1', 'M:2', 'M:2', 'm:3', 'M:2',
                                                                                  'm:3']),
        ModalityType.EgyptianPentatonic: ModalitySpec(ModalityType.EgyptianPentatonic, ['P:1', 'M:2', 'm:3', 'M:2',
                                                                                        'm:3', 'M:2']),
        ModalityType.MinorBluesPentatonic: ModalitySpec(ModalityType.MinorBluesPentatonic, ['P:1', 'm:3', 'M:2', 'm:3',
                                                                                            'M:2', 'M:2']),
        ModalityType.MajorBluesPentatonic: ModalitySpec(ModalityType.MajorBluesPentatonic, ['P:1', 'M:2', 'm:3', 'M:2',
                                                                                            'M:2', 'm:3']),
        ModalityType.MinorPentatonic: ModalitySpec(ModalityType.MinorPentatonic, ['P:1', 'm:3', 'M:2', 'M:2', 'm:3',
                                                                                  'M:2']),
    }

    def __init__(self, modality_type):
        """
        Constructor.
        
        Args:
          modality_type:  ModalityType for this modality instance.
        """
        if not isinstance(modality_type, int):
            raise Exception('Modality type must be int value of ModalityType') 
        #  Ensure type given is only for Pentatonic modalities.
        if modality_type not in PentatonicModality.PENTATONIC_MODALITIES:
            raise Exception('Illegal pentatonic modality: {0}'.format(modality_type))
        
        Modality.__init__(self, PentatonicModality.MODALITY_DEFINITION_MAP[modality_type])

    @staticmethod
    def pentatonic_modality_types_as_string_array():
        answer = [ModalityType.to_str(t) for t in PentatonicModality.PENTATONIC_MODALITIES]
        return answer
