"""

File: tonal_scale.py

Purpose: To compute pitch scales over a given range on the chromatic scale.
         It is call TonalScale rather than PitchScale, as it relates more to tonality than tone.

"""
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.pitch_range import PitchRange
from tonalmodel.diatonic_pitch import DiatonicPitch


class PitchScale(object):
    """
    Tonality based class to build a set of DiatonicPitch's from the tonality for a chromatic range.
    """

    def __init__(self, tonality, pitch_range):
        """
        Constructor.
        
        Args:
            tonality: the Tonality object for the scale.
            pitch_range: the PitchRange for the scale coverage.
        """
        self.__tonality = tonality
        self.__pitch_range = pitch_range
        
        self.__tone_scale = tonality.annotation
        self.__pitch_scale = self.__compute_pitch_scale()
        
    @property
    def tonality(self):
        return self.__tonality
    
    @property
    def pitch_range(self):
        return self.__pitch_range
    
    @property
    def tone_scale(self):
        return self.__tone_scale
    
    @property
    def pitch_scale(self):
        return self.__pitch_scale
        
    @staticmethod   
    def create_default(tonality):
        return PitchScale(tonality, PitchRange(ChromaticScale.chromatic_start_index(),
                                               ChromaticScale.chromatic_end_index()))
    
    def __compute_pitch_scale(self):
        (tone_index, pitch_index) = self.__find_lowest_tone()   # Determine the lowest tone in the range
        if tone_index == -1:
            return []
        scale = [DiatonicPitch(ChromaticScale.index_to_location(pitch_index)[0],
                               self.tone_scale[tone_index].diatonic_symbol)]
        
        # Given the first pitch, sync up with the incremental intervals on the tonality, and move forward, computing
        # each scale pitch until we are out of range.  
        # Note: be sure to skip the first incremental interval which should be P:1
        prior_pitch = scale[0]
        while True:
            tone_index += 1
            if tone_index > len(self.tone_scale) - 1:
                tone_index = 1  # skip 0 as that should be P:1
            incremental_interval = self.tonality.modality.incremental_intervals[tone_index]
            current_pitch = incremental_interval.get_end_pitch(prior_pitch)
            if current_pitch.chromatic_distance > self.pitch_range.end_index:
                break
            scale.append(current_pitch)
            prior_pitch = current_pitch
            
        return scale
        
    def __find_lowest_tone(self):
        tone_index = -1
        pitch_index = 300
        # loop over scale tones
        #    for each, find the lowest chromatic index in range (if any), and set that as the 'find' 
        for tone in self.tone_scale:
            #  Get the lowest chromatic index in range, for the given tone
            lowest_index = self.pitch_range.find_lowest_placement_in_range(tone.placement)
            if lowest_index != -1:
                if lowest_index < pitch_index:
                    tone_index = self.tone_scale.index(tone)
                    pitch_index = lowest_index
        return (tone_index, pitch_index)
