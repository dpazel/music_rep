"""

File: secondary_chord.py

Purpose: Represents and instance of a secondary chord.

"""
from harmonicmodel.chord import Chord
from tonalmodel.tonality import Tonality
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType
from tonalmodel.modality import ModalityType


class SecondaryChord(Chord):
    """
    Represents and instance of a secondary chord.
    """

    def __init__(self, secondary_chord_template, diatonic_tonality, secondary_tonality=None):
        """
        Constructor.
        :param secondary_chord_template: SecondaryChordTemplate
        :param diatonic_tonality: DiatonicTonality (used in scale degree chord formation)
        :param secondary_tonality: Used to represent denominator tonality
        Note: The means for determining the secondary tonality is not necessarily clean. The standard technique
        involves inferring the modality from the triad built on athe i-th tone of the base modality. However,
        the actual technique to be used can be a variable.  The secondary_tonality argument is meant for cases where
        the standard technique does not hold up - and provides a means for specifying the exact secondary tonality
        when the standard technique does not apply.
        """
        Chord.__init__(self, secondary_chord_template, diatonic_tonality) 
        
        # Build the tonality upon which the primary chord is based
        diatonic_basis = self.diatonic_tonality.get_tone(self.chord_template.secondary_scale_degree - 1)

        # if no secondary modality specified?
        #  Use diatonic_tonality + secondary scale degree.  Determine the triad type of the natural triad there, and
        #  if major, use major modality.  If minor, use melodic minor modality.  Otherwise flag an error.
        if not self.chord_template.secondary_modality:
            triad = TertianChordTemplate.get_triad(diatonic_tonality, self.chord_template.secondary_scale_degree)
            if triad:
                modality = ModalityType.Major if triad.chord_type.value == TertianChordType.Maj else \
                    ModalityType.MelodicMinor if triad.chord_type.value == TertianChordType.Min else None
                if modality is None:
                    raise Exception('Illegal secondary modality for secondary chord')
            else:
                raise Exception('Cannot determine secondary modality for secondary chord')
        else:
            modality = self.chord_template.secondary_modality
            
        self.__secondary_tonality = Tonality.create(modality, diatonic_basis) if not secondary_tonality else secondary_tonality
        
        # Create the principal chord
        self.__primary_chord = self.chord_template.principal_chord_template.create_chord(self.secondary_tonality)
        
    @property
    def chord_type(self):
        return self.primary_chord.chord_type 
    
    @property
    def root_tone(self):
        return self.primary_chord.root_tone
    
    @property
    def tones(self):
        return self.primary_chord.tones 
    
    @property
    def primary_chord(self):
        return self.__primary_chord
    
    @property
    def secondary_tonality(self):
        return self.__secondary_tonality
    
    def __str__(self):
        from harmonicmodel.chord_template import ChordTemplate
        s = str(ChordTemplate.SCALE_DEGREE_REVERSE_MAP[self.chord_template.secondary_scale_degree])
        t = str(self.secondary_tonality.modality.modality_type)
        tones = ', '.join(str(tone[0].diatonic_symbol) for tone in self.primary_chord.tones)
        return '{0}/{1}({2}) [{3}]'.format(str(self.primary_chord.chord_template), s, t, tones)
