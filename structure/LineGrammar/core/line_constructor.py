"""
File: line_constructor.py

Purpose: Helper classes for LineGrammar.g4. Used as the parser parses to assemble information into a line
         and harmonic context track.

"""
from fractions import Fraction

from harmoniccontext.harmonic_context import HarmonicContext
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmonicmodel.chord_template import ChordTemplate
from structure.note import Note
from structure.line import Line
from structure.line import Tuplet
from structure.line import Beam
from timemodel.duration import Duration
from timemodel.position import Position
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality


class LineConstructor(object):
    """
    Line and HarmonicContextTrack constructor. Used by LineGrammar.g4 to assemble parts for each entity.
    """

    DURATION_MAP = {
        'W': Fraction(1),
        'H': Fraction(1, 2),
        'Q': Fraction(1, 4),
        'I': Fraction(1, 8),
        'S': Fraction(1, 16),
        'T': Fraction(1, 32),
        'X': Fraction(1, 64)
    }

    MODALITY_MAP = {
        'Major': ModalityType.Major,
        'Minor': ModalityType.MelodicMinor,
        'Natural': ModalityType.NaturalMinor,
        'Harmonic': ModalityType.HarmonicMinor,
        'Melodic': ModalityType.MelodicMinor
    }

    DEFAULT_BEAM_DURATION = Duration(1, 8)
    DEFAULT_LINE_DURATION = Duration(1, 4)
    DEFAULT_TONALITY = Tonality(ModalityType.Major, DiatonicToneCache.get_tone('C'))

    def __init__(self):
        """
        Constructor.
        """
        self.tie_list = list()
        self.__line = Line()
        self.current_level = Level(self.__line, LineConstructor.DEFAULT_LINE_DURATION)
        self.level_stack = list()
        self.current_tonality = LineConstructor.DEFAULT_TONALITY
        self.harmonic_tag_list = list()
        self.current_harmonic_tag = None

        # Set up a default harmonic tag. In cases where a tag is immediately specified, this is discarded
        self.construct_harmonic_tag(LineConstructor.DEFAULT_TONALITY,
                                    ChordTemplate.generic_chord_template_parse('ti'))

    @property
    def line(self):
        return self.__line

    @property
    def hct(self):
        return self.build_harmonic_context_track()

    def start_level(self, duration=None, dur_int=None):
        level = Level(Tuplet(duration, dur_int) if duration is not None else Beam(),
                      duration if duration is not None else LineConstructor.DEFAULT_BEAM_DURATION)
        self.current_level.collector.append(level.collector)
        self.level_stack.append(self.current_level)
        self.current_level = level

    def end_level(self):
        self.current_level = self.level_stack.pop()

    def construct_note(self, pitch, duration, dots, tied):
        dur = duration if duration is not None else self.current_level.default_duration
        note = Note(pitch, dur, dots)
        if tied:
            self.tie_list.append(note)
        if duration is not None:
            self.current_level.default_duration = duration
        return note

    @staticmethod
    def construct_tone_from_tone_letters(letters):
        return DiatonicToneCache.get_tone(letters)

    def construct_pitch(self, tone, partition):
        part = partition if partition is not None else self.current_level.default_register
        if partition is not None:
            self.current_level.default_register = partition
        return DiatonicPitch(part, tone)

    @staticmethod
    def construct_duration_by_shorthand(shorthand):
        shorthand = shorthand.upper()
        if shorthand not in LineConstructor.DURATION_MAP:
            raise Exception('\'{0}\' not a valid duration shorthand.'.format(shorthand))
        return Duration(LineConstructor.DURATION_MAP[shorthand])

    @staticmethod
    def construct_duration(numerator, denominator):
        return Duration(numerator, denominator)

    def construct_tonality(self, tone, modality_str):
        if modality_str not in LineConstructor.MODALITY_MAP:
            raise Exception('\'{0}\' not a valid modality type.'.format(modality_str))
        modality_type = LineConstructor.MODALITY_MAP[modality_str]
        return Tonality(modality_type, tone)

    def construct_chord_template(self, tone, chord_type_str):
        chord_template_str = 't' + (tone.diatonic_symbol + chord_type_str if tone is not None else chord_type_str)
        return ChordTemplate.generic_chord_template_parse(chord_template_str)

    def construct_harmonic_tag(self, tonality, chord_template):
        tonality = tonality if tonality is not None else self.current_tonality
        chord = chord_template.create_chord(tonality)

        self.current_harmonic_tag = HarmonicTag(tonality, chord)
        self.harmonic_tag_list.append(self.current_harmonic_tag)

        self.current_tonality = tonality

    def build_harmonic_context_track(self):
        # Prune superfluous harmonic tags.
        new_tag_list = [tag for tag in self.harmonic_tag_list if tag.first_note is not None]
        self.harmonic_tag_list = new_tag_list

        hct = HarmonicContextTrack()
        for i in range(0, len(self.harmonic_tag_list)):
            harmonic_tag = self.harmonic_tag_list[i]
            duration = (self.harmonic_tag_list[i + 1].first_note.get_absolute_position()
                        if i < len(self.harmonic_tag_list) - 1 else Position(self.__line.duration)) \
                        - self.harmonic_tag_list[i].first_note.get_absolute_position()
            harmonic_context = HarmonicContext(harmonic_tag.tonality, harmonic_tag.chord, duration,
                                               harmonic_tag.first_note.get_absolute_position())
            hct.append(harmonic_context)
        return hct

    def add_note(self, note):
        self.current_level.collector.append(note)
        if self.current_harmonic_tag:
            self.current_harmonic_tag.first_note = note

    def note_list(self):
        return self.current_level.collector

    def __str__(self):
        return str(self.current_level.collector)


class Level(object):
    """
    Represents any of Line, Beam, or Tuplet, which may involve nesting of levels within level.
    LineCollector tracks these different levels, adding notes to each as the parsing progresses.
    """
    DEFAULT_REGISTER = 4

    def __init__(self, collector, default_duration=None):
        """
        Constructor.
        :param collector: Any of Line, Tuplet, or Beam.
        :param default_duration: default note duration.
        """
        self.__collector = collector
        self.__default_duration = default_duration
        self.__default_register = Level.DEFAULT_REGISTER

    @property
    def collector(self):
        return self.__collector

    @property
    def default_duration(self):
        return self.__default_duration

    @default_duration.setter
    def default_duration(self, value):
        self.__default_duration = value

    @property
    def default_register(self):
        return self.__default_register

    @default_register.setter
    def default_register(self, value):
        self.__default_register = value


class HarmonicTag(object):
    """
    Collects tonality and chord information about each harmonic context.
    Position and duration are determined after the Line construction since note durations might change while
    as further notes are added, e.g. Tuplet. Thus HC durations and positions cannot be determined during construction.
    So, to anchor the HC, we track the first note added to each - which in the end can be used to determine
    duration and position for the hc.
    """

    def __init__(self, tonality, chord):
        self.__tonality = tonality
        self.__chord = chord

        self.__first_note = None

    @property
    def tonality(self):
        return self.__tonality

    @property
    def chord(self):
        return self.__chord

    @property
    def first_note(self):
        return self.__first_note

    @first_note.setter
    def first_note(self, first_note):
        if self.__first_note is None:
            self.__first_note = first_note

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.tonality, self.chord, self.first_note,
                                        self.first_note.get_absolute_position(), self.first_note.duration)
