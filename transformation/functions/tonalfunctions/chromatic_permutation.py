"""

File: chromatic_permutation.py

Purpose: Class defining a permutation over the 12-tone chromatic tone set.

"""
from function.permutation import Permutation
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache


class ChromaticPermutation(Permutation):
    """
    Class implementation of a permutation chromatic tones.
    On the handling of enharmonics:
      Internally we use an unambiguous representation as given by NORMALIZED_TONES.  That is, the mapping's domain and
      range is based on that alone.
      However, the cycles given by the user do not need to be in that representation, and in a way represents
      a 'language' for tones that is user/usage dependent.  We use that representation to return values. For symbols
      not found in the user given cycles, we resort to the internal representation. So,
      1) for results that match tones in the user given cycles, those are returned.
      2) for results of tones not in the user given cycles, the internal representation is returned.

    """
    ENHARMONICS = [
        ['C', 'B#', 'Dbb'],
        ['C#', 'B##', 'Db'],
        ['D', 'C##', 'Ebb'],
        ['D#', 'Eb', 'Fbb'],
        ['E', 'D##', 'Fb'],
        ['F', 'E#', 'Gbb'],
        ['F#', 'E##', 'Gb'],
        ['G', 'F##', 'Abb'],
        ['G#', 'Ab'],
        ['A', 'G##', 'Bbb'],
        ['A#', 'Bb', 'Cbb'],
        ['B', 'A##', 'Cb']
        ]
    NORMALIZED_TONES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    NORMALIZED_MAPPING = dict()

    for v in ENHARMONICS:
        key = v[0]
        for k in v:
            NORMALIZED_MAPPING[k] = key

    def __init__(self, cycles=None):
        self._to_user_preference = dict()

        if cycles is None:
            cycles = list()

        norm_cycles = list()
        if len(cycles) == 0:
            for t in ChromaticPermutation.NORMALIZED_TONES:
                tone = DiatonicToneCache.get_tone(t)
                norm_cycles.append([tone])
                self._to_user_preference[tone] = tone
        else:
            if not isinstance(cycles, list):
                raise Exception('Cycles must be a list.')
            for cycle in cycles:
                if not isinstance(cycle, list):
                    raise Exception('Cycle must be a list {0}.'.format(cycle))
                norm_cycle = list()
                for v in cycle:
                    if not isinstance(v, str):
                        raise Exception('Cycle element must be a string {0}.'.format(v))
                    tone_txt = DiatonicTone.to_upper(v)
                    if tone_txt is None:
                        raise Exception('Cycle element \'{0}\' not a recognized tone.'.format(v))
                    tone = DiatonicToneCache.get_tone(ChromaticPermutation.NORMALIZED_MAPPING[tone_txt])
                    if tone in norm_cycle:
                        raise Exception('Tone \'{0}\' appears twice enharmonically in same cycle.'.format(v))
                    norm_cycle.append(tone)

                    # User preferred representation of tone is always the first one found.
                    if tone not in self._to_user_preference:
                        self._to_user_preference[tone] = DiatonicToneCache.get_tone(tone_txt)
                norm_cycles.append(norm_cycle)

        tone_list = [DiatonicToneCache.get_tone(x) for x in ChromaticPermutation.NORMALIZED_TONES]
        Permutation.__init__(self, tone_list, norm_cycles)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = DiatonicToneCache.get_tone(ChromaticPermutation.NORMALIZED_MAPPING[DiatonicTone.to_upper(key)])
        elif isinstance(key, DiatonicTone):
            key = DiatonicToneCache.get_tone(ChromaticPermutation.NORMALIZED_MAPPING[key.diatonic_symbol])
        else:
            raise Exception('Key \'{0}\' must be a tone string or DiatonicTone.'.format(key))

        return_tone = super(ChromaticPermutation, self).__getitem__(key)
        return self._to_user_preference[return_tone] if return_tone in self._to_user_preference else return_tone
