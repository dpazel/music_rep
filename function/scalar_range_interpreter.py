"""

File: scalar_range_interpreter.py

Purpose: A ScalarRangeInterpreter is a PitchRangeInterpreter that maps numerics to the pitches of a tonality.

"""
import math

from function.pitch_range_interpreter import PitchRangeInterpreter
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.pitch_range import PitchRange
from tonalmodel.pitch_scale import PitchScale
from misc.ordered_map import OrderedMap


class ScalarRangeInterpreter(PitchRangeInterpreter):
    """
    ScalarRangeInterpreter maps numeric values to pitches, exposed as a PitchRangeInterpreter.  The mapping is
    linear in v.
    """

    def __init__(self, tonality, anchor_pitch=None, anchor_value=None, pitch_unit=1):
        """
        Constructor.
        :param tonality: The tonality being mapped to.
        :param anchor_pitch: A DiatonicPitch, in combo with anchor_value is a sample of the mapping.
        :param anchor_value: A numeric value that maps to anchor_pitch.
        :param pitch_unit: In the linear map of value to pitches, pitch_unit is the distance between mapping values.
        """
        self.__tonality = tonality
        self.__pitch_scale = PitchScale(self.tonality, PitchRange.create('A:0', 'C:8')).pitch_scale

        self.anchor_pitch = self.pitch_scale[0] if anchor_pitch is None else \
            DiatonicPitch.parse(anchor_pitch) if isinstance(anchor_pitch, str) else anchor_pitch

        anchor_index = self.pitch_scale.index(self.anchor_pitch)
        if anchor_index == -1:
            raise Exception('Anchor pitch \'{0}\' not found in pitch scale for tonality \'{1}\''.
                            format(self.anchor_pitch, self.tonality))

        self.__pitch_unit = pitch_unit

        self.anchor_value = anchor_value if anchor_value is not None else anchor_index * self.pitch_unit

        # base value should map to beginning of pitch scale!
        # recall that pitch unit maps to each pitch, making the scalar scale linear in value!
        base_value = anchor_value - anchor_index * pitch_unit

        self.value_to_pitch = OrderedMap()
        self.pitch_to_value = dict()
        for i in range(0, len(self.pitch_scale)):
            pitch = self.pitch_scale[i]
            value = base_value + i * pitch_unit
            self.value_to_pitch.insert(value, pitch)
            self.pitch_to_value[pitch] = value

        PitchRangeInterpreter.__init__(self)

    @property
    def tonality(self):
        return self.__tonality

    @property
    def pitch_scale(self):
        return self.__pitch_scale

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
        return self.pitch_to_value[diatonic_pitch] if diatonic_pitch in self.pitch_to_value else None

    def eval_as_pitch(self, v):
        floor_value = self.value_to_pitch.floor(v)
        low_pitch = self.value_to_pitch[floor_value]
        index = self.pitch_scale.index(low_pitch)

        if index >= len(self.pitch_scale) - 1 or math.isclose(v, floor_value):
            return [low_pitch]
        return [low_pitch, self.pitch_scale[index + 1]]

    def eval_as_accurate_chromatic_distance(self, v):
        floor_value = self.value_to_pitch.floor(v)
        low_pitch = self.value_to_pitch[floor_value]
        index = self.pitch_scale.index(low_pitch)

        if index >= len(self.pitch_scale) - 1 or math.isclose(v, floor_value):
            return low_pitch.chromatic_distance
        high_pitch = self.pitch_scale[index + 1]
        return low_pitch.chromatic_distance + \
               ((v - floor_value) / (self.pitch_unit)) * \
               (high_pitch.chromatic_distance - low_pitch.chromatic_distance)
