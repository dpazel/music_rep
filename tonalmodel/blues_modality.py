"""

File: blues_modality.py

Purpose: to build a modality for the blues scale.

"""
from tonalmodel.modality import Modality, ModalityType, ModalitySpec


class BluesModality(Modality):
    """
    This class represents major and minor blues modalities - scales with 6 tones over the 12 tone chromatic partition.
    """
    BLUES_MODALITIES = [
                        ModalityType.MajorBlues,
                        ModalityType.MinorBlues,
                        ]
    MODALITY_DEFINITION_MAP = {
        ModalityType.MajorBlues: ModalitySpec(ModalityType.MajorBlues, ['P:1', 'M:2', 'A:1', 'm:2', 'm:3',
                                                                        'M:2', 'm:3']),   # Ascending
        ModalityType.MinorBlues: ModalitySpec(ModalityType.MinorBlues, ['P:1', 'm:3', 'M:2', 'A:1', 'm:2',
                                                                        'm:3', 'M:2']),   # Ascending
        }

    def __init__(self, modality_type, modal_index=0):
        """
        Constructor.
        
        Args:
          modality_type:  ModalityType for this modality instance.
        """
        if not isinstance(modality_type, int):
            raise Exception('Modality type must be int value of ModalityType')  
        #  Ensure type given is only for Pentatonic modalities.
        if modality_type not in BluesModality.BLUES_MODALITIES:
            raise Exception('Illegal blues modality: {0}'.format(modality_type))
        
        Modality.__init__(self, BluesModality.MODALITY_DEFINITION_MAP[modality_type], modal_index)

    @staticmethod
    def blues_modality_types_as_string_array():
        answer = [ModalityType.to_str(t) for t in BluesModality.BLUES_MODALITIES]
        return answer
