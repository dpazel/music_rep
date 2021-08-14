"""

File: t_shift.py

Purpose: Transformation to change to tonality of same cardinality, based on interval shift of scalar root pitch.

"""
from fractions import Fraction

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.chord_classifier import ChordClassifier
from harmonicmodel.secondary_chord import SecondaryChord
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from timemodel.duration import Duration
from timemodel.position import Position
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.modality import ModalityType
from tonalmodel.pitch_range import PitchRange
from tonalmodel.tonality import Tonality
from misc.interval import Interval
from tonalmodel.interval import Interval as TonalInterval
from transformation.transformation import Transformation
from transformation.functions.pitchfunctions.cross_tonality_shift_pitch_function import CrossTonalityShiftPitchFunction

from itertools import islice


class TShift(Transformation):

    def __init__(self, source_line, source_hct, default_root_shift_interval=None, default_modal_index=None,
                 default_range_modality_type=None):
        """
        Constructor
        :param source_line: Melodic Line being shifted
        :param source_hct: Harmonic Context Track being shifted
        :param default_root_shift_interval: Interval of shift from old to new key
        :param default_modal_index: modal index for key note to serve as root of key
        :param default_range_modality_type: specifies modality type of new key. If none, use original.
        Note: default_range_modality_type applies to any key in source_hct hc's.
        """

        #if default_range_modality_type is not None:
        #   if isinstance(default_range_modality_type, int):
        #        default_range_modality_type = ModalityType(default_range_modality_type)

        if default_root_shift_interval is None:
            default_root_shift_interval = TonalInterval.parse('P:1')

        self.__source_line = source_line
        self.__source_hct = source_hct
        self.__domain_pitch_range = TShift.compute_pitch_range(source_line)
        self.__default_root_shift_interval_interval = default_root_shift_interval
        self.__default_modal_index = default_modal_index
        self.__default_range_modality_type = default_range_modality_type

        self.temporal_extent = None
        self.keep_hct = None
        self.pre_extent = None
        self.post_extent = None

        self.hc_pitch_function_map = dict()

        self.root_shift_interval = None
        self.modal_index = None
        self.range_modality_type = None

        Transformation.__init__(self)

    @staticmethod
    def create(source_expression, default_root_shift_interval=None, default_range_modality_type=None):
        lge = LineGrammarExecutor()
        source_line, source_hct = lge.parse(source_expression)
        return TShift(source_line, source_hct, default_root_shift_interval, default_range_modality_type)

    @staticmethod
    def create_intervallic_shift(source_line, source_hct, interval, modal_index):
        # make default interval P:1 and use modal_index for diatonic shift
        return TShift(source_line, source_hct, interval, modal_index, None)

    @staticmethod
    def create_modal_shift(source_line, source_hct, modal_index):
        #       c shift 4 mean C+ --> C Lydian, i.e. a modal rotation of C
        return TShift(source_line, source_hct, None, modal_index,  None)

    @property
    def source_line(self):
        return self.__source_line

    @property
    def source_hct(self):
        return self.__source_hct

    @property
    def default_root_shift_interval(self):
        return self.__default_root_shift_interval_interval

    @property
    def domain_pitch_range(self):
        return self.__domain_pitch_range

    @property
    def default_modal_index(self):
        return self.__default_modal_index

    @property
    def default_range_modality_type(self):
        return self.__default_range_modality_type

    def apply(self, temporal_extent=None, root_shift_interval=None, modal_index=None, range_modality_type=None,
              as_copy=True):
        """
        Apply transform to a temporal extent.
        :param temporal_extent: numerical interval indicating start/end offsets on line to apply shift.
                                Interval from misc.interval
        :param root_shift_interval: root tone shift.
        :param modal_index: modal index for the new key.
        :param range_modality_type: modality type for the new key.
        :param as_copy: True means to return copys of line, hct as source_line, source_hct would be modified otherwise.
        :return: modified line and hct (as objects, the same as passed in.)
        """
        # If temporal_extent is None, use the whole range of hct.
        self.temporal_extent = temporal_extent if temporal_extent is not None else \
            Interval(Fraction(0), self.source_hct.duration.duration)

        self.pre_extent = None if self.temporal_extent.lower == 0 else Interval(0, self.temporal_extent.lower)
        self.post_extent = None if self.temporal_extent.upper >= self.source_line.duration else \
            Interval(self.temporal_extent.upper, self.source_line.duration.duration)

        self.root_shift_interval = self.default_root_shift_interval if root_shift_interval is None \
            else root_shift_interval
        self.modal_index = self.default_modal_index if modal_index is None else modal_index

        if range_modality_type is not None and isinstance(range_modality_type, int):
            range_modality_type = ModalityType(range_modality_type)
        self.range_modality_type = self.default_range_modality_type if range_modality_type is None \
            else range_modality_type

        self.hc_pitch_function_map = dict()

        score_line = self._reset_pitches(as_copy)

        score_hct = self._rebuild_hct(self.source_hct, as_copy)

        return score_line, score_hct

    def _reset_pitches(self, as_copy):
        line = self.source_line.clone() if as_copy else self.source_line
        last_hc = None
        for note in line.get_all_notes():
            if self.temporal_extent.contains(note.get_absolute_position().position):
                hc = self.source_hct.get_hc_by_position(note.get_absolute_position())
                if last_hc != hc:
                    f, _ = self._build_shift_function(hc)
                    last_hc = hc
                note.diatonic_pitch = f[note.diatonic_pitch]

        return line

    @staticmethod
    def _sign(x):
        return 1 if x > 0 else -1

    def _rebuild_hct(self, orig_hct, as_copy):
        hc_list = orig_hct.hc_list()
        if not as_copy:
            orig_hct.clear()
        new_hct = HarmonicContextTrack() if as_copy else orig_hct
        next_index = 0
        position = Position(0)
        if self.pre_extent is not None:
            for hc in hc_list:
                intersect = hc.extent.intersection(self.pre_extent)
                if intersect is None:
                    break
                duration = Duration(min(intersect.length(), hc.duration.duration))
                new_hc = HarmonicContext(hc.tonality, hc.chord, duration, hc.position)
                new_hct.append(new_hc)
                position += new_hc.duration
                if hc.extent.upper > self.pre_extent.upper:
                    break
                next_index += 1

        for hc in islice(hc_list, next_index, None):
            intersect = hc.extent.intersection(self.temporal_extent)
            if intersect is None:
                break
            duration = Duration(intersect.length())
            if self.keep_hct:
                new_hc = HarmonicContext(hc.tonality, hc.chord, duration, position)
            else:
                f, range_tonality = self._build_shift_function(hc)
                # TODO: the range tonality below is incorrect.
                new_hc = HarmonicContext(range_tonality, self.remap_chord(hc, f.range_tonality), duration, position)
            new_hct.append(new_hc)
            position += new_hc.duration
            if hc.extent.upper > self.temporal_extent.upper:
                break
            next_index += 1

        if self.post_extent is not None:
            for hc in islice(hc_list, next_index, None):
                intersect = hc.extent.intersection(self.post_extent)
                if intersect is None:
                    break
                duration = Duration(intersect.length())
                new_hc = HarmonicContext(hc.tonality, hc.chord, duration, position)
                new_hct.append(new_hc)
                position += new_hc.duration

        return new_hct

    def _build_shift_function(self, hc):
        if hc in self.hc_pitch_function_map.keys():   # reuse
            return self.hc_pitch_function_map[hc]

        if not isinstance(hc.chord, SecondaryChord):
            f = CrossTonalityShiftPitchFunction(hc.tonality,
                                                self.domain_pitch_range,
                                                self.root_shift_interval,
                                                self.range_modality_type,
                                                self.modal_index if self.modal_index is not None
                                                else hc.tonality.modal_index)
            range_tonality = f.range_tonality
        else:
            if self.root_shift_interval:
                range_tonality = Tonality.create(self.range_modality_type if self.range_modality_type is not None else hc.tonality.modality_type,
                                                 self.root_shift_interval.get_end_tone(hc.tonality.diatonic_tone),
                                                 self.modal_index if self.modal_index is not None else hc.tonality.modal_index)
            else:
                range_tonality = hc.tonality


            # Range tone is the tone from the denominator, e.g. the ii in V/ii.
            range_tone = range_tonality.annotation[hc.chord.chord_template.secondary_scale_degree - 1]
            #root_tone_interval = TShift.calculate_interval(hc.chord.secondary_tonality.root_tone,
            #                                               range_tone,
            #                                               self.root_shift_interval)

            root_tone_interval = TonalInterval.calculate_tone_interval(hc.chord.secondary_tonality.root_tone, range_tone) \
                                     if not TonalInterval.is_negative(self.root_shift_interval) else  \
                                 -TonalInterval.calculate_tone_interval(range_tone, hc.chord.secondary_tonality.root_tone)

            f = CrossTonalityShiftPitchFunction(hc.chord.secondary_tonality,
                                                self.domain_pitch_range,
                                                root_tone_interval,
                                                hc.chord.secondary_tonality.modality_type,
                                                hc.chord.secondary_tonality.modal_index)
        self.hc_pitch_function_map[hc] = (f, range_tonality)
        return f, range_tonality

    @staticmethod
    def calculate_interval(tone_1, tone_2, near_interval):
        """
        The purpose of this method is to find a transform interval close to 'near_interval'.  This is used
        to determine the transform interval for secondary chords, wherein the obvious jump does not match
        transform interval (e.g. major to minor scale), and as well must be adjusted for the number and sign of
        octaves nearest interval may have.  See test cases: test_modal_secondary_tonality where best_interval == d:4
        and near_interval == P:4 E-MM to Ab-MM using V/III chord.
        :param tone_1:
        :param tone_2:
        :param near_interval:
        :return:
        """
        sign = TShift._sign(near_interval.chromatic_distance)
        start, increment = (1, 1) if sign == 1 else (7, -1)
        p1 = DiatonicPitch(start, tone_1)
        oct_2 = start
        best = 100000
        best_interval = None
        while abs(oct_2) < 7:
            p2 = DiatonicPitch(oct_2, tone_2)
            i = TonalInterval.create_interval(p1, p2)
            if TShift._sign(i.chromatic_distance) != sign:
                oct_2 = oct_2 + sign
                continue
            diff = abs(near_interval.chromatic_distance - i.chromatic_distance)
            if diff < best:
                best = diff
                best_interval = i
            else:
                break
            oct_2 = oct_2 + sign
        return best_interval

    def remap_chord(self, hc, new_tonality):

        chord = hc.chord
        chord_tonality = new_tonality

        f, _ = self._build_shift_function(hc)

        if not isinstance(chord, SecondaryChord):
            new_chord_tones = [f.tonal_function[t[0]] for t in chord.tones]
            chords = ChordClassifier.classify_all_roots(new_chord_tones, chord_tonality)
            if chords is not None and len(chords) > 0:
                return chords[0]
            else:
                raise Exception('Cannot remap/classify chord {0} based on chord.'.format(
                    ', '.join(t.diatonic_symbol for t in new_chord_tones)))
        else:
            new_chord_tones = [f.tonal_function[t[0]] for t in chord.tones]
            chords = ChordClassifier.classify_all_roots(new_chord_tones, f.range_tonality)
            if chords is not None and len(chords) > 0:
                new_chord = chords[0]
            else:
                raise Exception('Cannot remap/classify chord {0} based on chord.'.format(
                    ', '.join(str(t) for t in new_chord_tones)))

            temp_range_tonality = Tonality.create(self.range_modality_type if self.range_modality_type is not None
                                                  else hc.tonality.modality_type,
                                                  self.root_shift_interval.get_end_tone(hc.tonality.diatonic_tone),
                                                  self.modal_index if self.modal_index is not None
                                                  else hc.tonality.modal_index) if self.root_shift_interval else \
                                                  hc.tonality

            secondary_chord_template = SecondaryChordTemplate(new_chord.chord_template,
                                                              chord.chord_template.secondary_scale_degree,
                                                              chord.secondary_tonality.modality.modality_type)
            secondary_chord = SecondaryChord(secondary_chord_template, temp_range_tonality)
            return secondary_chord

    @staticmethod
    def compute_pitch_range(line):
        notes = line.get_all_notes()
        max_pitch = min_pitch = notes[0].diatonic_pitch

        for i in range(1, len(notes)):
            pitch = notes[i].diatonic_pitch
            if pitch is None:
                continue
            if pitch < min_pitch:
                min_pitch = pitch
            elif pitch > max_pitch:
                max_pitch = pitch

        return PitchRange.create(min_pitch, max_pitch)