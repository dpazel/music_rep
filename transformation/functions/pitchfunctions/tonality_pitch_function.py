"""
File: tonality_pitch_function.py

Purpose: Class defining a pitch function wherein pitch mappings are based a tonality map between two tonalities.

"""
from collections import OrderedDict

from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.pitch_range import PitchRange
from tonalmodel.pitch_scale import PitchScale
from transformation.functions.pitchfunctions.general_pitch_function import GeneralPitchFunction


class TonalityPitchFunction(GeneralPitchFunction):
    """
    Class that uses a tonal_function + pitch range to produce pitch to pitch mapping.
    """

    FULL_PITCH_RANGE = PitchRange.create('A:0', 'C:8')

    def __init__(self, tonal_function, scale_origins, domain_pitch_range, reversal=False):
        """
        Constructor.
        :param tonal_function: TonalFunction upon which this function is based.
        :param scale_origins: Duplet of origin pitches for the domain and range respectively.
        :param domain_pitch_range: Domain pitch range (PitchRange)
        :param reversal: If during construction, domain and range octaves follow together forward, or if the range
                         follow backwards.
        """
        self.domain_tonality = tonal_function.domain_tonality
        self.range_tonality = tonal_function.range_tonality

        if domain_pitch_range is None or not isinstance(domain_pitch_range, PitchRange):
            raise Exception('domain pitch range cannot be None and must be PitchRange')

        dlex, dcom = TonalityPitchFunction._build_lex_dcom_maps(self.domain_tonality, scale_origins[0])
        rlex, rcom = TonalityPitchFunction._build_lex_dcom_maps(self.range_tonality, scale_origins[1])

        # Needed for getitem()
        self._dlex = dlex

        # These define how the mapping starts on the domain, in terms of octaves octaves
        # d_reg: The octave for which the domain tonality is centered.
        # d_min: The minimal octave in the octave coverage of the domain.
        # d_max: The maximal octave in the octave coverage of the domain.
        d_reg = DiatonicPitch.parse(scale_origins[0]).octave
        d_min = max(ChromaticScale.CHROMATIC_START[0],
                    ChromaticScale.index_to_location(domain_pitch_range.start_index)[0]) - 1
        d_max = min(ChromaticScale.CHROMATIC_END[0],
                    ChromaticScale.index_to_location(domain_pitch_range.start_index)[1]) + 1

        # Some aspects of building pitch_map.
        # Goal: pitch_map: (key from largest range of (tone, octave) in domain) --> (range tone, octave)
        # The following help:
        # d_lex: maps enharmonic representations of domain tone to the domain tones.
        #        the range is called the normalized range.
        # d_com: for domain pitch scale centered at scale_origin[0], maps normalized tone to octave.
        # r_lex and r_com are similar but for the range.
        #
        # The pitch map is based on the following dynamics:
        # For d_key in pitch domain, d_key --(d_lex)-->d_n_key--(d_com)-->d_octave
        #     d_key --(tonal_function)--> r_key
        #     r_key --(r_lex)-->r_n_key --(r_com)--> r_octave
        # then:
        #     pitch_map(DP(d_octave, d_key) = DP(r_octave, r_key)
        # with adjustments to d_octave, r_octave based on sliding over the octave ranges.
        pitch_map = OrderedDict()
        for d_octave in range(d_min, d_max + 1):
            for d_tone in tonal_function.map.keys():
                source_pitch = DiatonicPitch(d_octave + (dcom[dlex[d_tone]] - d_reg), d_tone)
                r_tone = tonal_function[d_tone]
                if r_tone is not None:
                    target_pitch = DiatonicPitch(rcom[rlex[r_tone]] -
                                                 (-1 if reversal else 1) * (d_reg - d_octave), r_tone)
                    if domain_pitch_range.is_pitch_inbounds(source_pitch) and \
                            TonalityPitchFunction.FULL_PITCH_RANGE.is_pitch_inbounds(target_pitch):
                        pitch_map[source_pitch] = target_pitch
                else:
                    pitch_map[source_pitch] = None

        GeneralPitchFunction.__init__(self, pitch_map)

    @staticmethod
    def _build_lex_dcom_maps(tonality, scale_origin_str):
        # lex maps all enharmonics to either tones in the tonality or outside of tonality to some select
        # representation
        lex = dict()
        used = set()
        for tone in tonality.annotation:
            enharmonics = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[tone.placement]
            for t in enharmonics:
                lex[DiatonicToneCache.get_tone(t)] = tone
            used.add(tone.placement)

        outside = set(range(0, 12)) - used
        for p in outside:
            enharmonics = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[p]
            select_tone = DiatonicToneCache.get_tone(enharmonics[0])
            enharmonics = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[select_tone.placement]
            for t in enharmonics:
                lex[DiatonicToneCache.get_tone(t)] = select_tone

        # build com which maps the range of lex to the appropriate octave
        origin_pitch = DiatonicPitch.parse(scale_origin_str)

        base_octave = origin_pitch.octave

        com = dict()
        values = list({v for v in lex.values()})
        values.sort(key=lambda x: x.placement)
        index = values.index(origin_pitch.diatonic_tone)
        value_list = values if index == 0 else values[index: len(values)] + values[0: index]
        com[value_list[0]] = octave = base_octave
        for i in range(1, len(value_list)):
            octave = octave + 1 if DiatonicPitch.crosses_c(value_list[i - 1], value_list[i], True) \
                else octave
            com[value_list[i]] = octave

        return lex, com

    @staticmethod
    def _build_pitch_segment_dict(tonality, scale_origin_str):
        origin_pitch = DiatonicPitch.parse(scale_origin_str)
        pitch_range = PitchRange.create(
            '{0}:{1}'.format(origin_pitch.diatonic_tone.diatonic_symbol, origin_pitch.octave),
            '{0}:{1}'.format(origin_pitch.diatonic_tone.diatonic_symbol, origin_pitch.octave + 1))

        scale = PitchScale(tonality, pitch_range).pitch_scale[0: -1]

        d = OrderedDict()
        for p in scale:
            d[p.diatonic_tone] = p.octave

        return d

    def __getitem__(self, pitch):
        if isinstance(pitch, str):
            pitch = DiatonicPitch.parse(pitch)
            if pitch is None:
                raise Exception('Illegal tone syntax \'{0}\'.'.format(pitch))
        if not isinstance(pitch, DiatonicPitch):
            raise Exception('Key \'{0}\' must be instance of DiatonticTone'.format(pitch))
        return super(TonalityPitchFunction, self).__getitem__(self._remap_enharmonic(pitch))

    def _remap_enharmonic(self, pitch):
        input_tone = pitch.diatonic_tone
        input_tone_ltr = input_tone.diatonic_letter
        octave = pitch.octave
        remapped_tone = self._dlex[input_tone]
        remapped_tone_letter = remapped_tone.diatonic_letter

        if (input_tone_ltr == 'C' or input_tone_ltr == 'D') and remapped_tone_letter < 'C':
            octave = octave - 1
        elif (input_tone_ltr == 'B' or input_tone_ltr == 'A') and remapped_tone_letter >= 'C':
            octave = octave + 1

        return DiatonicPitch(octave, remapped_tone)
