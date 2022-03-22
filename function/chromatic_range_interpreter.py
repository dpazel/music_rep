"""

File: chromatic_range_interpreter.py

Purpose: A PitchRangeInterpreter that evaluates chromatic distances into pitches (Ref. DiatonicFoundation).

"""
import math

from function.pitch_range_interpreter import PitchRangeInterpreter
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.chromatic_scale import ChromaticScale
from misc.ordered_map import OrderedMap


class ChromaticRangeInterpreter(PitchRangeInterpreter):
    """
    Class that interprets a number as being in the chromatic range A:0-C:8,
        and computes pitches that relate to that range.
    """

    def __init__(self, anchor_pitch=DiatonicPitch.parse('A:0'), anchor_value=9, pitch_unit=1):
        """
        Constructor,
        """
        self.__anchor_pitch = anchor_pitch
        if not isinstance(self.anchor_pitch, DiatonicPitch):
            raise Exception('Anchor is not a DiatonicPitch')

        self.__anchor_value = anchor_value
        self.__pitch_unit = pitch_unit

        anchor_index = self.anchor_pitch.chromatic_distance
        base_value = anchor_value - anchor_index * pitch_unit

        self.value_to_pitch = OrderedMap()
        self.pitch_to_value = dict()
        for i in range(ChromaticScale.chromatic_start_index(), ChromaticScale.chromatic_end_index() + 1):
            pitch = DiatonicFoundation.map_to_diatonic_scale(i)[0]
            value = base_value + i * pitch_unit
            self.value_to_pitch.insert(value, pitch)
            self.pitch_to_value[pitch] = value

        PitchRangeInterpreter.__init__(self)

    @property
    def anchor_pitch(self):
        return self.__anchor_pitch

    @property
    def anchor_value(self):
        return self.__anchor_value

    @property
    def pitch_unit(self):
        return self.__pitch_unit

    def eval_as_nearest_pitch(self, v):
        candidates = self.eval_as_pitch(v)
        if len(candidates) == 1:
            return candidates[0]
        v1 = self.pitch_to_value[candidates[0]]
        v2 = self.pitch_to_value[candidates[1]]
        if v <= (v1 + v2) / 2:
            return candidates[0]
        return candidates[1]

    def value_for(self, diatonic_pitch):
        if isinstance(diatonic_pitch, str):
            diatonic_pitch = DiatonicPitch.parse(diatonic_pitch)
            if diatonic_pitch is None:
                return None
        if diatonic_pitch not in self.pitch_to_value:
            enharmonics = diatonic_pitch.enharmonics()
            found = False
            for p in enharmonics:
                if p in self.pitch_to_value:
                    diatonic_pitch = p
                    found = True
                    break
            if not found:
                return None
        return self.pitch_to_value[diatonic_pitch] if diatonic_pitch in self.pitch_to_value else None

    def eval_as_pitch(self, v):
        floor_value = self.value_to_pitch.floor(v)
        ceil_value = self.value_to_pitch.ceil(v)
        if math.isclose(v, self.value_for(self.value_to_pitch[floor_value])):
            return [self.value_to_pitch[floor_value]]
        else:
            p1 = self.value_to_pitch[floor_value]
            p2 = self.value_to_pitch[ceil_value]
            return [p1, p2]

    def eval_as_accurate_chromatic_distance(self, v):
        floor_value = self.value_to_pitch.floor(v)
        low_pitch = self.value_to_pitch[floor_value]
        index = low_pitch.chromatic_distance

        if index >= ChromaticScale.chromatic_end_index() or math.isclose(v, floor_value):
            return low_pitch.chromatic_distance
        high_pitch = DiatonicFoundation.map_to_diatonic_scale(index + 1)[0]
        return low_pitch.chromatic_distance + \
               ((v - floor_value) / self.pitch_unit) * \
               (high_pitch.chromatic_distance - low_pitch.chromatic_distance)
