"""
File: modality.py

Purpose: Defines a generic sense of modality on the chromatic scale.
  All legal modalities must be defined in ModalityType, which serves as a input parameter.

"""
from tonalmodel.interval import Interval


class ModalityType(object):

    # System wide known modality types.
    Major = None
    NaturalMinor = None
    MelodicMinor = None
    HarmonicMinor = None
    HarmonicMajor = None
    Ionian = None
    Dorian = None
    Phrygian = None
    Lydian = None
    Myxolydian = None
    Aeolian = None
    Locrian = None
    WholeTone = None
    MajorPentatonic = None
    EgyptianPentatonic = None
    MinorBluesPentatonic = None
    MajorBluesPentatonic = None
    MinorPentatonic = None
    HWOctatonic = None
    WHOctatonic = None
    MajorBlues = None
    MinorBlues = None

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if other is None or not isinstance(other, ModalityType):
            raise Exception('Must compare to non-None ModalityType.')
        return self.name == other.name

    def __hash__(self):
        return self.name.__hash__()


# Initialize System-wide modality types.
ModalityType.Major = ModalityType('Major')
ModalityType.NaturalMinor = ModalityType('NaturalMinor')
ModalityType.MelodicMinor = ModalityType('MelodicMinor')
ModalityType.HarmonicMinor = ModalityType('HarmonicMinor')
ModalityType.HarmonicMajor = ModalityType('HarmonicMajor')
ModalityType.Ionian = ModalityType('Ionian')
ModalityType.Dorian = ModalityType('Dorian')
ModalityType.Phrygian = ModalityType('Phrygian')
ModalityType.Lydian = ModalityType('Lydian')
ModalityType.Myxolydian = ModalityType('Myxolydian')
ModalityType.Aeolian = ModalityType('Aeolian')
ModalityType.Locrian = ModalityType('Locrian')
ModalityType.WholeTone = ModalityType('WholeTone')
ModalityType.MajorPentatonic = ModalityType('MajorPentatonic')
ModalityType.EgyptianPentatonic = ModalityType('EgyptianPentatonic')
ModalityType.MinorBluesPentatonic = ModalityType('MinorBluesPentatonic')
ModalityType.MajorBluesPentatonic = ModalityType('MajorBluesPentatonic')
ModalityType.MinorPentatonic = ModalityType('MinorPentatonic')
ModalityType.HWOctatonic = ModalityType('HWOctatonic')
ModalityType.WHOctatonic = ModalityType('WHOctatonic')
ModalityType.MajorBlues = ModalityType('MajorBlues')
ModalityType.MinorBlues = ModalityType('MinorBlues')

SYSTEM_MODALITIES = [
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
    ModalityType.WholeTone,
    ModalityType.MajorPentatonic,
    ModalityType.EgyptianPentatonic,
    ModalityType.MinorBluesPentatonic,
    ModalityType.MajorBluesPentatonic,
    ModalityType.MinorPentatonic,
    ModalityType.HWOctatonic,
    ModalityType.WHOctatonic,
    ModalityType.MajorBlues,
    ModalityType.MinorBlues,
]


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
    
    def __init__(self, modality_spec, modal_index=0):
        self.__modality_spec = modality_spec

        if modal_index < 0 or modal_index > len(self.modality_spec.incremental_intervals) - 2:
            raise Exception('modal_index \'{0}\' invalid, must be positive and less than \'{1}\'.'.
                            format(modal_index, len(self.modality_spec.incremental_intervals) - 1))
        self.__modal_index = modal_index
            
        self.__root_intervals = list()
        self.__incremental_intervals = list()
        sumit = self.__modality_spec.incremental_intervals[0]   # Should be P:1
        self.__root_intervals.append(sumit)
        self.__incremental_intervals.append(sumit)
        for i in range(modal_index + 1, len(self.modality_spec.incremental_intervals) + modal_index + 1):
            ri = i % len(self.modality_spec.incremental_intervals)
            if ri != 0:
                sumit = sumit + self.modality_spec.incremental_intervals[ri]
                self.__incremental_intervals.append(self.modality_spec.incremental_intervals[ri])
                self.__root_intervals.append(sumit)
        # sumit = None
        # for interval in self.__modality_spec.incremental_intervals:
        #    sumit = sumit + interval if sumit is not None else interval
        #    self.__root_intervals.append(sumit)
        
        last_interval = self.__root_intervals[len(self.__root_intervals) - 1]    
        if str(last_interval) != 'P:8':
            raise Exception('Last interval {0} is not \'P:8\''.format(str(last_interval)))
    
    @property
    def modality_spec(self):
        return self.__modality_spec

    @property
    def modal_index(self):
        return self.__modal_index
    
    @property    
    def get_modality_name(self):
        return self.modality_spec.modality_name
    
    @property 
    def modality_type(self):
        return self.__modality_spec.modality_type
    
    @property
    def incremental_intervals(self):
        return self.__incremental_intervals
    
    @property
    def root_intervals(self):
        return self.__root_intervals
      
    def get_number_of_tones(self):
        return len(self.root_intervals) - 1

    @staticmethod
    def get_valid_root_tones():
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
        return '{0}{1}'.format(str(self.modality_spec),
                               '[{0}]'.format(self.modal_index) if self.modal_index != 0 else '')

    @staticmethod
    def find_modality(tones):
        from tonalmodel.diatonic_modality import DiatonicModality
        answers = list()
        answers.extend(DiatonicModality.find_modality(tones))

        from tonalmodel.pentatonic_modality import PentatonicModality
        answers.extend(PentatonicModality.find_modality(tones))
        return answers
