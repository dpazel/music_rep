"""

File: melodic_search.py

Purpose: Class implementation for searching for a melody (with harmonic annotation) over a harmonically annotated
         Line.

"""
from search.melodicsearch.global_search_options import GlobalSearchOptions
from search.melodicsearch.melodic_search_analysis import MelodicSearchAnalysis
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.line import Line
from timemodel.position import Position
from tonalmodel.interval import Interval
from search.melodicsearch.melodic_search_analysis import NotePairInformation


class MelodicSearch(object):
    """
    Search for a melodic pattern - given as a pattern line + its harmonic track, over a given (target) line with its
    harmonic track.
    """

    def __init__(self, pattern_line, pattern_hct):
        """
        Constructor.
        :param pattern_line:
        :param pattern_hct:
        """
        self.__pattern_line = pattern_line
        self.__pattern_hct = pattern_hct

        self.__analysis = MelodicSearchAnalysis(self.pattern_line, self.pattern_hct)

    @staticmethod
    def create(pattern_string):
        """
        Constructor for MelodicSearch using a text string representation for the pattern.
        :param pattern_string:
        :return:
        """
        line, hct = LineGrammarExecutor().parse(pattern_string)
        return MelodicSearch(line, hct)

    @property
    def pattern_line(self):
        return self.__pattern_line

    @property
    def pattern_hct(self):
        return self.__pattern_hct

    @property
    def analysis(self):
        return self.__analysis

    def search(self, target_line, target_hct, search_options=GlobalSearchOptions()):
        """
        Search a target_line/target_hct for matches to the pattern, ala GlobalSearchOptions.
        :param target_line:
        :param target_hct:
        :param search_options:
        :return: A list of starting positions that match pattern.
        """

        target_hc_count = 0

        position_answers = list()

        while True:
            hc_start = self.search_hct_incrementally(target_hct, target_hc_count, search_options)
            if hc_start is None:
                break
            search_answers = self.search_notes(target_line, target_hct, hc_start[1], search_options)
            target_hc_count = target_hc_count + 1 if search_answers is None or len(search_answers) == 0 \
                else hc_start[1] + 1
            if search_answers is not None and len(search_answers) != 0:
                position_answers.extend(search_answers)

        return position_answers

    def search_notes(self, target_line, target_hct, target_hc_index, search_options):
        if len(self.pattern_hct) == 1:
            return self.search_single_hc(target_line, target_hct.hc_list()[target_hc_index], search_options)
        else:
            return self.search_multi_hc(target_line, target_hct, target_hc_index, search_options)

    def search_single_hc(self, target_line, target_hc, search_options):
        answers = list()
        pattern_annotation = self.analysis.note_annotation
        note_pair_annotation = self.analysis.note_pair_annotation
        target_notes = MelodicSearch.get_all_contained_notes(target_line, target_hc.position, target_hc.duration)

        # TODO: The case wherein the pattern has no notes is an edge case not being dealt with right now.
        if len(pattern_annotation) == 0:
            return answers

        if len(target_notes) == 0 or len(target_notes) < len(pattern_annotation):
            return answers

        # Search over all notes in contained hc, and see if a match occurs.
        lead_pattern_annotation = pattern_annotation[0]
        lead_rest_space = lead_pattern_annotation.note.get_absolute_position().position
        i = 0
        while i < len(target_notes):
            if i + len(pattern_annotation) > len(target_notes):
                break
            first_note = target_notes[i]
            if not MelodicSearch.notes_compare(lead_pattern_annotation, first_note, target_hc, search_options):
                i = i + 1
                continue
            # See if the rest space before pattern is within hc bounds:
            target_lead_rest = first_note.get_absolute_position() - \
                (target_hc.position if i == 0 else target_notes[i-1].get_absolute_position())
            if lead_rest_space > target_lead_rest.duration:
                i = i + 1
                continue

            last_target_note = first_note
            last_pattern_annotation = lead_pattern_annotation
            fail = False
            for j in range(1, len(pattern_annotation)):
                pattern_info = pattern_annotation[j]
                target_note = target_notes[i + j]
                pair_annotation = note_pair_annotation[j - 1]
                if not MelodicSearch.notes_compare(pattern_info, target_note, target_hc, search_options):
                    fail = True
                    break
                if target_note.get_absolute_position() - last_target_note.get_absolute_position() != \
                        pattern_info.note.get_absolute_position() - \
                        last_pattern_annotation.note.get_absolute_position():
                    fail = True
                    break
                if not MelodicSearch.note_pair_check(pair_annotation, last_target_note, target_note):
                    fail = True
                    break
                last_pattern_annotation = pattern_info
                last_target_note = target_note

            if fail:
                i = i + 1
                continue

            start_position = first_note.get_absolute_position() - lead_rest_space
            if search_options.structural_match:
                if not self.structural_match(target_line, start_position):
                    i = i + 1
                    continue
            answers.append(start_position)
            i = i + len(pattern_annotation)

        return answers

    def search_multi_hc(self, target_line, target_hct, target_hc_index, search_options):
        answers = list()
        pattern_note_annotation = self.analysis.note_annotation
        pattern_note_pair_annotation = self.analysis.note_pair_annotation

        first_target_hc = target_hct.hc_list()[target_hc_index]
        target_start_position = Position(first_target_hc.position + first_target_hc.duration -
                                         self.pattern_hct.hc_list()[0].duration)
        target_notes = MelodicSearch.get_all_contained_notes(target_line, target_start_position,
                                                             self.pattern_line.duration)

        # TODO: The case wherein the pattern has no notes is an edge case not being dealt with right now.
        if len(pattern_note_annotation) == 0:
            return answers

        if len(target_notes) == 0 or len(target_notes) < len(pattern_note_annotation):
            return answers

        lead_pattern_note_annotation = pattern_note_annotation[0]
        lead_pattern_rest_space = lead_pattern_note_annotation.note.get_absolute_position().position
        i = 0
        while i <= len(target_notes) - len(pattern_note_annotation):
            first_target_note = target_notes[i]
            target_hc = target_hct[first_target_note.get_absolute_position()]
            if not MelodicSearch.notes_compare(lead_pattern_note_annotation, first_target_note, target_hc,
                                               search_options):
                i = i + 1
                continue
            # See if the rest space before pattern is within hc bounds:
            target_lead_rest = first_target_note.get_absolute_position() - target_start_position
            if lead_pattern_rest_space != target_lead_rest.duration:
                i = i + 1
                continue

            last_target_note = first_target_note
            last_pattern_annotation = lead_pattern_note_annotation
            fail = False
            for j in range(1, len(pattern_note_annotation)):
                pattern_info = pattern_note_annotation[j]
                target_note = target_notes[i + j]
                pair_annotation = pattern_note_pair_annotation[j - 1]
                target_hc = target_hct[target_note.get_absolute_position()]
                if not MelodicSearch.notes_compare(pattern_info, target_note, target_hc, search_options):
                    fail = True
                    break
                if target_note.get_absolute_position() - last_target_note.get_absolute_position() != \
                        pattern_info.note.get_absolute_position() - \
                        last_pattern_annotation.note.get_absolute_position():
                    fail = True
                    break
                if not MelodicSearch.note_pair_check(pair_annotation, last_target_note, target_note):
                    fail = True
                    break
                last_pattern_annotation = pattern_info
                last_target_note = target_note

            if fail:
                i = i + 1
                continue

            start_position = first_target_note.get_absolute_position() - target_lead_rest
            if search_options.structural_match:
                if not self.structural_match(target_line, start_position):
                    i = i + 1
                    continue

            answers.append(start_position)
            i = i + len(pattern_note_annotation)

        return answers

    def search_hct_incrementally(self, target_hct, target_hc_start_index, search_options):
        """
        Search across a target hct incrementally, using a target hc index as the incremental starting point.

        :param target_hct:
        :param target_hc_start_index:
        :param search_options:
        :return: pair (target hc that is starting point, index of next starting point in target hct)
        """
        pattern_hct_analysis = self.analysis.hct_annotation
        target_hc_list = target_hct.hc_list()

        if len(self.pattern_hct) == 1:
            pattern_hc_analysis = pattern_hct_analysis[0]
            for i in range(target_hc_start_index, len(target_hc_list)):
                hc = target_hc_list[i]
                if pattern_hc_analysis.span <= hc.duration:
                    if MelodicSearch.hc_meets_options(pattern_hc_analysis, hc, search_options):
                        return hc, i
        else:
            first_p_hc_info = pattern_hct_analysis[0]
            last_p_hc_info = pattern_hct_analysis[len(pattern_hct_analysis) - 1]
            pattern_mid_range = range(1, len(pattern_hct_analysis) - 1)

            i = 0
            while i < (len(target_hct) - target_hc_start_index) - len(self.pattern_hct) + 1:
                progress_ct = i + target_hc_start_index
                first_t_hc = target_hc_list[progress_ct]
                if first_p_hc_info.hc.duration > first_t_hc.duration or \
                        not MelodicSearch.hc_meets_options(first_p_hc_info, first_t_hc, search_options):
                    i = i + 1
                    continue

                progress_ct = progress_ct + 1
                fail = False
                for j in pattern_mid_range:
                    if target_hc_list[progress_ct].duration != pattern_hct_analysis[j].span or \
                            not MelodicSearch.hc_meets_options(pattern_hct_analysis[j], target_hc_list[progress_ct],
                                                               search_options):
                        fail = True
                        break
                    progress_ct = progress_ct + 1
                if fail:
                    i = i + 1
                    continue
                if last_p_hc_info.hc.duration > target_hc_list[progress_ct].duration or \
                        not MelodicSearch.hc_meets_options(last_p_hc_info, target_hc_list[progress_ct], search_options):
                    i = i + 1
                    continue
                return target_hc_list[i + target_hc_start_index], i + target_hc_start_index

        return None

    def search_hct(self, target_hct, search_options):
        target_hc_count = 0

        answers = list()

        while True:
            hc_start = self.search_hct_incrementally(target_hct, target_hc_count, search_options)
            if hc_start is None:
                break
            answers.append(hc_start)
            target_hc_count = hc_start[1] + 1

        return answers

    @staticmethod
    def hc_meets_options(p_hc_information, t_hc, search_options):
        if search_options.hct_match_tonality_key_tone:
            if p_hc_information.hc.tonality.diatonic_tone != t_hc.tonality.diatonic_tone:
                return False
        if search_options.hct_match_tonality_modality:
            if p_hc_information.hc.tonality.modality_type != t_hc.tonality.modality_type:
                return False

        if search_options.hct_match_relative_chord:
            target_relative_chord_degree = MelodicSearch.compute_chord_degree(t_hc)
            if p_hc_information.relative_chord_degree != target_relative_chord_degree:
                return False

        return True

    @staticmethod
    def compute_chord_degree(hc):
        if hc.chord.chord_template.diatonic_basis is None:
            return hc.chord.chord_template.scale_degree
        else:
            interval = Interval.calculate_tone_interval(hc.tonality.diatonic_tone,
                                                        hc.chord.chord_template.diatonic_basis)
            return interval.diatonic_distance + 1

    @staticmethod
    def get_all_contained_notes(line, start_position, duration):
        """
        Get all notes within a time interval. The first note within bounds which does not fit in the bounds,
        stops the process. Intentional, as otherwise we get non-continuous result.
        :param line:
        :param start_position:
        :param duration:
        :return:
        """
        end_position = start_position + duration
        notes = line.get_all_notes()
        answer = list()
        for note in notes:
            if end_position >= note.get_absolute_position() >= start_position:
                if note.get_absolute_position() + note.duration <= end_position:
                    answer.append(note)
                else:
                    break
        return answer

    @staticmethod
    def compute_scale_degree(pitch, hc):
        annotation = hc.tonality.annotation
        if pitch.diatonic_tone in annotation:
            return annotation.index(pitch.diatonic_tone)
        return None

    @staticmethod
    def note_pair_check(pair_information, prior_note, current_note):
        if pair_information.relationship == NotePairInformation.Relationship.LT:
            return prior_note.diatonic_pitch < current_note.diatonic_pitch
        elif pair_information.relationship == NotePairInformation.Relationship.GT:
            return prior_note.diatonic_pitch > current_note.diatonic_pitch
        return prior_note.diatonic_pitch == current_note.diatonic_pitch

    @staticmethod
    def compute_chord_interval(hc, note):
        tones = hc.chord.tones
        for tone in tones:
            if tone[0] == note.diatonic_pitch.diatonic_tone:
                return tone[1]
        return None

    @staticmethod
    def notes_compare(pattern_annotation, note, hc, search_options):
        pattern_note = pattern_annotation.note
        if pattern_note.duration != note.duration:
            return False
        if pattern_note.diatonic_pitch is None and note.diatonic_pitch is None:
            return True
        if (pattern_note.diatonic_pitch is None and note.diatonic_pitch is not None) or \
                (pattern_note.diatonic_pitch is not None and note.diatonic_pitch is None):
            return False
        target_pitch_scalar_degree = MelodicSearch.compute_scale_degree(note.diatonic_pitch, hc)
        target_chord_interval = MelodicSearch.compute_chord_interval(hc, note)

        if search_options.note_match_chordal:
            if pattern_annotation.is_chordal:
                if target_chord_interval is None:
                    return False
                if search_options.note_match_chordal_precision:
                    return pattern_annotation.chord_interval.diatonic_distance == \
                           target_chord_interval.diatonic_distance
                return True

        if pattern_annotation.is_scalar:
            if target_pitch_scalar_degree is not None:
                if search_options.note_match_scalar_precision:
                    return pattern_annotation.scale_degree == target_pitch_scalar_degree
                return True
            return False

        # Pattern note is non-scalar
        if target_pitch_scalar_degree is not None:  # Target is scalar
            return search_options.note_match_non_scalar_to_scalar
        # Target pitch is non-scalar
        if not search_options.note_match_non_scalar_precision:
            return True

        target_note_interval = \
            Interval.calculate_tone_interval(hc.tonality.root_tone, note.diatonic_pitch.diatonic_tone)
        if target_note_interval.diatonic_distance != pattern_annotation.root_based_interval.diatonic_distance:
            return False
        return True

    def structural_match(self, target_line, target_start_position):
        """
        Check if the pattern and target (@target_start_position) matches on all beam and tuplet sub-structures.
        Line structures are not checked.
        :param target_line:
        :param target_start_position:
        :return:
        """
        target_notes = MelodicSearch.get_all_contained_notes(target_line, target_start_position,
                                                             self.pattern_line.duration)
        pattern_notes = self.pattern_line.get_all_notes()

        if len(target_notes) != len(pattern_notes):
            return False

        pattern_to_target_dict = dict()
        for pattern_note, target_note in zip(pattern_notes, target_notes):
            if not MelodicSearch.note_structural_check(pattern_note, target_note, pattern_to_target_dict):
                return False

        return True

    @staticmethod
    def note_structural_check(pattern_note, target_note, pattern_to_target_dict):
        pattern_note_parent = pattern_note.parent
        target_note_parent = target_note.parent
        while True:
            if pattern_note_parent is None and target_note_parent is None:
                return True
            if pattern_note_parent is None:
                return isinstance(target_note_parent, Line)
            if target_note_parent is None:
                return isinstance(pattern_note_parent, Line)
            if type(pattern_note_parent) != type(target_note_parent):
                return False
            if isinstance(pattern_note_parent, Line):
                return True
            if pattern_note_parent in pattern_to_target_dict:
                if target_note_parent != pattern_to_target_dict[pattern_note_parent]:
                    return False
            else:
                pattern_to_target_dict[pattern_note_parent] = target_note_parent
            pattern_note_parent = pattern_note_parent.parent
            target_note_parent = target_note_parent.parent
