"""
File: modality.py

Purpose: Defines a generic sense of modality on the chromatic scale.
  All legal modalities must be defined in ModalityType, which serves as a input parameter.

"""
from tonalmodel.interval import Interval


class ModalityType(object):
    """
    Enum class for the quality of musical intervals.
    """
    Major, NaturalMinor, MelodicMinor, HarmonicMinor, \
        Ionian, Dorian, Phrygian, Lydian, Myxolydian, Aeolian, Locrian,   \
        WholeTone, \
        MajorPentatonic, EgyptianPentatonic, MinorBluesPentatonic, MajorBluesPentatonic, MinorPentatonic, \
        HWOctatonic, WHOctatonic, \
        MajorBlues, MinorBlues,  \
        = range(21)
    
    def __init__(self, vtype):
        self.value = vtype
        
    def __str__(self):
        return ModalityType.to_str(self.value)
    
    @staticmethod
    def to_str(value):
        if value == ModalityType.Major:
            return 'Major'
        elif value == ModalityType.NaturalMinor:
            return 'NaturalMinor'
        elif value == ModalityType.MelodicMinor:
            return 'MelodicMinor'
        elif value == ModalityType.HarmonicMinor:
            return 'HarmonicMinor'
        elif value == ModalityType.Ionian:
            return 'Ionian'
        elif value == ModalityType.Dorian:
            return 'Dorian'
        elif value == ModalityType.Phrygian:
            return 'Phrygian'
        elif value == ModalityType.Lydian:
            return 'Lydian'
        elif value == ModalityType.Myxolydian:
            return 'Myxolydian'
        elif value == ModalityType.Aeolian:
            return 'Aeolian'
        elif value == ModalityType.Locrian:
            return 'Locrian'
        elif value == ModalityType.WholeTone:
            return 'WholeTone'
        elif value == ModalityType.MajorPentatonic:
            return 'MajorPentatonic'
        elif value == ModalityType.EgyptianPentatonic:
            return 'EgyptionPentatonic'
        elif value == ModalityType.MinorBluesPentatonic:
            return 'MinorBluesPentatonic'
        elif value == ModalityType.MajorBluesPentatonic:
            return 'MajorBluesPentatonic'
        elif value == ModalityType.MinorPentatonic:
            return 'MinorPentatonic'
        elif value == ModalityType.HWOctatonic:
            return 'HWOctatonic'
        elif value == ModalityType.WHOctatonic:
            return 'WHOctatonic'
        elif value == ModalityType.MajorBlues:
            return "MajorBlues"
        elif value == ModalityType.MinorBlues:
            return "MinorBlues"
        else:
            raise Exception('Illegal modality type value: {0}'.format(value))
        
    @staticmethod
    def to_type(t_string):
        t = None
        if t_string == 'Major':
            t = ModalityType.Major
        elif t_string == 'NaturalMinor':
            t = ModalityType.NaturalMinor
        elif t_string == 'MelodicMinor':
            t = ModalityType.MelodicMinor
        elif t_string == 'HarmonicMinor':
            t = ModalityType.HarmonicMinor
        elif t_string == 'Ionian':
            t = ModalityType.Ionian
        elif t_string == 'Dorian':
            t = ModalityType.Dorian
        elif t_string == 'Phrygian':
            t = ModalityType.Phrygian
        elif t_string == 'Lydian':
            t = ModalityType.Lydian
        elif t_string == 'Myxolydian':
            t = ModalityType.Myxolydian
        elif t_string == 'Aeolian':
            t = ModalityType.Aeolian
        elif t_string == 'Locrian':
            t = ModalityType.Locrian
        elif t_string == 'WholeTone':
            t = ModalityType.WholeTone
        elif t_string == 'MajorPentatonic':
            t = ModalityType.MajorPentatonic
        elif t_string == 'EgyptianPentatonic':
            t = ModalityType.EgyptianPentatonic
        elif t_string == 'MinorBluesPentatonic':
            t = ModalityType.MinorBluesPentatonic
        elif t_string == 'MajorBluesPentatonic':
            t = ModalityType.MajorBluesPentatonic
        elif t_string == 'MinorPentatonic':
            t = ModalityType.MinorPentatonic
        elif t_string == 'HWOctatonic':
            t = ModalityType.HWOctatonic
        elif t_string == 'WHOctatonic':
            t = ModalityType.WHOctatonic
        elif t_string == 'MajorBlues':
            t = ModalityType.MajorBlues
        elif t_string == 'MinorBlues':
            t = ModalityType.MinorBlues
            
        return ModalityType(t) if t is not None else None
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return self.__str__().__hash__()

   
class ModalitySpec(object):
    """
    Class defining a modality specification that is used to initialize the Modality class.
    """
    
    def __init__(self, modality_type, incremental_interval_strs):
        """
        Constructor.

        :param modality_type:
        :param incremental_interval_strs:
        """
        if isinstance(modality_type, int):
            self.__modality_type = ModalityType(modality_type)    
        elif not isinstance(modality_type, ModalityType):
            raise Exception('Illegal modality type argument {0}.'.format(type(modality_type))) 
        else:
            self.__modality_type = modality_type
            
        if not isinstance(incremental_interval_strs, list):
            raise Exception('Illegal incremental intervals argument type {0}', type(incremental_interval_strs))
        
        self.__incremental_intervals = [Interval.parse(interval) for interval in incremental_interval_strs]
        
    @property
    def modality_type(self):
        return self.__modality_type
    
    @property
    def modality_name(self):
        return str(self.modality_type)
    
    @property
    def incremental_intervals(self):
        return self.__incremental_intervals   
    
    def __str__(self):
        return '{0}[{1}]'.format(self.modality_type, ', '.join(str(interval)
                                                               for interval in self.incremental_intervals))


class Modality(object):
    """
    Defines a generic sense of modality, based on a collection of semitone offsets on a chromatic partition.
    """
    
    # This is a global accessible list of all possible starting diatonic tones.  This is useful for any modalities
    # that could have an empty (C-based) key signature, or otherwise that depends on each note being qualified
    # by it respectful augmentation.
    COMMON_ROOTS = ['C', 'D', 'E', 'F', 'G', 'A', 'B',
                    'Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb',
                    'C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#']
    
    DIATONIC_TONE_LETTERS = list('CDEFGAB')
    KEY_PLACEMENT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
                     'Bb': 10, 'Eb': 3, 'Ab': 8, 'Db': 1, 'Gb': 6, 'Cb': 11,
                     'C#': 1, 'D#': 3, 'F#': 6, 'G#': 8, 'A#': 10, 'Fb': 4, 'B#': 0, 'E#': 5}
    
    def __init__(self, modality_spec): 
        self.__modality_spec = modality_spec
            
        self.__root_intervals = []
        sumit = None
        for interval in self.__modality_spec.incremental_intervals:
            sumit = sumit + interval if sumit is not None else interval
            self.__root_intervals.append(sumit)
        
        last_interval = self.__root_intervals[len(self.__root_intervals) - 1]    
        if str(last_interval) != 'P:8':
            raise Exception('Last interval {0} is not \'P:8\''.format(str(last_interval)))
    
    @property
    def modality_spec(self):
        return self.__modality_spec
    
    @property    
    def get_modality_name(self):
        return self.modality_spec.modality_name
    
    @property 
    def modality_type(self):
        return self.__modality_spec.modality_type
    
    @property
    def incremental_intervals(self):
        return self.modality_spec.incremental_intervals
    
    @property
    def root_intervals(self):
        return self.__root_intervals
      
    def get_number_of_tones(self):
        return len(self.root_intervals)

    def get_valid_root_tones(self):
        return Modality.COMMON_ROOTS
    
    def get_tonal_scale(self, diatonic_tone):
        """
        Given a tone root, compute the tonal scale for this modality.
        Treat this as a protected static method.
        
        Method:
          To simplify, we treat chromatic placement non-circularly, but linearly, and keep
          adding as we move along, running_placement.  
          We also do a linear calculation based on scale letter creation, starting at 0
          As we move scale letter to next, if we rollover (b-->C), we add 12 to 
          So. letter_placement is a linear sum of 12*rollovers + the letter's displacement.
          So letter_placement - running_placement are in sync and provides the ajustment calculation
          the make the new letter a scale key.
        
        Args:
          diatonic_tone: DiatonicTone for the root.
        Returns:
          List of DiatonicTone's in scale order for the input tone.  The starting and end tone are the same.
        """
        from tonalmodel.diatonic_pitch import DiatonicPitch
        root_pitch = DiatonicPitch(4, diatonic_tone)
        tones = []
        
        for interval in self.root_intervals:
            p = interval.get_end_pitch(root_pitch)
            tones.append(p.diatonic_tone)
            
        return tones
    
    def __str__(self):
        return str(self.modality_spec)