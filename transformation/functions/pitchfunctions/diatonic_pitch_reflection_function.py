"""
File: diatonic_pitch_reflection_function.py

Purpose: Class defining a pitch function based on flipping about a tone or about a neighboring tone pair.

"""
from enum import Enum

from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_pitch import DiatonicToneCache
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.pitch_range import PitchRange
from tonalmodel.pitch_scale import PitchScale
from transformation.functions.pitchfunctions.general_pitch_function import GeneralPitchFunction
from transformation.functions.tonalfunctions.tonality_permutation_function import TonalityPermutationFunction


class FlipType(Enum):
    """
    Enumeration of types of flips:
    CenterTone: that a given tone is stable, and surrounding pairs reflection.
    LowerNeighborOfPair: that a given town flips with the next higher, and the same for concentric pairs.
    UpperNeighborOfPair: that a given town flips with the next lower, and the same for concentric pairs.
    """
    CenterTone = 1
    LowerNeighborOfPair = 2
    UpperNeighborOfPair = 3


class DiatonicPitchReflectionFunction(GeneralPitchFunction):
    """
    Class for a pitch function based on flipping tones across a variety of boundaries as defined by FlipType, for
    a given tonality.
    """

    def __init__(self, tonality, cue_pitch, domain_pitch_range, flip_type=FlipType.CenterTone):
        """
        Constructor
        :param tonality: Tonality (key) of reflection_tests.
        :param cue_pitch: A pitch used to define/start the reflection_tests on the tonality scale.
        :param domain_pitch_range: The scale range that limits the flipped scale.
        :param flip_type: The reflection_tests type of the cue_pitch
        """
        self._tonality = tonality
        self._tones = tonality.annotation[:len(tonality.annotation) - 1]
        if cue_pitch.diatonic_tone not in self._tones:
            raise Exception('Tone \'{0}\' is not in tonality \'{1}\''.format(cue_pitch.diatonic_tone, tonality))
        self._tone_index = self._tones.index(cue_pitch.diatonic_tone)
        self._flip_type = flip_type
        self._scale_origin_octave = cue_pitch.octave
        self._domain_pitch_range = domain_pitch_range
        self._cue_tone = cue_pitch.diatonic_tone

        self._tonal_function = self._build_tonal_function()

        GeneralPitchFunction.__init__(self, self._build_pitch_map())

    @property
    def flip_type(self):
        return self._flip_type

    @property
    def cue_tone(self):
        return self._cue_tone

    @property
    def tones(self):
        return self._tones

    @property
    def tonality(self):
        return self._tonality

    @property
    def tonal_function(self):
        return self._tonal_function

    @property
    def domain_pitch_range(self):
        return self._domain_pitch_range

    def _build_tonal_function(self):
        cycles = []
        n_tones = len(self.tones)
        if self.flip_type == FlipType.CenterTone:
            cycles.append([self.cue_tone])
            pairs = (n_tones - 1) // 2 if n_tones % 2 == 1 else (n_tones - 2) // 2
            for i in range(1, pairs + 1):
                low = (self._tone_index - i) % n_tones
                high = (self._tone_index + i) % n_tones
                cycles.append([self.tones[low], self.tones[high]])
            if n_tones % 2 == 0:
                extra = (self._tone_index - pairs - 1) % n_tones
                cycles.append([self.tones[extra]])
        else:
            low_idx = self._tone_index if self.flip_type == FlipType.LowerNeighborOfPair else self._tone_index - 1
            high_idx = low_idx + 1
            pairs = (n_tones - 1) // 2 if n_tones % 2 == 1 else n_tones // 2
            for i in range(0, pairs):
                low = (low_idx - i) % n_tones
                high = (high_idx + i) % n_tones
                cycles.append([self.tones[low], self.tones[high]])
            if n_tones % 2 == 0:
                extra = (self._tone_index - pairs) % n_tones
                cycles.append([self.tones[extra]])

        pure_map = TonalityPermutationFunction.create(self.tonality, cycles)

        extension = self._build_chromatic_extension(pure_map)
        extended_map = TonalityPermutationFunction.create(self.tonality, cycles, extension)

        return extended_map

    def _build_pitch_map(self):
        imap = dict()
        n_tones = len(self.tones)
        if self.flip_type == FlipType.CenterTone:
            upper = lower = self._tone_index
            upper_octave = lower_octave = self._scale_origin_octave
            upper_tone = self.cue_tone
            lower_tone = self.tonal_function[self.cue_tone]
            imap[DiatonicPitch(lower_octave, lower_tone)] = DiatonicPitch(upper_octave, upper_tone)
        else:
            if self.flip_type == FlipType.LowerNeighborOfPair:
                lower = self._tone_index
                upper = (lower + 1) % n_tones
                lower_tone = self.tones[lower]
                upper_tone = self.tonal_function[lower_tone] #self.tones[upper]
                lower_octave = self._scale_origin_octave
                upper_octave = self._scale_origin_octave + 1 if DiatonicPitch.crosses_c(lower_tone, upper_tone, True)\
                    else self._scale_origin_octave
            else:
                upper = self._tone_index
                lower = (upper - 1) % n_tones
                lower_tone = self.tones[lower]
                upper_tone = self.tonal_function[lower_tone] #self.tones[upper]
                upper_octave = self._scale_origin_octave
                lower_octave = self._scale_origin_octave if not DiatonicPitch.crosses_c(lower_tone, upper_tone, True) \
                    else self._scale_origin_octave - 1

            lower_pitch = DiatonicPitch(lower_octave, lower_tone)
            upper_pitch = DiatonicPitch(upper_octave, upper_tone)
            imap[lower_pitch] = upper_pitch
            imap[upper_pitch] = lower_pitch

        entered_range = False
        while True:
            lower = (lower - 1) % n_tones
            upper = (upper + 1) % n_tones
            if DiatonicPitch.crosses_c(lower_tone, self._tones[lower], False):
                lower_octave = lower_octave - 1
            if DiatonicPitch.crosses_c(upper_tone, self._tones[upper], True):
                upper_octave = upper_octave + 1
            lower_tone = self._tones[lower]
            upper_tone = self.tonal_function[lower_tone]

            lower_pitch = DiatonicPitch(lower_octave, lower_tone)
            upper_pitch = DiatonicPitch(upper_octave, upper_tone)
            if upper_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                    upper_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                break
            if lower_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                    lower_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                break
            if entered_range:
                if not self._domain_pitch_range.is_pitch_inbounds(lower_pitch) and \
                    not self._domain_pitch_range.is_pitch_inbounds(upper_pitch):
                    break
            elif self._domain_pitch_range.is_pitch_inbounds(lower_pitch) or \
                self._domain_pitch_range.is_pitch_inbounds(upper_pitch):
                entered_range = True
            else:
                continue
            imap[lower_pitch] = upper_pitch
            imap[upper_pitch] = lower_pitch

        return self._build_non_tonal_pitch_map(imap)

    def __getitem__(self, pitch):
        if pitch is None:
            return None
        if not isinstance(pitch, DiatonicPitch) and not isinstance(pitch, str):
            raise Exception('Map only good for diatonic pitch or string, not {0}'.format(type(pitch)))
        if isinstance(pitch, str):
            pitch = DiatonicPitch.parse(pitch)
            if pitch is None:
                raise Exception('Illegal pitch string representation {0}.'.format(pitch))
        if pitch in self.map.keys():
            return super(DiatonicPitchReflectionFunction, self).__getitem__(pitch)
        print('++++++ calling map non tonality pitch')
        raise Exception('Flip cannot map \'{0}\', not in keys.'.format(pitch))

    def __str__(self):
        return str(self.tonal_function)

    def _build_non_tonal_pitch_map(self, pmap):
        octave_start = self._domain_pitch_range.start_index // 12
        octave_end = self._domain_pitch_range.end_index // 12
        for octave in range(octave_start, octave_end + 1):
            for l in 'ABCDEFG':
                for aug in ['bb', 'b', '', '#', "##"]:
                    p = DiatonicPitch(octave, DiatonicFoundation.get_tone(l + aug))
                    if self._domain_pitch_range.is_pitch_inbounds(p) and p not in pmap.keys():
                        closest_p, closest_distance = self._find_closest_pitch(p)
                        if closest_p not in pmap.keys():
                            continue
                        closest_p_prime = pmap[closest_p]
                        t = self.tonal_function[p.diatonic_tone]
                        if closest_p > p:
                            o = closest_p_prime.octave + 1 if DiatonicPitch.crosses_c(closest_p_prime.diatonic_tone,
                                                                                      t,
                                                                                      True) else closest_p_prime.octave
                        else:
                            o = closest_p_prime.octave - 1 if DiatonicPitch.crosses_c(closest_p_prime.diatonic_tone,
                                                                                      t,
                                                                                      False) else closest_p_prime.octave
                        p_prime = DiatonicPitch(o, t)
                        pmap[p] = p_prime
                        # The mapping is not-symmetrical. e.g. E-pentatonic reflection_tests on G#, f(A#)->G and f(g)->G##
        return pmap

    '''
    Approach to chromatic interpretation.
    
    Given a non-tonal tone/pitch, to what should it map?
    The approach is the following for pitch P:
    1) If the tone ltr l of P is in the tonality, get the actual tone L of l. Devise an augmentation 'aug' 
       that modifies L to P's tone. Map L to L' with the tonal function. 
       Change aug to its complement aug'. 
       Liquidate aug' with L's augmentation. Use that tone.
       e.g. P = F#, l=F, L=F, aug=# F-->D (L'==D). aug'=b : F#-->Db!
    2) If the tone ltr l of P has no augmented counterpart in the tonality, 
            find a tone P' in the tonality that is closest to P (in half-steps).
       Let s be the number of diatonic steps from P to P', e.g. Eb to D# is s=-1.   
       Map P' --> P'' using the tonal map. 
       Let tone T be the pure tone '-s' diatonic steps from P''. 
       Form the pitch Q based on T and correct octave (requires octave cross check).
       Modify Q with an augmentation to get same half step distance to P'', as P is from P'. 
       
       Note: concerning pitch comparision.
       DiatonicPitch comparison is primarily based on comparing chromatic_distance, and for equality, ensuring the
       DiatonicTones are exactly the same. There is no allowance for enharmonic equality.
       In our logic below, we need to alter that comparision. Comparing chromatic_distance covers < and > just fine.
       However, given say G#:4 and Ab:4 or worse B#:4 and C:5, we need for this logic that in each case the former 
       precedes the latter (I hesitate to say 'less than'), giving a sort of order to enharmonic tones. This is
       important here, since the tone letter makes a big difference when computing chromatic locality.
       The ordering of enharmonic pitches is based on:
       1) Ensuring the pitches match chromatic distance, i.e. they are enharmonic.
       2) The tones are not more than 2 letters apart, i.e. their indices are within 2.
       Loosely for A < B, using indices 'CDEFGAB', B.index - A.index in [1, 2, -5, -6]
                               consider D<E (1) or B<C (-6) 
               for A > B, B.index - A.index in [-1, -2, 5, 6]
               
       Why not use intervals to do these calclations? Intervals do not support some of the stretches, e.g. Cb to C# is
        in E major pentatonic, a doubly-augmented Perfect. If we extend interval to doubly augmented/diminished
        intervals, it would be worth considering.  Ref. test E##:5' == str(f['Cb:4'])
    '''

    def _find_closest_pitch(self, pitch):
        """
        Given a pitch, find the scale pitch closest to it in chromatic distance.
        :param pitch:
        :return:
           1) closest in half-steps pitch in tonality.
           2) chromatic distance measured from closest pitch to given pitch.
        Note: algorithm looks for tonal pitches with same letter as pitch first, otherwise nearest non-tonal pitch.
        """
        start_octave = max(pitch.octave - 1, ChromaticScale.CHROMATIC_START[0])
        end_octave = min(pitch.octave + 1, ChromaticScale.CHROMATIC_END[0])

        # Compute the first and last pitches within the start/end octave range. To build a PitchScale
        first_pitch = None
        for t in self.tonality.annotation:
            first_pitch = DiatonicPitch(start_octave, t)
            if DiatonicFoundation.get_chromatic_distance(first_pitch) >= ChromaticScale.chromatic_start_index():
                break

        last_pitch = None
        loop_finished = False
        for o in range(end_octave, end_octave - 2, -1):
            if loop_finished:
                break
            for t in reversed(self.tonality.annotation):
                last_pitch = DiatonicPitch(o, t)
                if DiatonicFoundation.get_chromatic_distance(last_pitch) <= ChromaticScale.chromatic_end_index():
                    loop_finished = True
                    break

        scale = PitchScale(self.tonality, PitchRange.create(first_pitch, last_pitch))

        # determine if pitch ltr is in tonality, get that tone
        ll = [t for t in self.tones if t.diatonic_letter == pitch.diatonic_tone.diatonic_letter]
        if len(ll) == 1:
            pp = DiatonicPitch(pitch.octave, ll[0])
            return pp, pitch.chromatic_distance - pp.chromatic_distance

        # Do something if len(ll) > 1
        elif len(ll) > 1:
            ll.sort(key=lambda x: abs(x.augmentation_offset - pitch.diatonic_tone.augmentation_offset))
            pp = DiatonicPitch(pitch.octave, ll[0])
            return pp, pitch.chromatic_distance - pp.chromatic_distance

        before_pitch = first_pitch
        after_pitch = last_pitch
        for p in scale.pitch_scale:
            if pitch.chromatic_distance <= p.chromatic_distance:
                after_pitch = p
                break
            else:
                before_pitch = p

        before_distance = pitch.chromatic_distance - before_pitch.chromatic_distance
        after_distance = pitch.chromatic_distance - after_pitch.chromatic_distance

        if pitch.diatonic_tone.diatonic_letter == before_pitch.diatonic_tone.diatonic_letter:
            closest_distance = before_distance
            closest_pitch = before_pitch
        elif pitch.diatonic_tone.diatonic_letter == after_pitch.diatonic_tone.diatonic_letter:
            closest_distance = after_distance
            closest_pitch = after_pitch
        else:
            if abs(before_distance) < abs(after_distance):
                closest_distance = before_distance
                closest_pitch = before_pitch
            else:
                closest_distance = after_distance
                closest_pitch = after_pitch

        return closest_pitch, closest_distance

    def _build_chromatic_extension(self, pure_tonal_map):
        m = dict()
        for c in 'ABCDEFG':
            for aug in ['bb', 'b', '', '#', '##']:
                tone = DiatonicToneCache.get_tone(c + aug)
                if tone not in pure_tonal_map.tonality_permutation.tone_domain:
                    m[tone] = self._map_non_tonality_tone(tone, pure_tonal_map)
        return m

    def _map_non_tonality_tone(self, ttone, pure_tonal_map):
        # Get the closest tone in terms of chromatic distance.
        closest_tone, closest_distance = self._find_closest_tone(ttone)

        dd = closest_tone.diatonic_index - ttone.diatonic_index
        # Look for octave crossing.  if dd in {-5, -6] closest pitch is one octave up.
        if dd in [-5, -6]:  # [1, 2] are alright.  pitch < closest_pitch
            dd = (7 + dd) % 7
        elif dd in [5, 6]:  # [-1, -2] are alright.  pitch > closest_pitch
            dd = dd - 7

        closest_tone_target = pure_tonal_map[closest_tone]
        index = (closest_tone_target.diatonic_index + dd) % 7
        tone = DiatonicToneCache.get_tone('CDEFGAB'[index])

        # Octave 4 is chosen arbitrarily, and using dd we determine if ttone and closest need different
        # octave assignments.  We do this in order to get accurate chromatic distances below.
        if dd < 0:
            octave = 3 if DiatonicPitch.crosses_c(tone, closest_tone_target, True) else 4
        elif dd > 0:
            octave = 5 if DiatonicPitch.crosses_c(tone, closest_tone_target, False) else 4
        else:
            octave = 4

        target_pitch = DiatonicPitch(octave, tone)
        actual_distance = target_pitch.chromatic_distance - DiatonicPitch(4, closest_tone_target).chromatic_distance
        # recall: closest_distance is chrom. dist to get from closest pitch to pitch: we are on 'other side', so
        #         we use the negative of it.
        correction = closest_distance - actual_distance

        if correction == 0:
            return tone
        result_tone = DiatonicTone.alter_tone_by_augmentation(tone, correction)

        return result_tone

    def _find_closest_tone(self, tone):
        # determine if pitch ltr is in tonality, get that tone
        ll = [t for t in self.tones if t.diatonic_letter == tone.diatonic_letter]
        if len(ll) == 1:
            return ll[0], ll[0].augmentation_offset - tone.augmentation_offset

        # Do something if len(ll) > 1
        elif len(ll) > 1:
            ll.sort(key=lambda x: abs(x.augmentation_offset - tone.augmentation_offset))
            return ll[0], ll[0].augmentation_offset - tone.augmentation_offset

        first_pitch = DiatonicPitch(3, self.tones[0])
        last_pitch = DiatonicPitch(5, self.tones[-1])
        scale = PitchScale(self.tonality, PitchRange.create(first_pitch, last_pitch))

        pitch = DiatonicPitch(4, tone)
        after_pitch = last_pitch
        before_pitch = None
        for p in scale.pitch_scale:
            if pitch.chromatic_distance <= p.chromatic_distance:
                after_pitch = p
                break
            else:
                before_pitch = p

        # distance measured FROM pitch TO near pitch (e.g., -1 before, +1 after)
        before_distance = before_pitch.chromatic_distance - pitch.chromatic_distance
        after_distance = after_pitch.chromatic_distance - pitch.chromatic_distance

        if abs(before_distance) < abs(after_distance):
            closest_distance = before_distance
            closest_pitch = before_pitch
        else:
            closest_distance = after_distance
            closest_pitch = after_pitch

        return closest_pitch.diatonic_tone, closest_distance
