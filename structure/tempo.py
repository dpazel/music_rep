from tonalmodel.range import Range
from timemodel.duration import Duration
from fractions import Fraction

from enum import Enum


# The following are global variables used by TempoType, as we could not define these
# inside TempoType.
class TempoTypeHelper:
    RANGE_MAP = None
    ALL_TYPES = None


class TempoType(Enum):
    """
    Enum class for the quality of tempo names.
    """
    Larghissimo = 1
    Grave = 2
    Lento = 3
    Largo = 4
    Larghetto = 5
    Adagio = 6
    Adagietto = 7
    Andantino = 8
    Andante = 9
    AndanteModerato = 10
    MarciaModerato = 11
    Moderato = 12
    AllegroModerato = 13
    Allegretto = 14
    Allegro = 15
    Vivace = 16
    Vivacissimo = 17
    Allegrissimo = 18
    Presto = 19
    Prestissimo = 20

    def __str__(self):
        return self.name

    @staticmethod
    def class_init():
        """
        This method is a class initializer.  It is called outside the class before 
        its first use.  The tables are:
        1) NAME_MAP: map TempoType to string name.
        2) RANGE_MAP: map TempoType to BPM range.
        3) ALL_TYPES: list of all TempoTypes
        """
        if TempoTypeHelper.RANGE_MAP is not None:
            return

        TempoTypeHelper.RANGE_MAP = {
            TempoType.Larghissimo: Range(0, 24),
            TempoType.Grave: Range(25, 45),
            TempoType.Lento: Range(45, 60),
            TempoType.Largo: Range(40, 60),
            TempoType.Larghetto: Range(60, 66),
            TempoType.Adagio: Range(66, 76),
            TempoType.Adagietto: Range(72, 76),
            TempoType.Andantino: Range(80, 108),
            TempoType.Andante: Range(76, 108),
            TempoType.AndanteModerato: Range(92, 112),
            TempoType.MarciaModerato: Range(83, 85),
            TempoType.Moderato: Range(108, 120),
            TempoType.AllegroModerato: Range(116, 120),
            TempoType.Allegretto: Range(112, 120),
            TempoType.Allegro: Range(120, 168),
            TempoType.Vivace: Range(168, 176),
            TempoType.Vivacissimo: Range(172, 176),
            TempoType.Allegrissimo: Range(172, 176),
            TempoType.Presto: Range(168, 200),
            TempoType.Prestissimo: Range(200, 10000)
        }

        TempoTypeHelper.ALL_TYPES = [
            TempoType.Larghissimo,
            TempoType.Grave,
            TempoType.Lento,
            TempoType.Largo,
            TempoType.Larghetto,
            TempoType.Adagio,
            TempoType.Adagietto,
            TempoType.Andantino,
            TempoType.Andante,
            TempoType.AndanteModerato,
            TempoType.MarciaModerato,
            TempoType.Moderato,
            TempoType.AllegroModerato,
            TempoType.Allegretto,
            TempoType.Allegro,
            TempoType.Vivace,
            TempoType.Vivacissimo,
            TempoType.Allegrissimo,
            TempoType.Presto,
            TempoType.Prestissimo,
        ]
    
    def get_range(self):
        return TempoTypeHelper.RANGE_MAP[self]
    
    @staticmethod
    def get_types():
        return TempoTypeHelper.ALL_TYPES
    
    @staticmethod
    def get_range_for(tempo_type):
        """
        Static method to get the range for a tempo type.
        Args:
          tempo_type: if integer, turned into TempoType based on int.  Otherwise must be a TempoType.
          
        Returns: Range for type.
        Exception: on bad argument type.
        """
        if isinstance(tempo_type, int):
            tempo_type = TempoType(tempo_type)
        elif not isinstance(tempo_type, TempoType):
            raise Exception('Illegal argument type for get_range_for {0}'.format(type(tempo_type)))
        return TempoType.get_range(tempo_type)

# Initialize the static tables in the TempoType class.   
TempoType.class_init()
    

class Tempo(object):
    """
    Class that encapsulates the concept of tempo.
    Tempo is measured in BPM (beats per minute).
    self.__tempo holds the BPM.
    The value of the beat itself is determined by a time signature.
    
    Args:
      tempo:  the int or float value for the tempo
      beat_duration: the duration of the representative beat.  Usually 
                     implicitly the same as the time signature.  Here, the default is a quarter note,
                     but for compound signatures may be given as other than the beat value of a time signature.
                     e.g 12:8 may be 3/8 duration.
    """
    
    def __init__(self, tempo, beat_duration=Duration(1, 4)):
        if isinstance(tempo, int) or isinstance(tempo, float):
            self.__tempo = tempo
        elif isinstance(tempo, TempoType):
            r = tempo.get_range()
            self.__tempo = int((r.end_index + r.start_index) / 2)
        else:
            raise Exception('Tempo rate can only use types int, float, or TempoType, not {0}'.format(type(tempo)))
        self.__beat_duration = beat_duration  
        
    @property
    def beat_duration(self):
        return self.__beat_duration 
    
    def effective_tempo(self, duration):
        """
        Convert the tempo relative to a new beat duration that maintains the same tempo rate for
        the original tempo.  e.g. 50 BMP for a 1/4 note == 100 BPM for an 1/8 note.
        
        Args: 
          duration: a Duration for the new beat value
          
        Returns:
          the new tempo as a float
        """
        return float(Fraction(self.tempo) * self.beat_duration.duration / duration.duration)
        
    @property
    def tempo(self):
        return self.__tempo

    def __str__(self):
        return str(self.tempo)
