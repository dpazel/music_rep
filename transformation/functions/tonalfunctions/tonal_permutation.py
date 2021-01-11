"""

File: tonal_permutation.py

Purpose: Class defining a function whose cycles are composed of tone strings (no None).

"""
from function.permutation import Permutation
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.diatonic_tone import DiatonicTone


class TonalPermutation(Permutation):
    """
    Class implementation of a permuation on a set of tones, given in string format.
    """

    def __init__(self, cycles, domain_tones=None):
        """
        Concstructor.
                :param cycles: The cycles of a permutation. List of lists. Strings or DiatonicTones.
                :param domain_tones:  Tones to use in cycles, if empty or None, use tones in cycles. String or
                                      DiatonicTones.
        """
        self._tone_domain = TonalPermutation.check_domain(domain_tones)
        self._tone_cycles = TonalPermutation.convert_cycles_to_tones(self.tone_domain, cycles)

        # if the tone_domain is not specified, we use the tones in the cycles as the domain.
        if len(self._tone_domain) == 0:
            for cycle in self._tone_cycles:
                for tone in cycle:
                    self._tone_domain.add(tone)

        Permutation.__init__(self, self.tone_domain, self.tone_cycles)

    @property
    def tone_domain(self):
        return self._tone_domain

    @property
    def tone_cycles(self):
        return self._tone_cycles

    @staticmethod
    def check_domain(tone_domain):
        tones = set()
        if tone_domain is not None:
            if not isinstance(tone_domain, list) and not isinstance(tone_domain, set):
                raise Exception('Tone domain must be a list or set.')
            for tone_rep in tone_domain:
                if isinstance(tone_rep, str):
                    tone = DiatonicToneCache.get_tone(tone_rep)
                    if tone is None:
                        raise Exception('Tone domain item \'{0}\' illegal syntax.'.format(tone_rep))
                elif isinstance(tone_rep, DiatonicTone):
                    tone = tone_rep
                else:
                    raise Exception('Tone domain item \'{0}\' must be string.'.format(tone_rep))

                tones.add(tone)

        return tones

    @staticmethod
    def convert_cycles_to_tones(tone_domain, cycles):
        if cycles is None:
            return []
        if not isinstance(cycles, list):
            raise Exception('Cycles paramater is not a list.')

        new_cycles = list()
        for cycle in cycles:
            if not isinstance(cycles, list):
                raise Exception('Cycle \'{0}\' must be a list.'.format(cycle))
            new_cycle = list()
            for tone_rep in cycle:
                if isinstance(tone_rep, str):
                    tone = DiatonicToneCache.get_tone(tone_rep)
                    if tone is None:
                        raise Exception('Tone domain item \'{0}\' illegal syntax.'.format(tone_rep))
                elif isinstance(tone_rep, DiatonicTone):
                    tone = tone_rep
                else:
                    raise Exception('Tone domain item \'{0}\' must be string.'.format(tone_rep))

                if len(tone_domain) != 0:
                    if tone not in tone_domain:
                        raise Exception('Tone \'{0}\' not in explicit tone domain.'.format(tone))
                new_cycle.append(tone)
            new_cycles.append(new_cycle)

        return new_cycles

    def __getitem__(self, key):
        if isinstance(key, str):
            key = DiatonicToneCache.get_tone(key)
            if key is None:
                raise Exception('Illegal tone syntax \'{0}\'.'.format(key))
        if not isinstance(key, DiatonicTone):
            raise Exception('Key \'{0}\' must be instance of DiatonticTone'.format(key))
        return super(TonalPermutation, self).__getitem__(key)

