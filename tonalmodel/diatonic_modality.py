"""

File: diatonic_modality.py

Purpose: Defines the DiatonicModality class, defining the major diatonic scales.

"""
from tonalmodel.modality import Modality, ModalityType, ModalitySpec
from tonalmodel.interval import Interval


class DiatonicModality(Modality):
    """
    This class represents diatonic modalities - scales with 7 tones over the 12 tone chromatic scale.
    These include Major, Minor, and Modal scales.
    """
    DIATONIC_MODALITIES = [
                           ModalityType.Major, 
                           ModalityType.NaturalMinor,
                           ModalityType.MelodicMinor,
                           ModalityType.HarmonicMinor,
                           ModalityType.HarmonicMajor,
                           ModalityType.Ionian,
                           ModalityType.Dorian,
                           ModalityType.Phrygian,
                           ModalityType.Lydian,
                           ModalityType.Myxolydian,
                           ModalityType.Aeolian,
                           ModalityType.Locrian,
                           ]
    
    MODALITY_DEFINITION_MAP = {
        ModalityType.Major: ModalitySpec(ModalityType.Major, ['P:1', 'M:2', 'M:2', 'm:2', 'M:2', 'M:2', 'M:2', 'm:2']),
        ModalityType.NaturalMinor: ModalitySpec(ModalityType.NaturalMinor, ['P:1', 'M:2', 'm:2', 'M:2', 'M:2', 'm:2',
                                                                            'M:2', 'M:2']),
        ModalityType.MelodicMinor: ModalitySpec(ModalityType.MelodicMinor, ['P:1', 'M:2', 'm:2', 'M:2', 'M:2', 'M:2',
                                                                            'M:2', 'm:2']),
        ModalityType.HarmonicMinor: ModalitySpec(ModalityType.HarmonicMinor, ['P:1', 'M:2', 'm:2', 'M:2', 'M:2', 'm:2',
                                                                              'A:2', 'm:2']),
        ModalityType.HarmonicMajor: ModalitySpec(ModalityType.HarmonicMajor, ['P:1', 'M:2', 'M:2', 'm:2', 'M:2', 'm:2',
                                                                              'A:2', 'm:2']),
        ModalityType.Ionian: ModalitySpec(ModalityType.Ionian, ['P:1', 'M:2', 'M:2', 'm:2', 'M:2', 'M:2', 'M:2',
                                                                'm:2']),
        ModalityType.Dorian: ModalitySpec(ModalityType.Dorian, ['P:1', 'M:2', 'm:2', 'M:2', 'M:2', 'M:2', 'm:2',
                                                                'M:2']),
        ModalityType.Phrygian: ModalitySpec(ModalityType.Phrygian, ['P:1', 'm:2', 'M:2', 'M:2', 'M:2', 'm:2', 'M:2',
                                                                    'M:2']),
        ModalityType.Lydian: ModalitySpec(ModalityType.Lydian, ['P:1', 'M:2', 'M:2', 'M:2', 'm:2', 'M:2', 'M:2',
                                                                'm:2']),
        ModalityType.Myxolydian: ModalitySpec(ModalityType.Myxolydian, ['P:1', 'M:2', 'M:2', 'm:2', 'M:2', 'M:2',
                                                                        'm:2', 'M:2']),
        ModalityType.Aeolian: ModalitySpec(ModalityType.Aeolian, ['P:1', 'M:2', 'm:2', 'M:2', 'M:2', 'm:2', 'M:2',
                                                                  'M:2']),
        ModalityType.Locrian: ModalitySpec(ModalityType.Locrian, ['P:1', 'm:2', 'M:2', 'M:2', 'm:2', 'M:2', 'M:2',
                                                                  'M:2']),
    }

    def __init__(self, modality_type, modal_index=0):
        """
        Constructor
        """
        if not isinstance(modality_type, int):
            raise Exception('Modality type must be int value of ModalityType')    
        if modality_type not in DiatonicModality.MODALITY_DEFINITION_MAP:
            raise Exception('Illegal diatonic modality value: {0}'.format(str(modality_type)))
        
        Modality.__init__(self, DiatonicModality.MODALITY_DEFINITION_MAP[modality_type], modal_index)

    @staticmethod
    def diatonic_modality_types_as_string_array():
        answer = [ModalityType.to_str(t) for t in DiatonicModality.DIATONIC_MODALITIES]
        return answer

    @staticmethod
    def find_modality(tones):
        answers = list()
        if len(tones) == 7:
            for t in [ModalityType.Major, ModalityType.NaturalMinor, ModalityType.MelodicMinor,
                      ModalityType.HarmonicMinor, ModalityType.HarmonicMajor]:
                modality_spec = DiatonicModality.MODALITY_DEFINITION_MAP[t]

                p1 = Interval.parse('P:1')
                for scale_start in range(0, 7):
                    intervals = [p1] + [Interval.calculate_tone_interval(tones[(scale_start + i) % 7],
                                                                         tones[(scale_start + i + 1) % 7])
                                        for i in range(0, len(tones))]
                    if intervals == modality_spec.incremental_intervals:
                        answers.append(DiatonicModality(t, (-scale_start) % len(tones)))
        return answers
