"""
File: chromatic_scale.py

Purpose: Functions related to chromatic scale.

Reference:
  https://en.wikipedia.org/wiki/Piano_key_frequencies

"""
import math
import re


class ChromaticScale(object):

    NUMBER_OF_SEMITONES = 12
    CHROMATIC_START = (0, 9)
    CHROMATIC_END = (8, 0)

    A0 = 27.5000    # lowest chromatic frequency in chromatic scale, corresponds to (0, 9) or '0:9'
    SEMITONE_RATIO = math.pow(2.0, 1.0 / 12.0)

    # (partition number, 12-based offset)
    CHROMATIC_FORM = r'([0-8]):(10|11|[0-9])' 
    CHROMATIC_PATTERN = re.compile(CHROMATIC_FORM)

    @staticmethod
    def get_chromatic_scale(start_pitch, end_pitch):
        """
        Get the chromatic scale from start to end inclusive.
    
        Args
            start: chromatic location of starting pitch (p, i) 
            end: chromatic location of ending pitch (p, i)
        Returns
            List of semitone frequencies from start to end inclusive.
        """
    
        start_index = ChromaticScale.location_to_index(start_pitch)
        end_index = ChromaticScale.location_to_index(end_pitch)
    
        if start_index > end_index:
            return None
    
        if start_index < ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_START) or \
           end_index > ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_END):
            return None
    
        freq = ChromaticScale.A0
        for _ in range(ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_START) + 1, start_index + 1):
            freq *= ChromaticScale.SEMITONE_RATIO
        
        answer = [freq]
        for _ in range(start_index + 1, end_index + 1):
            freq *= ChromaticScale.SEMITONE_RATIO
            answer.append(freq)
        return answer 

    @staticmethod
    def get_frequency(pitch_location):
        """
        Get the frequency for a given pitch as chromatic location.
        
        Args:
            pitch_location: in (p, i) form
        Returns:
            frequency: (float)
        """
        index = ChromaticScale.location_to_index(pitch_location) 
    
        if index < ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_START) or \
           index > ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_END):
            return None 
    
        freq = ChromaticScale.A0
        for _ in range(ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_START) + 1, index + 1):
            freq *= ChromaticScale.SEMITONE_RATIO
        
        return freq

    @staticmethod
    def parse_notation(notation):
        """"
        Parse a pitch in 'o:i' string format into (0, i) form.
        
        Args:
            notation: pitch in 'o:i' format
        Returns:
            pitch in (o, i) form
        """
        n = ChromaticScale.CHROMATIC_PATTERN.match(notation)
        if not n:
            return None
        return int(n.group(1)), int(n.group(2))

    @staticmethod
    def location_to_index(pitch):
        """
        Convert a pitch in (p, i) form into absolute index
        
        Args:
            pitch: in (p, i) form
        Return:
            corresponding absolute index of (o, i) form
        """
        return ChromaticScale.NUMBER_OF_SEMITONES * pitch[0] + pitch[1]

    @staticmethod
    def index_to_location(index):
        """
        Convert pitch absolute index to (p, i) form
        
        Args:
            absolute index of pitch
        Returns:
            (o, i) form of absolute index
        """
        return index / ChromaticScale.NUMBER_OF_SEMITONES, index % ChromaticScale.NUMBER_OF_SEMITONES
    
    @staticmethod
    def chromatic_start_index():
        return ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_START)
    
    @staticmethod
    def chromatic_end_index():
        return ChromaticScale.location_to_index(ChromaticScale.CHROMATIC_END)
