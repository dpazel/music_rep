"""
File: intervallic_key_change_pitch_functiony.py

Purpose: Class defining a pitch function based on shifting a tonality by an interval.

"""
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_foundation import DiatonicFoundation
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.interval import Interval
from tonalmodel.pitch_range import PitchRange
from transformation.functions.pitchfunctions.general_pitch_function import GeneralPitchFunction
from transformation.functions.tonalfunctions.cross_tonality_shift_tonal_function import \
    CrossTonalityShiftTonalFunction


class CrossTonalityShiftPitchFunction(GeneralPitchFunction):

    def __init__(self, domain_tonality, domain_pitch_range, root_shift_interval=None,
                 inherent_modality_type=None, modal_index=0):
        """
        Constructor.
        :param domain_tonality:
        :param domain_pitch_range:
        :param root_shift_interval: interval mapping first domain tone to first range tone.
        :param inherent_modality_type: alternative modality type (not modal index)
        :param modal_index: alternative index
        """

        self.__root_shift_interval = Interval.parse('P:1') if root_shift_interval is None else root_shift_interval
        range_modality_type = domain_tonality.modality.modality_type if inherent_modality_type is None \
            else inherent_modality_type

        self.__domain_tonality = domain_tonality

        self.__domain_pitch_range = domain_pitch_range
        self.__modal_index = modal_index

        # Take the root tone from the domain tonality, shift it by the interval, to produce new_root.
        # That new root has to be the modal_index-th tone in some new tonality.
        new_root = self.__root_shift_interval.get_end_tone(domain_tonality.root_tone)
        self.__tonal_function = CrossTonalityShiftTonalFunction(domain_tonality, new_root, self.__modal_index,
                                                                range_modality_type)
        self.__range_tonality = self.tonal_function.range_tonality
        if domain_tonality.cardinality != self.__range_tonality.cardinality:
            raise Exception('domain and range tonalities must have same cardinality')

        self.__range_pitch_range = None

        GeneralPitchFunction.__init__(self, self._build_pitch_map())

    @property
    def domain_tonality(self):
        return self.__domain_tonality

    @property
    def root_shift_interval(self):
        return self.__root_shift_interval

    @property
    def domain_pitch_range(self):
        return self.__domain_pitch_range

    @property
    def range_tonality(self):
        return self.__range_tonality

    @property
    def tonal_function(self):
        return self.__tonal_function

    @property
    def range_pitch_range(self):
        return self.__range_pitch_range

    def __getitem__(self, pitch):
        if pitch is None:
            return None
        if not isinstance(pitch, DiatonicPitch) and not isinstance(pitch, str):
            raise Exception('Map only good for diatonic pitch or string, not {0}'.format(type(pitch)))
        if isinstance(pitch, str):
            pitch = DiatonicPitch.parse(pitch)
            if pitch is None:
                raise Exception('Illegal pitch string representation {0}.'.format(pitch))
        if not self.domain_pitch_range.is_pitch_inbounds(pitch):
            return None
        if pitch in self.map.keys():
            return super(CrossTonalityShiftPitchFunction, self).__getitem__(pitch)
        raise Exception('\'{0}\' illegal pitch for this pitch function.'.format(pitch))

    def _build_pitch_map(self):
        pitch_map = dict()

        lo_reg = self.domain_pitch_range.start_index // 12
        hi_reg = self.domain_pitch_range.end_index // 12

        domain_start_tone = CrossTonalityShiftPitchFunction.compute_lowest_letter(
            self.domain_pitch_range.start_index % 12)

        # note letter template should start with letter for domain_start_tone
        note_letters = 'ABCDEFG'
        i = note_letters.index(domain_start_tone.diatonic_letter)
        note_letters = note_letters[i:] + note_letters[:i]

        domain_tones = list()
        for ltr in note_letters:
            for aug in ['bb', 'b', '', '#', '##']:
                domain_tones.append(DiatonicFoundation.get_tone(ltr + aug))

        first_domain_pitch = None
        first_range_pitch = None
        last_domain_pitch = None
        last_range_pitch = None
        for register in range(lo_reg, hi_reg + 1):
            domain_reg = register
            target_pitch = self.root_shift_interval.get_end_pitch(DiatonicPitch(domain_reg, domain_start_tone))
            range_reg = target_pitch.octave
            range_start_tone = target_pitch.diatonic_tone
            domain_reg_upped = False
            range_reg_upped = False
            for tone in domain_tones:
                if not domain_reg_upped and tone.diatonic_letter == 'C' and domain_start_tone.diatonic_letter != 'C':
                    domain_reg = domain_reg + 1
                    domain_reg_upped = True
                domain_pitch = DiatonicPitch(domain_reg, tone)
                if domain_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                        domain_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                    continue
                if self.domain_pitch_range.is_pitch_inbounds(domain_pitch):
                    range_tone = self.tonal_function[tone]
                    if not range_reg_upped and range_tone.diatonic_letter == 'C' and \
                            range_start_tone.diatonic_letter != 'C':
                        range_reg = range_reg + 1
                        range_reg_upped = True
                    target_pitch = DiatonicPitch(range_reg, range_tone)
                    if target_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                            target_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                        continue
                    pitch_map[domain_pitch] = target_pitch
                    if first_domain_pitch is None:
                        first_domain_pitch = domain_pitch
                        first_range_pitch = target_pitch
                    last_domain_pitch = domain_pitch
                    last_range_pitch = target_pitch

        if first_domain_pitch.chromatic_distance > last_domain_pitch.chromatic_distance:
            self.__domain_pitch_range = PitchRange.create(last_domain_pitch, first_domain_pitch)
        else:
            self.__domain_pitch_range = PitchRange.create(first_domain_pitch, last_domain_pitch)

        if first_range_pitch.chromatic_distance > last_range_pitch.chromatic_distance:
            self.__range_pitch_range = PitchRange.create(last_range_pitch, first_range_pitch)
        else:
            self.__range_pitch_range = PitchRange.create(first_range_pitch, last_range_pitch)
        return pitch_map

    def _build_pitch_map1(self):
        pitch_map = dict()

        lo_reg = self.domain_pitch_range.start_index // 12
        hi_reg = self.domain_pitch_range.end_index // 12

        domain_start_tone = CrossTonalityShiftPitchFunction.compute_lowest_letter(
            self.domain_pitch_range.start_index % 12)   # self.domain_tonality.annotation[0]
        range_start_tone = CrossTonalityShiftPitchFunction.compute_highest_letter(
            self.domain_pitch_range.end_index % 12)     # self.range_tonality.annotation[0]

        # note letter template should start with letter for domain_start_tone
        note_letters = 'ABCDEFG'
        i = note_letters.index(domain_start_tone.diatonic_letter)
        note_letters = note_letters[i:] + note_letters[:i]

        domain_tones = list()
        for ltr in note_letters:
            for aug in ['bb', 'b', '', '#', '##']:
                domain_tones.append(DiatonicFoundation.get_tone(ltr + aug))

        first_domain_pitch = None
        first_range_pitch = None
        last_domain_pitch = None
        last_range_pitch = None
        for register in range(lo_reg, hi_reg + 1):
            domain_reg = register
            target_pitch = self.root_shift_interval.get_end_pitch(DiatonicPitch(domain_reg, domain_start_tone))
            range_reg = target_pitch.octave
            domain_reg_upped = False
            range_reg_upped = False
            for tone in domain_tones:
                if not domain_reg_upped and tone.diatonic_letter == 'C' and domain_start_tone.diatonic_letter != 'C':
                    domain_reg = domain_reg + 1
                    domain_reg_upped = True
                domain_pitch = DiatonicPitch(domain_reg, tone)
                if domain_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                        domain_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                    continue
                if self.domain_pitch_range.is_pitch_inbounds(domain_pitch):
                    range_tone = self.tonal_function[tone]
                    if not range_reg_upped and range_tone.diatonic_letter == 'C' and \
                            range_start_tone.diatonic_letter != 'C':
                        range_reg = range_reg + 1
                        range_reg_upped = True
                    target_pitch = DiatonicPitch(range_reg, range_tone)
                    if target_pitch.chromatic_distance < ChromaticScale.chromatic_start_index() or \
                            target_pitch.chromatic_distance > ChromaticScale.chromatic_end_index():
                        continue
                    pitch_map[domain_pitch] = target_pitch
                    if first_domain_pitch is None:
                        first_domain_pitch = domain_pitch
                        first_range_pitch = target_pitch
                    last_domain_pitch = domain_pitch
                    last_range_pitch = target_pitch

        if first_domain_pitch.chromatic_distance > last_domain_pitch.chromatic_distance:
            self.__domain_pitch_range = PitchRange.create(last_domain_pitch, first_domain_pitch)
        else:
            self.__domain_pitch_range = PitchRange.create(first_domain_pitch, last_domain_pitch)

        if first_range_pitch.chromatic_distance > last_range_pitch.chromatic_distance:
            self.__range_pitch_range = PitchRange.create(last_range_pitch, first_range_pitch)
        else:
            self.__range_pitch_range = PitchRange.create(first_range_pitch, last_range_pitch)
        return pitch_map

    @staticmethod
    def compute_lowest_letter(index):
        ltrs = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[index]
        l_tone = DiatonicTone.DIATONIC_LETTERS[min([DiatonicTone.DIATONIC_INDEX_MAPPING[s[0]] for s in ltrs])]
        return DiatonicToneCache.get_tone(l_tone)

    @staticmethod
    def compute_highest_letter(index):
        ltrs = DiatonicTone.DIATONIC_OFFSET_ENHARMONIC_MAPPING[index]
        l_tone = DiatonicTone.DIATONIC_LETTERS[max([DiatonicTone.DIATONIC_INDEX_MAPPING[s[0]] for s in ltrs])]
        return DiatonicToneCache.get_tone(l_tone)
