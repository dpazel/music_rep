"""

File: pitch_range.py

Purpose: defines an inclusive chromatic pitch range specified either by chromatic indices or locations. 

"""
from tonalmodel.range import Range
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch


class PitchRange(Range):
    """
    PitchRange defines an inclusive chromatic pitch range.
    """

    def __init__(self, start_index, end_index):
        """
        Constructor
        
        Args:
          start_index: integer start chromatic pitch index
          end_index: integer end chromatic pitch index
        Exceptions: is start, end out of range of absolute chromatic range, plus those from Range.
        """
        Range.__init__(self, start_index, end_index)
        if start_index < ChromaticScale.chromatic_start_index():
            raise Exception(
                "Start index {0} lower than chromatic start {1}".format(start_index,
                                                                        ChromaticScale.chromatic_start_index()))
        if end_index > ChromaticScale.chromatic_end_index():
            raise Exception(
                "end index {0} higher than chromatic end {1}".format(end_index, ChromaticScale.chromatic_end_index()))
        
    @staticmethod
    def create(start_spn, end_spn):
        """
        Create PitchRange based on start and end scientific pitch notation.
        
        Args:
          start_spn: start spn (pitch string).
          end_spn: end spn (pitch string).
        Returns:
          PitchRange based on inputs.
        """
        start = DiatonicFoundation.get_chromatic_distance(DiatonicPitch.parse(start_spn)
                                                          if isinstance(start_spn, str) else start_spn)
        end = DiatonicFoundation.get_chromatic_distance(
            DiatonicPitch.parse(end_spn) if isinstance(end_spn, str) else end_spn)
        return PitchRange(start, end)
    
    def is_location_inbounds(self, location):
        """
        Determines if given chromatic location is in bounds of range.
        
        Args:
          location: chromatic location
        Returns:
          boolean indicating if in bounds.
        """
        return self.is_inbounds(ChromaticScale.location_to_index(location))
    
    def is_pitch_inbounds(self, pitch):
        """
        Determines if given chromatic location is in bounds of range.
        
        Args:
          pitch: spn text for pitch, e.g. 'c:4' or DiatonticPitch object.
        Returns:
          boolean indicating if in bounds.
        """
        p = DiatonicPitch.parse(pitch) if isinstance(pitch, str) else pitch
        return self.is_inbounds(DiatonicFoundation.get_chromatic_distance(p))
    
    def find_lowest_placement_in_range(self, placement):
        """
        For a given chromatic placement (0, ..., 11) find the lowest chromatic index 
        in the range for it.
        """
        if placement < 0 or placement >= 12:
            raise Exception('Illegal placement value {0} must be between 0 and 11'.format(placement))
        start_partition = ChromaticScale.index_to_location(self.start_index)[0]
        end_partition = ChromaticScale.index_to_location(self.end_index)[0]
        lowest_index = -1
        for partition in range(start_partition, end_partition + 1):
            if self.is_location_inbounds((partition, placement)):
                lowest_index = ChromaticScale.location_to_index((partition, placement))
                break
        return lowest_index
    
    def __str__(self):
        return 'P-R({0}, {1})'.format(DiatonicFoundation.map_to_diatonic_scale(self.start_index)[0],
                                      DiatonicFoundation.map_to_diatonic_scale(self.end_index)[0])
