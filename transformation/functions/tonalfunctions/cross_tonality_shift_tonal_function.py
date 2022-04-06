"""
File: cross_tonality_shift_tonal_function.py

Purpose: Class for mapping tonality to tonality of same cardinality an interval difference,
         based on the end point of the interval.

"""
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from transformation.functions.tonalfunctions.tonal_function import TonalFunction
from tonalmodel.tonality import Tonality
from tonalmodel.interval import Interval


class CrossTonalityShiftTonalFunction(TonalFunction):
    """
    Class to build a tonal function based on a map from a domain tonality to a new tonality built upon:
    1) specified root tone.
    2) modal index identified to the root.
    3) basis modality type.
    """

    def __init__(self, domain_tonality, new_root_tone, modal_index=None, inherent_modality_type=None):
        """
        Constructor.
        :param domain_tonality: Given domain tonality.
        :param new_root_tone: The root for the new tonality.
        :param modal_index: The modal index for the new root tone.  If none, match to domain_tonality.
        :param inherent_modality_type: new modality type for behind the new tonality, e.g. major. if None, match
               to domain tonality.
        Note: tonality cardinality must match!
        Note: new_root_tone should be the domain_tonality's modal_index tone.
        """
        modality = inherent_modality_type if inherent_modality_type is not None else domain_tonality.modality_type
        if isinstance(new_root_tone, str):
            root_tone_parameter = DiatonicToneCache.get_tone(new_root_tone)
        else:
            root_tone_parameter = new_root_tone
        range_tonality = Tonality.create(modality, root_tone_parameter,
                                         modal_index if modal_index is not None else domain_tonality.modal_index)

        if domain_tonality.cardinality != range_tonality.cardinality:
            raise Exception('domain and range tonalities must have same cardinality')

        self._domain_tonality = domain_tonality
        self._range_tonality = range_tonality
        self._modal_index = range_tonality.modal_index

        self.constr_primary_map = self._build_primary_map()
        TonalFunction.__init__(self, self.domain_tonality, self.range_tonality, self.constr_primary_map,
                               self._build_extension_map())

    @staticmethod
    def create_shift(domain_tonality, interval):
        """
        Alternative Construction using tonality and interval.
        :param domain_tonality:
        :param interval: interval specifying the shift of domain_tonality's root tone. (not basis)
        :return:
        """
        return CrossTonalityShiftTonalFunction(domain_tonality, interval.get_end_tone(domain_tonality.root_tone))

    @property
    def domain_tonality(self):
        return self._domain_tonality

    @property
    def range_tonality(self):
        return self._range_tonality

    @property
    def modal_index(self):
        return self._modal_index

    def _build_primary_map(self):
        domain_tones = self.domain_tonality.annotation[:-1]
        range_tones = self.range_tonality.annotation[:-1]

        # In order, map domain tonality tones to range tonality tones.
        primary_map = {domain_tones[i]: range_tones[i] for i in range(0, len(domain_tones))}
        return primary_map

    def _build_extension_map(self):
        extension = dict()

        # Map domain tone augmentations to similarly augmented range tonality tones.
        #   e.g. if m[Db] == G, then m[D == Db#] == G#
        key_ltr_map = {d.diatonic_letter: d for d in self.domain_tonality.annotation}
        for ltr_item, tone_item in key_ltr_map.items():
            target_tone = self.constr_primary_map[tone_item]
            for aug in ['bb', 'b', '', '#', "##"]:
                tone = DiatonicFoundation.get_tone(ltr_item + aug)
                if tone not in self.constr_primary_map.keys():
                    aug_difference = tone.augmentation_offset - tone_item.augmentation_offset
                    new_target = DiatonicTone.alter_tone_by_augmentation(target_tone, aug_difference)
                    extension[tone] = new_target

        # Map all the other cases, e.g. tones outside pentatonic tonal scale for example.
        tone_list = self.domain_tonality.annotation[:-1]
        for ltr_item in 'ABCDEFG':
            if ltr_item not in key_ltr_map.keys():
                t = DiatonicFoundation.get_tone(ltr_item)
                lo_tone, hi_tone = CrossTonalityShiftTonalFunction._compute_neighbor_tones(t, tone_list)
                lo_target = self.constr_primary_map[lo_tone] if lo_tone in self.constr_primary_map.keys() else \
                    extension[lo_tone]
                hi_target = self.constr_primary_map[hi_tone] if hi_tone in self.constr_primary_map.keys() else \
                    extension[hi_tone]

                # d_diff is half-step diff between lo_tone and hi_tone for domain.
                d_diff = hi_tone.placement - lo_tone.placement if lo_tone.placement <= hi_tone.placement else \
                    hi_tone.placement - lo_tone.placement + 12
                # r_diff is half-step diff between lo_tone and hi_tone for target.
                r_diff = hi_target.placement - lo_target.placement if lo_target.placement <= hi_target.placement else\
                    hi_target.placement - lo_target.placement + 12

                range_factor = r_diff / d_diff
                # tone_domain_distance is chromatic distance from lo_tone to t  (domain).
                tone_domain_distance = t.placement - lo_tone.placement if lo_tone.placement <= t.placement else \
                    t.placement - lo_tone.placement + 12
                # range_chrom_dist is conversion of tone_domain_distance to range chromatic distance (interpolation).
                #     i.e. distance from lo_target to ideal target (corresponding to t in domain).
                range_chrom_dist = int(round(tone_domain_distance * range_factor))

                # Tonal interpolation:
                # 1) Need to use a diatonic dist from lo_target
                # 2) Adjusted so that from lo_target is range_chrom_dist
                diatonic_distance = DiatonicTone.calculate_diatonic_distance(lo_tone, t)
                # target_tone is end tone of interval based on diatonic_distance and range_chrom_dist
                target_tone = Interval.end_tone_from_pure_distance(lo_target, diatonic_distance, range_chrom_dist)

                extension[t] = target_tone
                tone_list.insert(tone_list.index(lo_tone) + 1, t)
                key_ltr_map[t] = target_tone

                # Now that t is mappec, map all the augmentations.
                for aug in ['bb', 'b', '#', "##"]:
                    aug_tone = DiatonicFoundation.get_tone(ltr_item + aug)
                    if aug_tone not in self.constr_primary_map.keys() and aug_tone not in extension.keys():
                        aug_difference = aug_tone.augmentation_offset - t.augmentation_offset
                        new_target = DiatonicTone.alter_tone_by_augmentation(target_tone, aug_difference)
                        extension[aug_tone] = new_target

        return extension

    @staticmethod
    def _compute_neighbor_tones(cue_tone, tone_list):
        # Find from tone_list, a tone1, tone2 with tone1<=tone<=tone2 with nearest proximity/
        from misc.ordered_map import OrderedMap

        # s : placement -> index over all tones in tone_list
        s = OrderedMap({v.placement: tone_list.index(v) for v in tone_list})

        # least_index == index of tone in tone_list mapped by least placement.
        least_index = s[min(pl for pl in s.keys())]
        # nearest_pl = s's placement key that is just below cue_tones placement
        nearest_pl = s.floor(cue_tone.placement)
        if nearest_pl is None:
            return tone_list[-1 if least_index == 0 else least_index - 1], tone_list[least_index]

        if nearest_pl == cue_tone.placement:
            return tone_list[s[nearest_pl]], None

        nearest_idx = s[nearest_pl]
        return tone_list[nearest_idx], tone_list[nearest_idx + 1 if nearest_idx != len(tone_list) - 1 else 0]
