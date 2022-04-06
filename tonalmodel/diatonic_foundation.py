"""
File: diatonic_foundation.py

Purpose: Class defining diatonic foundation, a static class that ties the diatonic pitches to the chromatic scale.

"""
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache


class DiatonicFoundation(object):
    """
    Static class that connects the diatonic pitches to the Chromatic scale.
    
    """
    
    # Map all valid tones to their displacement on chromatic partition.
    TONE_PLACEMENT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11,
                      'Cb': -1, 'Db': 1, 'Eb': 3, 'Fb': 4, 'Gb': 6, 'Ab': 8, 'Bb': 10,
                      'C#': 1, 'D#': 3, 'E#': 5, 'F#': 6, 'G#': 8, 'A#': 10, 'B#': 12,
                      'Cbb': -2, 'Dbb': 0, 'Ebb': 2, 'Fbb': 3, 'Gbb': 5, 'Abb': 7, 'Bbb': 9,
                      'C##': 2, 'D##': 4, 'E##': 6, 'F##': 8, 'G##': 9, 'A##': 11, 'B##': 13,
                      }
    
    # Note: this needs to sync with DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING
    ENHARMONIC_OCTAVE_ADJUSTMENT_MAPPING = {
        0: [0, -1, 0],
        1: [0, -1, 0],
        2: [0, 0, 0],
        3: [0, 0, 0],
        4: [0, 0, 0],
        5: [0, 0, 0],
        6: [0, 0, 0],
        7: [0, 0, 0],
        8: [0, 0],
        9: [0, 0, 0],
        10: [0, 0, 1],
        11: [0, 0, 1]
        }

    def __init__(self):
        """
        Constructor
        """
    
    @staticmethod 
    def get_chromatic_distance(diatonic_pitch):
        """
        Convert a diatonic pitch into its chromatic distance
        
        Args:
          diatonic_pitch: instance of DiatonicPitch
        Return:
          the chromatic index of the pitch, e.g. 48 for C4.
        """
        return diatonic_pitch.chromatic_distance
    
    @staticmethod 
    def map_to_diatonic_scale(chromatic_index):
        """
        Convert a chromatic index (int) to a diatonic pitch in string format.
        
        Args:
          chromatic_index: the chromatic index of the pitch (int)
        Return:
          all enharmonic diatonic pitches
        """
        from tonalmodel.diatonic_pitch import DiatonicPitch
        location = ChromaticScale.index_to_location(chromatic_index)
        enharmonics = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[location[1]]
        octave_adjustments = DiatonicFoundation.ENHARMONIC_OCTAVE_ADJUSTMENT_MAPPING[location[1]]
        answers = []
        for i in range(0, len(enharmonics)):
            enharmonic = enharmonics[i]
            answers.append(DiatonicPitch.parse(enharmonic + ':' + str(location[0] + octave_adjustments[i])))
        return answers
    
    @staticmethod        
    def add_semitones(diatonic_pitch, semitones):
        """
        Given a diatonic pitch, add a number of semitones, and return
          all enharmonic representations.
          
        Args:
          diatonic_pitch: DiatonicPitch instance
          semitones: number of semitones to add
        Returns:
          A list of enharmonic quivalent pitches that result from the addition.
        """
        index = DiatonicFoundation.get_chromatic_distance(diatonic_pitch)
        if index == -1:
            return None
        return DiatonicFoundation.map_to_diatonic_scale(index + semitones)
    
    @staticmethod
    def semitone_difference(diatonic_pitch_a, diatonic_pitch_b):
        """
        Given two pitches, compute their difference, 1st - 2nd
        
        Args:
          diatonic_pitch_a: DiatonicPitch instance
          diatonic_pitch_b: DiatonicPitch instance
        Returns:
          1st - 2nd returning semitones.
        """
        index_a = DiatonicFoundation.get_chromatic_distance(diatonic_pitch_a)
        index_b = DiatonicFoundation.get_chromatic_distance(diatonic_pitch_b)
        if index_a == -1 or index_b == -1:
            raise Exception('Illegal pitch specified')
        return index_a - index_b
                
    @staticmethod
    def get_tone(diatonic_tone_text):
        """
        Fetch a cached diatonic tone based on text representation.
        
        Args:
          diatonic_tone_text: text specification, e.g. Abb
          
        Returns:
          DiatonicTone for specified pitch
          
        Exceptions:
          If specified pitch cannot be parsed.
        """
        return DiatonicToneCache.get_tone(diatonic_tone_text)
    
    @staticmethod
    def get_tones():
        return DiatonicToneCache.get_tones()
