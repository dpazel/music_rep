"""

File: whole_tone_modality.py

Purpose: To define the whole tone modality type.

"""
from tonalmodel.modality import Modality, ModalityType, ModalitySpec


class WholeToneModality(Modality):
    """
    This class represents whole tone modalities - scales with 6 tones over the 12 tone chromatic scale.
    All tones are 2 semitones apart.
    """

    WHOLE_TONE_SPEC = ModalitySpec(ModalityType.WholeTone, ['P:1', 'M:2', 'M:2', 'M:2',
                                                            'M:2', 'M:2', 'd:3'])

    @staticmethod
    def create(modality_type, modal_index = 0):
        if modality_type != ModalityType.WholeTone:
            raise Exception('Type parameter is not WholeTone.')
        return Modality(WholeToneModality.WHOLE_TONE_SPEC, modal_index)

