"""

File: pentatonic_modality.py

Purpose: Defines the PentatonicModality class, defining the range of 
         pentatonic scales and their variations.

"""
from tonalmodel.modality import Modality, ModalityType, ModalitySpec
from tonalmodel.interval import Interval


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

    @staticmethod
    def create(modality_type, modal_index = 0):
        if modality_type not in PentatonicModality.PENTATONIC_MODALITIES:
            raise Exception('Type parameter is not diatonic.')
        if modality_type not in PentatonicModality.MODALITY_DEFINITION_MAP:
            raise Exception('Illegal diatonic modality value: {0} - Check Modality_definition_map'.format(
                str(modality_type)))
        return Modality(PentatonicModality.MODALITY_DEFINITION_MAP[modality_type], modal_index)

    @staticmethod
    def pentatonic_modality_types_as_string_array():
        answer = [ModalityType.to_str(t) for t in PentatonicModality.PENTATONIC_MODALITIES]
        return answer

    @staticmethod
    def find_modality(tones):
        answers = list()
        if len(tones) == 5:
            for t in [ModalityType.MajorPentatonic]:
                modality_spec = PentatonicModality.MODALITY_DEFINITION_MAP[t]

                p1 = Interval.parse('P:1')
                for scale_start in range(0, 5):
                    intervals = [p1] + [Interval.calculate_tone_interval(tones[(scale_start + i) % 5],
                                                                         tones[(scale_start + i + 1) % 5])
                                        for i in range(0, len(tones))]
                    if intervals == modality_spec.incremental_intervals:
                        answers.append(PentatonicModality.create(t, (-scale_start) % len(tones)))
        return answers

