"""

File: chromatic_tonal_reflection_function.py

Purpose: Class defining a function that tonally reflects over a given tone.

"""
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.tonality import Tonality
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import FlipType
from transformation.functions.tonalfunctions.tonal_function import TonalFunction
from tonalmodel.interval import Interval


class ChromaticTonalReflectionFunction(TonalFunction):

    def __init__(self, domain_tonality, cue_tone, reflect_type=FlipType.CenterTone):
        """
        Constructor
        :param domain_tonality: Scalar tonality being reflected
        :param cue_tone: Cue tone for reflection (must be in domain tonality).
        :param reflect_type: See FlipType for types of reflection.
        """
        self.__domain_tonality = domain_tonality
        self.__cue_tone = cue_tone
        self.__reflect_type = reflect_type

        if cue_tone not in domain_tonality.annotation:
            raise Exception('Cue tone {0} is not in tonality {1}.'.format(cue_tone.diatonic_symbol, domain_tonality))

        self.__primary_map, tonality_list = self._build_primary_map()

        if len(tonality_list) == 0:
            raise Exception('Tonal relfection on {0} cue {1} could not resolve range tonality.'.format(
                self.domain_tonality, self.cue_tone))

        # We like should do some kind of matching of domain to range, e.g. minor-type --> minor-type.from
        # TODO: Explore how to improve this setting when tonality_list has more than 1 element.
        self.__range_tonality = tonality_list[0]

        TonalFunction.__init__(self, self.domain_tonality, self.range_tonality, self.tonal_map,
                               self._build_extension_map())

    @property
    def cue_tone(self):
        return self.__cue_tone

    @property
    def reflect_type(self):
        return self.__reflect_type

    @property
    def tonal_map(self):
        return self.__primary_map

    @property
    def domain_tonality(self):
        return self.__domain_tonality

    @property
    def range_tonality(self):
        return self.__range_tonality

    def _build_primary_map(self):
        domain_scale = self.domain_tonality.annotation[:-1]

        tonal_map = dict()
        if self.reflect_type == FlipType.CenterTone:
            for tone in domain_scale:
                interval = Interval.calculate_tone_interval(tone, self.cue_tone)
                end_tone = interval.get_end_tone(self.cue_tone)
                tonal_map[tone] = end_tone
        else:
            if self.reflect_type == FlipType.LowerNeighborOfPair:
                lower_index = domain_scale.index(self.cue_tone)
                upper_index = (lower_index + 1) % len(domain_scale)
            else:
                upper_index = domain_scale.index(self.cue_tone)
                lower_index = (upper_index - 1) % len(domain_scale)
            tonal_map[domain_scale[upper_index]] = domain_scale[lower_index]
            tonal_map[domain_scale[lower_index]] = domain_scale[upper_index]

            last_lower = domain_scale[lower_index]
            last_upper = domain_scale[upper_index]
            for i in list(reversed(range(0, lower_index))):
                new_lower = domain_scale[i]
                interval = Interval.calculate_tone_interval(new_lower, last_lower)
                new_upper = interval.get_end_tone(last_upper)
                tonal_map[new_lower] = new_upper
                last_lower = new_lower
                last_upper = new_upper

            last_lower = domain_scale[lower_index]
            last_upper = domain_scale[upper_index]
            for i in list(range((upper_index + 1), len(domain_scale))):
                new_upper = domain_scale[i]
                interval = Interval.calculate_tone_interval(last_upper, new_upper)
                new_lower = interval.negation().get_end_tone(last_lower)
                tonal_map[new_upper] = new_lower
                last_lower = new_lower
                last_upper = new_upper

        range_tones = list(reversed([tonal_map[tone] for tone in domain_scale]))
        first_tone = range_tones[-1]
        range_tones = [first_tone] + range_tones[:-1]

        # Determine the tonality of the range
        range_tonality = Tonality.find_tonality(range_tones)

        return tonal_map, range_tonality

    def _build_extension_map(self):
        ltrs = 'CDEFGAB'
        extension = dict()

        domain_scale = self.domain_tonality.annotation[:-1]
        domain_start_index = ltrs.index(domain_scale[0].diatonic_letter)
        domain_index_list = list(ltrs[domain_start_index:] + ltrs[:domain_start_index])

        # One time calculations based on lower upper
        if self.reflect_type != FlipType.CenterTone:
            if self.reflect_type == FlipType.LowerNeighborOfPair:
                lower_domain_index = domain_scale.index(self.cue_tone)
                upper_domain_index = (lower_domain_index + 1) % len(domain_scale)
            else:
                upper_domain_index = domain_scale.index(self.cue_tone)
                lower_domain_index = (upper_domain_index - 1) % len(domain_scale)
            lower_tone = domain_scale[lower_domain_index]
            upper_tone = domain_scale[upper_domain_index]
            lower_ltr_index = domain_index_list.index(lower_tone.diatonic_letter)
            lower_augmentation = lower_tone.augmentation_offset
            upper_ltr_index = domain_index_list.index(upper_tone.diatonic_letter)
            upper_augmentation = upper_tone.augmentation_offset
        else:
            lower_tone = None
            upper_tone = None
            lower_ltr_index = None
            lower_augmentation = None
            upper_ltr_index = None
            upper_augmentation = None

        for l in 'CDEFGAB':
            for aug in ['bb', 'b', '', '#', "##"]:
                tone = DiatonicFoundation.get_tone(l + aug)
                if tone not in self.tonal_map.keys():
                    if self.reflect_type == FlipType.CenterTone:
                        interval = Interval.calculate_tone_interval(tone, self.cue_tone)
                        if interval:  # Some intervals are illegal, eg Cbb --> C, for now ignore
                            end_tone = interval.get_end_tone(self.cue_tone)
                            extension[tone] = end_tone
                    else:

                        tone_ltr_index = domain_index_list.index(tone.diatonic_letter)
                        tone_augmentation = tone.augmentation_offset
                        if tone_ltr_index >= 0 and (tone_ltr_index < lower_ltr_index or
                                                    (tone_ltr_index == lower_ltr_index and
                                                     tone_augmentation <= lower_augmentation)):
                            interval = Interval.calculate_tone_interval(tone, lower_tone)
                            if interval:
                                upper = interval.get_end_tone(upper_tone)
                                extension[tone] = upper
                        elif tone_ltr_index < len(domain_index_list) and (tone_ltr_index > upper_ltr_index or
                                                                          (tone_ltr_index == upper_ltr_index and
                                                                           tone_augmentation >= upper_augmentation)):
                            interval = Interval.calculate_tone_interval(tone, upper_tone)
                            if interval:
                                new_lower = interval.get_end_tone(lower_tone)
                                extension[tone] = new_lower
                        else:   # Between the two limits
                            upper_interval = Interval.calculate_tone_interval(tone, upper_tone)
                            lower_interval = Interval.calculate_tone_interval(lower_tone, tone)
                            if upper_interval is None and lower_interval is None:
                                continue
                            elif upper_interval is None:
                                extension[tone] = upper_tone
                            elif lower_interval is None:
                                extension[tone] = lower_tone
                            else:
                                if abs(lower_interval.chromatic_distance) <= abs(upper_interval.chromatic_distance):
                                    extension[tone] = lower_interval.negation().get_end_tone(upper_tone)
                                else:
                                    extension[tone] = upper_interval.negation().get_end_tone(lower_tone)

        return extension
