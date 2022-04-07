from fractions import Fraction
import enum

from misc.interval import Interval

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone import DiatonicTone
from timemodel.duration import Duration
from timemodel.position import Position
from transformation.transformation import Transformation
from harmonicmodel.chord_classifier import ChordClassifier
from harmonicmodel.secondary_chord import SecondaryChord
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate
from harmonicmodel.tertian_chord_template import TertianChordTemplate

from itertools import islice


class SecondaryShiftType(enum.Enum):
    Standard = 1   # Change the numerator of a secondary chord.
    Tonal = 2      # Change the denominator of a secondary chord.


class TStepShift(Transformation):

    def __init__(self, source_line, source_hct, default_secondary_shift_type=SecondaryShiftType.Standard):
        """
        Constructor
        :param source_line: The source Line of notes.
        :param source_hct: The source harmonic context track.
        :param default_secondary_shift_type: In the case of secondary chord harmonic context's, to do the shift
                                            standard or tanal. This sets a default, overriden by apply().
        """
        self.__source_line = source_line
        self.__source_hct = source_hct
        self.__default_secondary_shift_type = default_secondary_shift_type
        self.__secondary_shift_type = self.__default_secondary_shift_type
        self.step_increment = 1
        self.temporal_extent = None
        self.pre_extent = None
        self.post_extent = None
        self.hc_step_pitch_function_map = None

        Transformation.__init__(self)

    @property
    def source_line(self):
        return self.__source_line

    @property
    def source_hct(self):
        return self.__source_hct

    @property
    def default_secondary_shift_type(self):
        return self.__default_secondary_shift_type

    @property
    def secondary_shift_type(self):
        return self.__secondary_shift_type

    def apply(self, step_increment=0, temporal_extent=None, secondary_shift_type=None):
        """
        Do an apply action for this transform.
        :param step_increment: The number of scalar steps to do.
        :param secondary_shift_type: If not None, overrides the default setting of secondary_shift_type.
        :param temporal_extent: The temporal extent over which to transform
        :return: A new score line and new score hct reflecting the transform changes in the extent.
        """
        if step_increment is None or not isinstance(step_increment, int):
            raise Exception('Increment must be specified and be an integer.')
        self.step_increment = step_increment

        self.__secondary_shift_type = secondary_shift_type if secondary_shift_type is not None \
            else self.__default_secondary_shift_type

        # If temporal_extent is None, use the whole range of hct.
        self.temporal_extent = temporal_extent if temporal_extent is not None else \
            Interval(Fraction(0), self.source_hct.duration.duration)

        self.pre_extent = None if self.temporal_extent.lower == 0 else Interval(0, self.temporal_extent.lower)
        self.post_extent = None if self.temporal_extent.upper >= self.source_line.duration else \
            Interval(self.temporal_extent.upper, self.source_line.duration.duration)

        self.hc_step_pitch_function_map = dict()

        score_hct = self._rebuild_hct(self.source_hct)

        score_line = self._reset_pitches(score_hct)
        return score_line, score_hct

    def _rebuild_hct(self, orig_hct):
        hc_list = orig_hct.hc_list()
        new_hct = HarmonicContextTrack()

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

            new_hc = self.rebuild_hc(hc, position, duration)
            new_hct.append(new_hc)

            # TODO: this has to be called, but not sure what side effects are necessary.
            self._build_step_shift_function(new_hc, hc)

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

    def rebuild_hc(self, hc, position, duration):
        chord = hc.chord
        if isinstance(chord, SecondaryChord):
            chord = self.rebuild_secondary_chord(chord, hc.tonality)
            return HarmonicContext(hc.tonality, chord, duration, position)
        else:
            return HarmonicContext(hc.tonality, self.remap_chord(hc), duration, position)

    def _reset_pitches(self, score_hct):
        line = self.source_line.clone()
        last_hc = None
        f = None
        for note in line.get_all_notes():
            if self.temporal_extent.contains(note.get_absolute_position().position):
                hc = score_hct.get_hc_by_position(note.get_absolute_position() - self.temporal_extent.lower)
                if last_hc != hc:
                    f = self._build_step_shift_function(hc)
                    last_hc = hc
                if f is not None:
                    note.diatonic_pitch = f[note.diatonic_pitch]

        return line

    def _build_step_shift_function(self, hc, old_hc=None):
        if hc in self.hc_step_pitch_function_map.keys():   # reuse
            return self.hc_step_pitch_function_map[hc]

        if isinstance(hc.chord, SecondaryChord):
            if self.secondary_shift_type == SecondaryShiftType.Standard:
                f = PitchRemapFunction(hc.chord.secondary_tonality, self.step_increment)
            else:
                f = PitchRemapFunction(hc.chord.secondary_tonality,
                                       self.step_increment,
                                       old_hc.chord.secondary_tonality)
        else:
            f = PitchRemapFunction(hc.tonality, self.step_increment)

        self.hc_step_pitch_function_map[hc] = f
        return f

    def remap_chord(self, hc):

        chord = hc.chord
        chord_tonality = hc.tonality

        if isinstance(chord, SecondaryChord):
            return self.rebuild_secondary_chord(chord, chord_tonality)
        else:
            f = PitchRemapFunction(hc.tonality, self.step_increment)
            new_chord_tones = [f.tonal_function(t[0]) for t in chord.tones]
            chords = ChordClassifier.classify_all_roots(new_chord_tones, chord_tonality)
            if chords is not None and len(chords) > 0:
                return chords[0]
            else:
                raise Exception('Cannot remap/classify chord {0} based on chord.'.format(
                    ', '.join(t.diatonic_symbol for t in new_chord_tones)))

    def rebuild_secondary_chord(self, secondary_chord, base_tonality):
        if self.secondary_shift_type == SecondaryShiftType.Standard:
            orig_principal_chord_template = secondary_chord.chord_template.principal_chord_template
            if not isinstance(orig_principal_chord_template, TertianChordTemplate):
                raise Exception('Secondary chord requires TertianChordTemplate for this operation.')
            new_scale_degree = ((orig_principal_chord_template.scale_degree - 1) + self.step_increment) % 7 + 1
            new_principal_chord_template = TertianChordTemplate(orig_principal_chord_template.diatonic_basis,
                                                                new_scale_degree,
                                                                orig_principal_chord_template.chord_type,
                                                                orig_principal_chord_template.tension_intervals,
                                                                orig_principal_chord_template.inversion,
                                                                orig_principal_chord_template.inversion_interval)

            secondary_chord_template = SecondaryChordTemplate(new_principal_chord_template,
                                                              secondary_chord.chord_template.secondary_scale_degree,
                                                              secondary_chord.chord_template.secondary_modality)
            new_secondary_chord = SecondaryChord(secondary_chord_template, base_tonality)
            return new_secondary_chord
        else:
            orig_template = secondary_chord.chord_template
            new_degree = ((orig_template.secondary_scale_degree - 1) + self.step_increment) % 7 + 1
            secondary_chord_template = SecondaryChordTemplate(orig_template.principal_chord_template,
                                                              new_degree,
                                                              orig_template.secondary_modality)
            new_secondary_chord = SecondaryChord(secondary_chord_template, base_tonality)
            return new_secondary_chord


class PitchRemapFunction(object):

    def __init__(self, tonality, increment, aux_tonality=None):
        self.__tonality = tonality
        self.__increment = increment
        self.__aux_tonality = aux_tonality

        if tonality.cardinality != 7:
            raise Exception('Expect tonalities with cardinality 7 only.')

        self.__tone_map = dict()
        if aux_tonality is None:
            annotation = self.tonality.annotation
            for index in range(0, self.tonality.cardinality):
                dt = annotation[index]
                mapped_tone = self.tonality.annotation[(index + self.increment) % self.tonality.cardinality]
                if dt.augmentation_offset != 0:
                    mapped_tone = DiatonicTone.alter_tone_by_augmentation(mapped_tone, -dt.augmentation_offset)
                self.tone_map[dt.diatonic_letter] = mapped_tone
        else:
            annotation = self.tonality.annotation           # target scale
            aux_annotation = self.aux_tonality.annotation   # source scale
            for index in range(0, self.aux_tonality.cardinality):
                dt = aux_annotation[index]
                mapped_tone = annotation[index]
                if dt.augmentation_offset != 0:
                    mapped_tone = DiatonicTone.alter_tone_by_augmentation(mapped_tone, -dt.augmentation_offset)
                self.tone_map[dt.diatonic_letter] = mapped_tone

    @property
    def tonality(self):
        return self.__tonality

    @property
    def increment(self):
        return self.__increment

    @property
    def tone_map(self):
        return self.__tone_map

    @property
    def aux_tonality(self):
        return self.__aux_tonality

    @staticmethod
    def _sign(x):
        return 1 if x > 0 else -1

    def tonal_function(self, tone):
        result_tone = self.tone_map[tone.diatonic_letter]
        alteration = tone.augmentation_offset
        result_tone = DiatonicTone.alter_tone_by_augmentation(result_tone, alteration)
        return result_tone

    def __getitem__(self, pitch):
        if pitch is None:
            return None

        result_tone = self.tonal_function(pitch.diatonic_tone)

        crosses = DiatonicPitch.crosses_c(pitch.diatonic_tone, result_tone,
                                          True if self._sign(self.increment) >= 0 else False)

        result_register = pitch.octave + self._sign(self.increment) * ((abs(self.increment) // 7) +
                                                                       (1 if crosses else 0))

        return DiatonicPitch(result_register, result_tone)
