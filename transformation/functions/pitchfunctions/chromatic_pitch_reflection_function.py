"""
File: chromatic_pitch_reflection_function.py

Purpose: Class defining a pitch function based on flipping about a tone or about a neighboring tone pair using
         chromatic reflection

"""
from enum import Enum

from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.functions.pitchfunctions.general_pitch_function import GeneralPitchFunction
from transformation.functions.tonalfunctions.tonality_permutation_function import TonalityPermutationFunction
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType
from transformation.functions.tonalfunctions.chromatic_tonal_reflection_function import ChromaticTonalReflectionFunction


class ChromaticPitchReflectionFunction(GeneralPitchFunction):
    """
    Class for a pitch function based on flipping tones across a variety of boundaries as defined by FlipType, for
    a given tonality.
    """

    def __init__(self, domain_tonality, cue_pitch, domain_pitch_range, reflect_type=FlipType.CenterTone):
        self.__domain_tonality = domain_tonality
        self.__cue_pitch = cue_pitch
        self.__domain_pitch_range = domain_pitch_range

        self.__tonal_function = ChromaticTonalReflectionFunction(domain_tonality, cue_pitch.diatonic_tone, reflect_type)

        GeneralPitchFunction.__init__(self, self._build_pitch_map())


    @property
    def tonal_function(self):
        return self.__tonal_function

    @property
    def domain_tonality(self):
        return self.__domain_tonality

    @property
    def range_tonality(self):
        return self.tonal_function.range_tonality

    @property
    def cue_pitch(self):
        return self.__cue_pitch

    @property
    def domain_pitch_range(self):
        return self.__domain_pitch_range

    def _build_pitch_map(self):
        LTRS = 'CDEFGAB'
        index = LTRS.index(self.domain_tonality.diatonic_tone.diatonic_letter)
        key_ltrs = list(LTRS[index:] + LTRS[:index])
        c_index = key_ltrs.index('C')
        low_octave = self.cue_pitch.octave if key_ltrs.index(self.cue_pitch.diatonic_tone.diatonic_letter) < c_index \
            else self.cue_pitch.octave - 1
        high_octave = low_octave + 1

        RANGE_LTRS = 'CBAGFED'
        index = RANGE_LTRS.index(self.range_tonality.diatonic_tone.diatonic_letter)
        range_key_ltrs = list(RANGE_LTRS[index:] + RANGE_LTRS[:index])
        range_c_index = range_key_ltrs.index('C')
        range_low_octave = self.cue_pitch.octave if range_key_ltrs.index(self.cue_pitch.diatonic_tone.diatonic_letter) \
                                                    > range_c_index else self.cue_pitch.octave - 1
        range_high_octave = range_low_octave + 1

        imap = dict()
        for tone in self.tonal_function.domain:
            domain_octave = low_octave if key_ltrs.index(tone.diatonic_letter) < c_index else high_octave
            value = self.tonal_function[tone]
            range_octave = range_high_octave if range_key_ltrs.index(value.diatonic_letter) <= range_c_index else range_low_octave
            imap[DiatonicPitch(domain_octave, tone)] = DiatonicPitch(range_octave, value)

        full_map = dict()
        start = ChromaticScale.index_to_location(self.domain_pitch_range.start_index)[0]
        end = ChromaticScale.index_to_location(self.domain_pitch_range.end_index)[0] + 1

        for octave in range(start, end):
            if octave < ChromaticScale.CHROMATIC_START[0] or octave > ChromaticScale.CHROMATIC_END[0]:
                continue
            octave_delta = self.cue_pitch.octave - octave
            for pitch in imap.keys():
                rrange = imap[pitch]
                new_pitch = DiatonicPitch(pitch.octave - octave_delta, pitch.diatonic_tone)
                if self.domain_pitch_range.is_pitch_inbounds(new_pitch):
                    full_map[new_pitch] = DiatonicPitch(rrange.octave + octave_delta, rrange.diatonic_tone)


        return full_map


