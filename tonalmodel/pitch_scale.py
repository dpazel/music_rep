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

    @staticmethod
    def compute_tonal_pitches(tonality, pitch_range):
        """
        For a tonality and pitch range, compute all scale pitches in that range.

        :param tonality: Tonality
        :param pitch_range: PitchRange
        :return:
        """
        pitch_scale = PitchScale(tonality, pitch_range)
        return pitch_scale.pitch_scale
    
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
        return tone_index, pitch_index

    @staticmethod
    def compute_closest_scale_tones(tonality, pitch):
        """
        Returns either the pitch if in tonality, or lower/upper pitches in scale to pitch.
        :param tonality:
        :param pitch:
        :return: an array with 1 element if exact match, otherwise closest lower and upper bound pitches
                 in given tonality.
        """
        from tonalmodel.pitch_range import PitchRange
        chromatic_index = pitch.chromatic_distance
        pitch_range = PitchRange(max(chromatic_index - 12, ChromaticScale.chromatic_start_index()),
                                 min(chromatic_index + 12, ChromaticScale.chromatic_end_index()))
        pitch_scale = PitchScale(tonality, pitch_range)

        for i in range(0, len(pitch_scale.pitch_scale)):
            p = pitch_scale.pitch_scale[i]
            if p.chromatic_distance < chromatic_index:
                continue
            if p.chromatic_distance == chromatic_index:
                return [p]
            if i == 0:
                raise Exception(
                    'unexpected logic issue in compute_closest_pitch_range {0}, {1]'.format(tonality, pitch))
            return [pitch_scale.pitch_scale[i - 1], p]
        raise Exception(
            'unexpected logic fail in compute_closest_pitch_range {0}, {1]'.format(tonality, pitch))

    @staticmethod
    def compute_tonal_pitch_range(tonality, pitch, lower_index, upper_index):
        """
        Find all pitches within range of tonality based on an arbitrary pitch given as starting point.
        In all cases, look at the closest pitches (1 or 2) as origin 0, and the lower/upper as counting indices
        below or up from them.
        :param tonality:
        :param pitch:
        :param lower_index:
        :param upper_index:
        :return:
        """
        import math
        from tonalmodel.pitch_range import PitchRange
        starting_points = PitchScale.compute_closest_scale_tones(tonality, pitch)

        # Determine the number of octaves that will cover the given range.
        up_chrom = max(0, int(math.ceil(float(abs(upper_index)) / len(tonality.annotation)) * 12) *
                       (-1 if upper_index < 0 else 1))
        down_chrom = min(0, int(math.ceil(float(abs(lower_index)) / len(tonality.annotation)) * 12) *
                         (-1 if lower_index < 0 else 1))

        # Compute all pitches within that range
        low = max(starting_points[0].chromatic_distance + down_chrom, ChromaticScale.chromatic_start_index())
        high = min((starting_points[0].chromatic_distance if len(starting_points) == 1
                    else starting_points[1].chromatic_distance) + up_chrom, ChromaticScale.chromatic_end_index())

        pitch_range = PitchRange(low, high)
        pitch_scale = PitchScale(tonality, pitch_range).pitch_scale

        # The first starting point is either the enharmonic equivalent to pitch, or the lower scale pitch to the pitch.
        # lower_starting_index is the index in pitch_scale for that pitch.
        lower_starting_index = [index for index in range(0, len(pitch_scale))
                                if pitch_scale[index].chromatic_distance == starting_points[0].chromatic_distance][0]

        if len(starting_points) == 1:
            full_range = range(lower_starting_index + lower_index,
                               min(lower_starting_index + upper_index + 1, len(pitch_scale)))
            return [pitch_scale[i] for i in full_range]
        else:
            upper_starting_index = [index for index in range(0, len(pitch_scale))
                                    if pitch_scale[index].chromatic_distance ==
                                    starting_points[1].chromatic_distance][0]
            lo = lower_index + (lower_starting_index if lower_index <= 0 else upper_starting_index)
            hi = upper_index + (lower_starting_index if upper_index < 0 else upper_starting_index)
            full_range = range(lo, hi + 1)
            return [pitch_scale[i] for i in full_range]
