"""

File: t_diatonic_reflection.py

Purpose: Tranformation to diatonically reflection a portion of a line around or near a pitch.

"""
from fractions import Fraction

from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from tonalmodel.pitch_range import PitchRange
from transformation.transformation import Transformation
from misc.interval import Interval
from harmoniccontext.harmonic_context import HarmonicContext
from timemodel.duration import Duration
from timemodel.position import Position
from transformation.functions.pitchfunctions.diatonic_pitch_reflection_function import \
    FlipType, DiatonicPitchReflectionFunction
from harmonicmodel.chord_classifier import ChordClassifier
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from harmonicmodel.secondary_chord import SecondaryChord
from tonalmodel.diatonic_pitch import DiatonicPitch

from itertools import islice


class TDiatonicReflection(Transformation):
    """
    Transformation to reflection a scale over a cue pitch, across a pitch range on a line/hct
    Primary actions are:
       1) Transform the notes.
       2) Transform the chords.
    """

    def __init__(self, source_line, source_hct, default_cue_pitch, default_flip_type=FlipType.CenterTone):
        self.__source_line = source_line
        self.__source_hct = source_hct
        self.__default_cue_pitch = default_cue_pitch
        self.__domain_pitch_range = TDiatonicReflection.compute_pitch_range(source_line)
        self.__default_flip_type = default_flip_type

        self.temporal_extent = None
        self.keep_hct = None
        self.cue_pitch = None
        self.pre_extent = None
        self.post_extent = None
        self.flip_type = None

        self.hc_flip_map = dict()  # Maps hc to reflection_tests function - for reuse

        Transformation.__init__(self)

    @staticmethod
    def create(source_expression, default_cue_pitch):
        lge = LineGrammarExecutor()
        source_line, source_hct = lge.parse(source_expression)
        return TDiatonicReflection(source_line, source_hct, default_cue_pitch)

    @property
    def source_line(self):
        return self.__source_line

    @property
    def source_hct(self):
        return self.__source_hct

    @property
    def default_cue_pitch(self):
        return self.__default_cue_pitch

    @property
    def domain_pitch_range(self):
        return self.__domain_pitch_range

    @property
    def default_flip_type(self):
        return self.__default_flip_type

    def apply(self, temporal_extent=None, cue_pitch=None, flip_type=None, as_copy=True):
        """
        Apply the TFlip transform to a tempoaral extent.

        :param temporal_extent: misc.Interval
        :param cue_pitch:  Possible override of the cue pitch.
        :param flip_type:
        :param as_copy: True means to return copys of line, hct as source_line, source_hct would be modified otherwise.
        :return: modified line and hct (as objects, the same as passed in.)
        """
        # If temporal_extent is None, use the whole range of hct.
        self.temporal_extent = temporal_extent if temporal_extent is not None else \
            Interval(Fraction(0), self.source_hct.duration.duration)

        self.cue_pitch = self.default_cue_pitch if cue_pitch is None else cue_pitch
        self.flip_type = self.default_flip_type if flip_type is None else flip_type
        self.pre_extent = None if self.temporal_extent.lower == 0 else Interval(0, self.temporal_extent.lower)
        self.post_extent = None if self.temporal_extent.upper >= self.source_line.duration else\
            Interval(self.temporal_extent.upper, self.source_line.duration.duration)

        score_line = self._reset_pitches(as_copy)

        score_hct = self._rebuild_hct(self.source_hct, as_copy)

        return score_line, score_hct

    def _reset_pitches(self, as_copy):
        line = self.source_line.clone() if as_copy else self.source_line
        for note in line.get_all_notes():
            if self.temporal_extent.contains(note.get_absolute_position().position):
                hc = self.source_hct.get_hc_by_position(note.get_absolute_position())
                if hc not in self.hc_flip_map.keys():
                    if isinstance(hc.chord, SecondaryChord):
                        f = self._build_secondary_flip_function(hc)
                    else:
                        low, high = TDiatonicReflection._adjust_flip_cue_to_tonality(self.cue_pitch, hc.tonality)
                        if high is None:
                            f = DiatonicPitchReflectionFunction(hc.tonality, self.cue_pitch, self.domain_pitch_range,
                                                                self.flip_type)
                        else:
                            f = DiatonicPitchReflectionFunction(hc.tonality, low, self.domain_pitch_range,
                                                                FlipType.LowerNeighborOfPair)
                    self.hc_flip_map[hc] = f
                else:
                    f = self.hc_flip_map[hc]

                note.diatonic_pitch = f[note.diatonic_pitch]
        return line

    def _build_secondary_flip_function(self, hc):
        # Strategy - for secondary chords, we simply build a reflection for the secondary scale.
        #  The cue pitch is used if the cue pitch exists in the secondary scale.
        #  otherwise we build a reflection_tests around the neighboring pitches to the cue.
        #  This is about the simplest stragegy to use in this situation, and has credibility by virtue of using
        #  the same cue pitch.  However, it may result in irregular resolutions in chord
        #  sequences, like V/ii, ii
        secondary_tonality = hc.chord.secondary_tonality

        lo_cue_tone, hi_cue_tone = TDiatonicReflection._compute_cue_tone(self.cue_pitch.diatonic_tone,
                                                                         secondary_tonality)
        octave = self.cue_pitch.octave
        if hi_cue_tone is None:  # case where lo_cue_tone should be enharmonic to cue_pitch.diatonic_tone
            if self.cue_pitch.chromatic_distance < DiatonicPitch(octave, lo_cue_tone).chromatic_distance:
                octave = octave - 1
            elif self.cue_pitch.chromatic_distance > DiatonicPitch(octave, lo_cue_tone).chromatic_distance:
                octave = octave + 1

            lo_cue_pitch = DiatonicPitch(octave, lo_cue_tone)
            f = DiatonicPitchReflectionFunction(secondary_tonality, lo_cue_pitch, self.domain_pitch_range)
        else:
            if DiatonicPitch(octave, lo_cue_tone).chromatic_distance > self.cue_pitch.chromatic_distance:
                octave = octave - 1
            lo_cue_pitch = DiatonicPitch(octave, lo_cue_tone)
            f = DiatonicPitchReflectionFunction(secondary_tonality, lo_cue_pitch, self.domain_pitch_range,
                                                FlipType.LowerNeighborOfPair)

        #
        # Note: the above produces the same tonal function as TonalFunction.create_adapted_function
        #       The former uses a reversal based on the same cue scale index, while the latter
        #       would do that anyway by pickup up on the original note permutation derived from reflection_tests.
        #
        return f

    @staticmethod
    def _adjust_flip_cue_to_tonality(cue_pitch, tonality):
        tones = tonality.annotation[:-1]
        if cue_pitch.diatonic_tone in tones:
            return cue_pitch, None
        return TDiatonicReflection._compute_cue_tone(cue_pitch, tonality)

    @staticmethod
    def _compute_cue_tone(old_cue_tone, tonality):
        from misc.ordered_map import OrderedMap

        tones = tonality.annotation[:-1]
        s = OrderedMap({v.placement: tones.index(v) for v in tones})

        least_index = s[min(pl for pl in s.keys())]
        nearest_pl = s.floor(old_cue_tone.placement)
        if nearest_pl is None:
            return tones[-1 if least_index == 0 else least_index - 1], tones[least_index]

        if nearest_pl == old_cue_tone.placement:
            return tones[s[nearest_pl]], None

        nearest_idx = s[nearest_pl]
        return tones[nearest_idx], tones[nearest_idx + 1 if nearest_idx != len(tones) - 1 else 0]

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
                new_hc = HarmonicContext(hc.tonality, self.remap_chord(hc), duration, position)
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

    def remap_chord(self, hc):

        chord = hc.chord
        chord_tonality = hc.tonality

        if not isinstance(chord, SecondaryChord):
            f = self.hc_flip_map[hc] if hc in self.hc_flip_map.keys() else \
                DiatonicPitchReflectionFunction(hc.tonality, self.cue_pitch, self.domain_pitch_range)
            new_chord_tones = [f.tonal_function[t[0]] for t in chord.tones]
            chords = ChordClassifier.classify_all_roots(new_chord_tones, chord_tonality)
            if chords is not None and len(chords) > 0:
                return chords[0]
            else:
                raise Exception('Cannot remap/classify chord {0} based on chord.'.format(
                    ', '.join(str(t) for t in new_chord_tones)))
        else:
            secondary_tonality = chord.secondary_tonality
            if hc in self.hc_flip_map.keys():
                secondary_function = self.hc_flip_map[hc].tonal_function
            else:
                secondary_function = self._build_secondary_flip_function(hc).tonal_function

            # Alternatively, in the else part, we could have done:
            #   secondary_function = f.tonal_function.create_adapted_function(secondary_tonality, secondary_tonality)
            # but to be consistent within the logic, we go for the reflection_tests constructiobn
            # of the secondary function
            # as embodied in tFlip._build_secondary_flip_function()

            new_chord_tones = [secondary_function[t[0]] for t in chord.tones]
            chords = ChordClassifier.classify_all_roots(new_chord_tones, secondary_tonality)

            if chords is not None and len(chords) > 0:
                new_chord = chords[0]
            else:
                raise Exception('Cannot remap/classify chord {0} based on chord.'.format(
                    ', '.join(str(t) for t in new_chord_tones)))

            secondary_chord_template = SecondaryChordTemplate(new_chord.chord_template,
                                                              chord.chord_template.secondary_scale_degree,
                                                              secondary_tonality.modality.modality_type)
            secondary_chord = SecondaryChord(secondary_chord_template, chord_tonality)
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
