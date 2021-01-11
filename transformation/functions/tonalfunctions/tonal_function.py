"""

File: tonal_function.py

Purpose: Class defining a function from one tonality to another.

"""
from function.discrete_function import DiscreteFunction
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.interval import Interval
from collections import OrderedDict
import logging

import sys


class TonalFunction(DiscreteFunction):
    """
    Class implementation of a function between two discrete sets of tones.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def __init__(self, domain_tonality, range_tonality, primary_map=None, extension_map=None):
        """
        Create a map between two tonalities. There are some special cases.
        1) Domain and range have same cardinality, 1-1 onto mapping created.
        2) Unequal cardinality, domain tones map to None

        In referencing domain, enharmonics are obeyed, i.e. f[C#] == f[Db]
        However, for range tonality, some select tone is used to represent enharmonic class, and that representative
        tone is not specified.

        :param domain_tonality: Domain tonality.
        :param range_tonality: Range tonality.
        :param primary_map: Map of domain to range tones. if None and same cardinality, 1-1 onto map formed.
        :param extension_map: Map of non-domain tones.
        """
        self.__domain_tonality = domain_tonality
        self._domain_tones = domain_tonality.annotation[:len(domain_tonality.annotation) - 1]

        self.__range_tonality = range_tonality
        self._range_tones = range_tonality.annotation[:len(range_tonality.annotation) - 1]

        # t_map will be a dictionary combining primary and extension
        t_map = OrderedDict()
        self._primary_map = OrderedDict()
        if primary_map is not None:
            # Map domain tones to range tones, not intermediate normalized tone representation
            if not isinstance(primary_map, dict):
                raise Exception('Primary dict {0} must be a dict.'.format(primary_map))
            if len(primary_map) != len(self._domain_tones):
                raise Exception('Specified init map size must match size of domain {0}.'.format(
                    len(self._domain_tones)))
            for key, value in primary_map.items():
                if isinstance(key, str):
                    key = DiatonicToneCache.get_tone(key)
                elif not isinstance(key, DiatonicTone):
                    raise Exception('Key \'{0}\' must be string or DiatonicTone.'.format(key))
                if key not in self._domain_tones:
                    raise Exception('Tone {0} must be in tonality {1}'.format(key, domain_tonality))

                if value is not None:
                    if isinstance(value, str):
                        value = DiatonicToneCache.get_tone(value)
                    elif not isinstance(value, DiatonicTone):
                        raise Exception('Value \'{0}\' must be string or DiatonicTone.'.format(value))
                    if value not in self._range_tones:
                        raise Exception('Tone {0} must be in tonality {1}'.format(value, range_tonality))

                t_map[key] = value
                self._primary_map[key] = value
        else:
            # map each domain tone using a cycle over the range tones.
            range_index = 0
            for x in self._domain_tones:
                t_map[x] = self._range_tones[range_index]
                self._primary_map[x] = self._range_tones[range_index]
                range_index = range_index + 1
                if range_index >= len(self._range_tones):
                    range_index = 0

        self._extension_map = OrderedDict()
        if extension_map is not None:
            # key-->value but make key normalized. We cannot do that to value since 2 keys can map to different
            # enharmonic representations. (so a user_pref map from normalized result would be 2 values.)
            if not isinstance(extension_map, dict):
                raise Exception('Extension map {0} must be a dict.'.format(primary_map))
            for key, value in extension_map.items():
                if isinstance(key, str):
                    key = DiatonicToneCache.get_tone(key)
                elif not isinstance(key, DiatonicTone):
                    raise Exception('Key \'{0}\' must be string.'.format(key))

                if value is not None:
                    if not isinstance(value, str) and not isinstance(value, DiatonicTone):
                        raise Exception('Value \'{0}\' must be string or DiatonicTone.'.format(value))
                    if isinstance(value, str):
                        value = DiatonicToneCache.get_tone(value)
                        if value is None:
                            raise Exception('Illegal tone format or type \'{0}\'.'.format(value))
                    t_map[key] = value
                    self._extension_map[key] = value  # Normalized tones mapping
                else:
                    raise Exception('Value \'{0}\' is None but must be string or DiatonicTone.'.format(value))

        DiscreteFunction.__init__(self, t_map)

    @property
    def domain_tonality(self):
        return self.__domain_tonality

    @property
    def range_tonality(self):
        return self.__range_tonality

    @property
    def primary_map(self):
        return self._primary_map

    @property
    def extension_map(self):
        return self._extension_map

    def __getitem__(self, key):
        if isinstance(key, str):
            key = DiatonicToneCache.get_tone(key)
            if key is None:
                raise Exception('Key \'{0}\' invalid syntax.'.format(key))

        return super(TonalFunction, self).__getitem__(key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = DiatonicToneCache.get_tone(key)
            if key is None:
                raise Exception('Key \'{0}\' invalid syntax.'.format(key))
        elif not isinstance(key, DiatonicTone):
            raise Exception('Key {0} invalid - must be string or DiatonicTone.'.format(key))
        domain_tonal = key in self._domain_tones

        if isinstance(value, str):
            value = DiatonicToneCache.get_tone(value)
            if value is None:
                raise Exception('Value \'{0}\' invalid syntax.'.format(value))
        elif value is not None and not isinstance(value, DiatonicTone):
            raise Exception('Range {0} invalid - must be string, DiatonicTone or None.'.format(value))

        range_tonal = value in self._range_tones

        if domain_tonal != range_tonal:
            raise Exception('Both key {0} and value {1} must be in respective tonality or outside for valid setting.'.
                            format(key, value))

        super(TonalFunction, self).__setitem__(key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            key = DiatonicToneCache.get_tone(key)
            if key is None:
                raise Exception('Key \'{0}\' invalid syntax.'.format(key))
        elif not isinstance(key, DiatonicTone):
            raise Exception('Key {0} invalid - must be string or DiatonicTone.'.format(key))

        if key in self._domain_tones:
            raise Exception('Tone {0} must not be in tonality {1}'.format(key, self.domain_tonality))

        super(TonalFunction, self).__delitem__(key)

    def extract_tonal_and_extension_maps(self):
        """
        Deprecated - use primary_map and extension_map

        Extract the mapping information in two parts:
        1) the mapping of the domain tonality tones.
        2) the mapping of the non-domain tonality tones.
        :return: (in order as described above)
          1) domain_tonality_map
          2) extension_map
        """

        domain_tonality_map = dict()
        used = set()
        for tone in self.domain_tonality.annotation:
            domain_tonality_map[tone] = self[tone]
            used.add(tone.placement)

        extension_map = dict()
        outside = set(range(0, 12)) - used
        for p in outside:
            enharmonics = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[p]
            source_tone = DiatonicToneCache.get_tone(enharmonics[0])
            extension_map[source_tone] = self[tone] if tone in self.map else None

        return domain_tonality_map, extension_map

    def __str__(self):
        return '{{{0}}} --> {{{1}}}'.format(self.domain_tonality, self.range_tonality)

    def extract_template(self):
        """
        Return the generic template for this function.
        :return:
        """
        return TonalFunctionTemplate(self)

    def create_adapted_function(self, domain_tonality, range_tonality):
        """
        Create a new function based on this function's characteristics, using a (potentially) different
        domain and range tonality.

        :param domain_tonality:
        :param range_tonality:
        :return:
        """
        return self.extract_template().create_adapted_function(domain_tonality, range_tonality)


class TonalFunctionTemplate(object):
    """
    Class that holds generic information about a tonal function's tonal and chromatic information - so that
    a comparable function can be generated from it using different tonalities. The key constraint is that the
    cardinalities of the tonalities for the new domain/range must match that of the function that generates the
    template.
    """

    def __init__(self, tonal_function):
        """
        Constructor.
        :param tonal_function: Tonal function whose characteristics are used for the template.
        """
        self._domain_cardinality = tonal_function.domain_tonality.cardinality
        self._range_cardinality = tonal_function.range_tonality.cardinality

        self._tonal_order, self._tonal_interval_map = TonalFunctionTemplate.create_primary_templates(tonal_function)
        self._extension_interval_map = TonalFunctionTemplate.create_extension_interval_template(tonal_function)

    @property
    def tonal_order(self):
        return self._tonal_order

    @property
    def tonal_interval_map(self):
        return self._tonal_interval_map

    @property
    def extension_interval_map(self):
        return self._extension_interval_map

    @property
    def domain_cardinality(self):
        return self._domain_cardinality

    @property
    def range_cardinality(self):
        return self._range_cardinality

    def create_adapted_function(self, domain_tonality, range_tonality):
        """
        Generate a tonal function from this template using:

        :param domain_tonality: Replacement domain tonality.
        :param range_tonality: Replacement range tnality.
        :return:
        """

        # Tonalities must match original domain and range in cardinality.
        if domain_tonality.cardinality != self.domain_cardinality:
            raise Exception('Cardinalities of domains don\'t match: given {0} versus {1}.'.format(
                domain_tonality.cardinality, self.domain_cardinality))
        if range_tonality.cardinality != self.range_cardinality:
            raise Exception('Cardinalities of ranges don\'t match: given {0} versus {1}.'.format(
                range_tonality.cardinality, self.range_cardinality))

        domain_tones = domain_tonality.annotation[:len(domain_tonality.annotation) - 1]
        range_tones = range_tonality.annotation[:len(range_tonality.annotation) - 1]

        primary_map = dict()
        for t, i in zip(domain_tones, self.tonal_order):
            primary_map[t] = None if i is None else range_tones[i]

        # Build the extension map
        extension_map = dict()
        for k, v in self.extension_interval_map.items():
            key_tone = Interval.end_tone_from_pure_distance(domain_tones[0], k[0], k[1])
            if key_tone not in domain_tones:
                value_tone = Interval.end_tone_from_pure_distance(range_tones[0], v[0], v[1])
                extension_map[key_tone] = value_tone

        # Examine the primary intervals, as some may not be primary due to modality change.
        for k, v in self.tonal_interval_map.items():
            key_tone = Interval.end_tone_from_pure_distance(domain_tones[0], k[0], k[1])
            if key_tone not in domain_tones:
                value_tone = Interval.end_tone_from_pure_distance(range_tones[0], v[0], v[1])
                extension_map[key_tone] = value_tone

        return TonalFunction(domain_tonality, range_tonality, primary_map, extension_map)

    @staticmethod
    def create_primary_templates(tonal_function):
        domain_tones = tonal_function.domain_tonality.annotation[:len(tonal_function.domain_tonality.annotation) - 1]
        range_tones = tonal_function.range_tonality.annotation[:len(tonal_function.range_tonality.annotation) - 1]

        tonal_order_template = list()
        tonal_interval_map = dict()
        for t in domain_tones:
            tonal_order_template.append(range_tones.index(tonal_function[t]) if tonal_function[t] in range_tones
                                        else None)
            key_pure_dist = Interval.calculate_pure_distance(domain_tones[0], t)

            if tonal_function[t] is not None:
                value_pure_distance = Interval.calculate_pure_distance(range_tones[0], tonal_function[t])
            else:
                value_pure_distance = None
            tonal_interval_map[key_pure_dist] = value_pure_distance

        return tonal_order_template, tonal_interval_map

    @staticmethod
    def create_extension_interval_template(tonal_function):
        domain_tones = tonal_function.domain_tonality.annotation[:len(tonal_function.domain_tonality.annotation) - 1]
        range_tones = tonal_function.range_tonality.annotation[:len(tonal_function.range_tonality.annotation) - 1]

        extension_interval_map = dict()
        ext_map = tonal_function.extension_map
        if ext_map is None:
            return extension_interval_map

        for t in tonal_function.map.keys():
            if t not in domain_tones:
                key_pure_dist = Interval.calculate_pure_distance(domain_tones[0], t)

                if tonal_function[t] is not None:
                    value_pure_distance = Interval.calculate_pure_distance(range_tones[0], tonal_function[t])
                else:
                    value_pure_distance = None
                extension_interval_map[key_pure_dist] = value_pure_distance

        return extension_interval_map
