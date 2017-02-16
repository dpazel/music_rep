"""

File: secondary_chord.py

Purpose: Represents and instance of a secondary chord.

"""
from chord import Chord
from tonalmodel.tonality import Tonality
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType
from tonalmodel.modality import ModalityType


class SecondaryChord(Chord):
    """
    Represents and instance of a secondary chord.
    """

    def __init__(self, secondary_chord_template, diatonic_tonality):
        """
        Constructor.
        Args:
          secondary_chord_template: SecondaryChordTemplate
          diatonic_tonality: DiatonicTonality (used in scale degree chord formation)
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
            modality = self.chord_template.secondary_modality.value  
            
        self.__secondary_tonality = Tonality(modality, diatonic_basis)
        
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
        return '{0}'.format(str(self.primary_chord))
