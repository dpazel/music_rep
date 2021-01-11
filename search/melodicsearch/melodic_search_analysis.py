from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor

from enum import Enum

from tonalmodel.interval import Interval


class MelodicSearchAnalysis(object):

    def __init__(self, pattern_line, pattern_hct):
        self.__pattern_line = pattern_line
        self.__pattern_hct = pattern_hct

        self.__note_annotation = self.prepare_note_search_parameters()
        self.__note_pair_annotation = self.prepare_note_pair_search_parameters()
        self.__hct_annotation = self.prepare_hct_search_parameters()

    @staticmethod
    def create(pattern_string):
        line, hct = LineGrammarExecutor().parse(pattern_string)
        return MelodicSearchAnalysis(line, hct)

    @property
    def pattern_line(self):
        return self.__pattern_line

    @property
    def pattern_hct(self):
        return self.__pattern_hct

    @property
    def note_annotation(self):
        return self.__note_annotation

    @property
    def note_pair_annotation(self):
        return self.__note_pair_annotation

    @property
    def hct_annotation(self):
        return self.__hct_annotation

    def prepare_note_search_parameters(self):
        annotation_list = list()
        for note in self.pattern_line.get_all_notes():
            hc = self.pattern_hct[note.get_absolute_position()]
            annotation_list.append(NoteInformation(note, hc))
        return annotation_list

    def prepare_note_pair_search_parameters(self):
        pair_annotation_list = list()
        note_list = self.pattern_line.get_all_notes()
        for i in range(0, len(note_list) - 1):
            first = note_list[i]
            if first.diatonic_pitch is None:
                continue
            second = None
            for j in range(i + 1, len(note_list)):
                second = note_list[j]
                if second.diatonic_pitch is not None:
                    break
            if second.diatonic_pitch is None:
                continue
            pair_annotation_list.append(NotePairInformation(first, second))
        return pair_annotation_list

    def prepare_hct_search_parameters(self):
        hct_annotation = list()
        hc_list = self.pattern_hct.hc_list()
        for i in range(0, len(hc_list)):
            hc = hc_list[i]
            hct_annotation.append(HCInformation(hc))

        return hct_annotation


class NoteInformation(object):

    def __init__(self, note, hc):
        self.__note = note
        self.__hc = hc

        self.__scale_degree = self.compute_scale_degree()
        self.__chord_interval = self.compute_chord_interval()
        self.__root_based_interval = self.compute_root_based_interval()

        self.__duration = note.duration

    @property
    def note(self):
        return self.__note

    @property
    def hc(self):
        return self.__hc

    @property
    def scale_degree(self):
        return self.__scale_degree

    @property
    def chord_interval(self):
        return self.__chord_interval

    @property
    def is_scalar(self):
        return self.scale_degree is not None

    @property
    def is_chordal(self):
        return self.chord_interval is not None

    @property
    def duration(self):
        return self.__duration

    @property
    def root_based_interval(self):
        return self.__root_based_interval

    def compute_scale_degree(self):
        annotation = self.hc.tonality.annotation
        if self.note.diatonic_pitch is None:   # Rest
            return None
        if self.note.diatonic_pitch.diatonic_tone in annotation:
            return annotation.index(self.note.diatonic_pitch.diatonic_tone)
        return None

    def compute_root_based_interval(self):
        if self.note.diatonic_pitch is None:
            return None
        return Interval.calculate_tone_interval(self.hc.tonality.root_tone, self.note.diatonic_pitch.diatonic_tone)

    def compute_chord_interval(self):
        tones = self.hc.chord.tones
        if self.note.diatonic_pitch is None:
            return None
        for tone in tones:
            if tone[0] == self.note.diatonic_pitch.diatonic_tone:
                return tone[1]
        return None

    def __str__(self):
        return '{0} hc={1} scale_degree={2} interval={3} is_scalar={4} is_chordal={5} duration={6}'.\
            format(self.note, self. hc, self.scale_degree, self.chord_interval, self.is_scalar,
                   self.is_chordal, self.duration)


class NotePairInformation(object):

    class Relationship(Enum):
        LT = -1
        EQ = 0
        GT = 1

    def __init__(self, first_note, second_note):
        self.__first_note = first_note
        self.__second_note = second_note
        self.__time_difference = self.second_note.get_absolute_position() - self.first_note.get_absolute_position()

        self.__forward_interval = Interval.create_interval(self.first_note.diatonic_pitch,
                                                           self.second_note.diatonic_pitch)

        cd = self.forward_interval.chromatic_distance
        self.__relationship = NotePairInformation.Relationship.GT if cd < 0 else NotePairInformation.Relationship.LT \
            if cd > 0 else NotePairInformation.Relationship.EQ

    @property
    def first_note(self):
        return self.__first_note

    @property
    def second_note(self):
        return self.__second_note

    @property
    def time_difference(self):
        return self.__time_difference

    @property
    def forward_interval(self):
        return self.__forward_interval

    @property
    def relationship(self):
        return self.__relationship

    @staticmethod
    def rel_pair_symbol(relationship):
        return '>' if relationship == NotePairInformation.Relationship.GT else \
            '<' if relationship == NotePairInformation.Relationship.LT else '=='

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_note, NotePairInformation.rel_pair_symbol(self.relationship),
                                    self.second_note)


class HCInformation(object):

    def __init__(self, hc):
        self.__hc = hc
        self.__span = hc.duration

        if self.hc.chord.chord_template.diatonic_basis is None:
            self.__relative_chord_degree = self.hc.chord.chord_template.scale_degree
        else:
            interval = Interval.calculate_tone_interval(self.hc.tonality.diatonic_tone,
                                                        self.hc.chord.chord_template.diatonic_basis)
            self.__relative_chord_degree = interval.diatonic_distance + 1

    @property
    def hc(self):
        return self.__hc

    @property
    def span(self):
        return self.__span

    @property
    def relative_chord_degree(self):
        return self.__relative_chord_degree

    def __str__(self):
        return '{0} span={1} chord_degree={2}'.format(self.hc, self.span, self.relative_chord_degree)
