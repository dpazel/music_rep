"""

File: tempo.py

Purpose: Defines classes for Tempo and TempoType

"""
from tonalmodel.range import Range
from timemodel.duration import Duration
from fractions import Fraction


class TempoType:
    """
    Enum class for the quality of musical intervals.
    """
    Larghissimo, Grave, Lento, Largo, Larghetto,\
        Adagio, Adagietto, Andantino, Andante, AndanteModerato,\
        MarciaModerato, Moderato, AllegroModerato, Allegretto, Allegro,\
        Vivace, Vivacissimo, Allegrissimo, Presto, Prestissimo = range(20)

    NAME_MAP = None
    
    RANGE_MAP = None
    
    ALL_TYPES = None
        
    def __init__(self, vtype):
        self.value = vtype
    
    @staticmethod   
    def class_init():
        """
        This method is a class initializer.  It is called outside the class before 
        its first use.  The tables are:
        1) NAME_MAP: map TempoType to string name.
        2) RANGE_MAP: map TempoType to BPM range.
        3) ALL_TYPES: list of all TempoTypes
        """
        TempoType.NAME_MAP = {
            TempoType(TempoType.Larghissimo): 'Larghissimo',
            TempoType(TempoType.Grave): 'Grave',
            TempoType(TempoType.Lento): 'Lento',
            TempoType(TempoType.Largo): 'Largo',
            TempoType(TempoType.Larghetto): 'Larghetto',
            TempoType(TempoType.Adagio): 'Adagio',
            TempoType(TempoType.Adagietto): 'Adagietto',
            TempoType(TempoType.Andantino): 'Andantino',
            TempoType(TempoType.Andante): 'Andante',
            TempoType(TempoType.AndanteModerato): 'AndanteMaoerato',
            TempoType(TempoType.MarciaModerato): 'MarciaModerato',
            TempoType(TempoType.Moderato): 'Moderato',
            TempoType(TempoType.AllegroModerato): 'AllegroModerato',
            TempoType(TempoType.Allegretto): 'Allegretto',
            TempoType(TempoType.Allegro): 'Allegro',
            TempoType(TempoType.Vivace): 'Vivace',
            TempoType(TempoType.Vivacissimo): 'Vivacissimo',
            TempoType(TempoType.Allegrissimo): 'Allegrissimo',
            TempoType(TempoType.Presto): 'Presto',
            TempoType(TempoType.Prestissimo): 'Prestissimo',
        }
        
        TempoType.RANGE_MAP = {
            TempoType(TempoType.Larghissimo): Range(0, 24),
            TempoType(TempoType.Grave): Range(25, 45),
            TempoType(TempoType.Lento): Range(45, 60),
            TempoType(TempoType.Largo): Range(40, 60),
            TempoType(TempoType.Larghetto): Range(60, 66),
            TempoType(TempoType.Adagio): Range(66, 76),
            TempoType(TempoType.Adagietto): Range(72, 76),
            TempoType(TempoType.Andantino): Range(80, 108),
            TempoType(TempoType.Andante): Range(76, 108),
            TempoType(TempoType.AndanteModerato): Range(92, 112),
            TempoType(TempoType.MarciaModerato): Range(83, 85),
            TempoType(TempoType.Moderato): Range(108, 120),
            TempoType(TempoType.AllegroModerato): Range(116, 120),
            TempoType(TempoType.Allegretto): Range(112, 120),
            TempoType(TempoType.Allegro): Range(120, 168),
            TempoType(TempoType.Vivace): Range(168, 176),
            TempoType(TempoType.Vivacissimo): Range(172, 176),
            TempoType(TempoType.Allegrissimo): Range(172, 176),
            TempoType(TempoType.Presto): Range(168, 200),
            TempoType(TempoType.Prestissimo): Range(200, 10000),
        }
        
        TempoType.ALL_TYPES = [
            TempoType(TempoType.Larghissimo),
            TempoType(TempoType.Grave),
            TempoType(TempoType.Lento),
            TempoType(TempoType.Largo),
            TempoType(TempoType.Larghetto),            
            TempoType(TempoType.Adagio),   
            TempoType(TempoType.Adagietto), 
            TempoType(TempoType.Andantino),  
            TempoType(TempoType.Andante),
            TempoType(TempoType.AndanteModerato),
            TempoType(TempoType.MarciaModerato),
            TempoType(TempoType.Moderato),
            TempoType(TempoType.AllegroModerato),
            TempoType(TempoType.Allegretto),
            TempoType(TempoType.Allegro),
            TempoType(TempoType.Vivace),
            TempoType(TempoType.Vivacissimo),
            TempoType(TempoType.Allegrissimo),
            TempoType(TempoType.Presto),
            TempoType(TempoType.Prestissimo),
        ]
       
    def __str__(self):
        return TempoType.NAME_MAP[self]
        
    def __eq__(self, y):
        return self.value == y.value
    
    def __hash__(self):
        return hash(self.value)
    
    def get_range(self):
        return TempoType.RANGE_MAP[self]
    
    @staticmethod
    def get_types():
        return TempoType.ALL_TYPES
    
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
        return TempoType.RANGE_MAP[tempo_type]

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
