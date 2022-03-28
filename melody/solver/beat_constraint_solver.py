"""

File: beat_constraint_solver.py

Purpose: Class whose purpose is to reposition notes on a line to mean a set of OnBeat Constraints.

"""
from melody.constraints.on_beat_constraint import OnBeatConstraint
from structure.line import Line

from melody.solver.position_delta_info import PositionDeltaInfo


class BeatConstraintSolver(object):
    """
    Class whose algorithm moves notes on a line so that a set of OnBeat constraints are met. The algorithm provides a
    set of PositionDeltaInfo(s) which can be applied to the line to produce a remediated line satisfying all the
    OnBeat constraints.
    """

    def __init__(self, line, tempo_event_sequence, ts_event_sequence, hct, on_beat_constraints):
        """
        Constructor
        :param line: Line
        :param tempo_event_sequence: TempoEventSequence
        :param ts_event_sequence: EventSequence
        :param hct: HarmonicContextTrack
        :param on_beat_constraints: All OnBeat constraints pertinent to line that need to be satisifed.
        """
        self.__line = line
        self.__tempo_event_sequence = tempo_event_sequence
        self.__ts_event_sequence = ts_event_sequence
        self.__on_beat_constraints = on_beat_constraints
        self.__hct = hct

        self.__on_beat_notes = self._compute_on_beat_notes()
        self.coverage_map, self.reverse_coverage_map, self.coverage_node_list = self._compute_coverage_structures()
        self.node_constraint_map = {constraint.actor: constraint for constraint in on_beat_constraints}

        self.__results = None

    @staticmethod
    def create(lite_score, on_beat_constraints):
        """
        Constructor using LiteScore
        :param lite_score: LiteScore
        :param on_beat_constraints:
        :return:
        """
        return BeatConstraintSolver(lite_score.line, lite_score.tempo_sequence, lite_score.time_signature_sequence,
                                    lite_score.hct, on_beat_constraints)

    @property
    def line(self):
        return self.__line

    @property
    def tempo_event_sequence(self):
        return self.__tempo_event_sequence

    @property
    def ts_event_sequence(self):
        return self.__ts_event_sequence

    @property
    def on_beat_constraints(self):
        return self.__on_beat_constraints

    @property
    def on_beat_notes(self):
        return self.__on_beat_notes

    @property
    def results(self):
        return self.__results

    @property
    def hct(self):
        return self.__hct

    def solve(self):
        """
        Solve for the on-beat constraints by modifying the time-line.
        :return: A set of PDI's that solve the constraints.
                 Empty if initially solves the constraints.
                 None if no solution is found.
        """
        if self.results is None:
            self.__results = self._compute_coverage()
        return self.results

    def _compute_coverage(self):
        return self._visit(0, PositionDeltaInfo(self.coverage_node_list, self.tempo_event_sequence,
                                                self.ts_event_sequence,
                                                self.hct,
                                                self.line))

    def _visit(self, coverage_list_index, pdi):
        results = list()
        for i in range(coverage_list_index, len(self.coverage_node_list)):
            cover = self.coverage_node_list[i]
            # find the first note in cover that violates its beat constraint.
            cover_note = None
            constraint = None
            for n in self.reverse_coverage_map[cover]:
                constraint = self.node_constraint_map[n]
                if constraint.verify(pdi):
                    continue
                cover_note = n
                break
            if cover_note is None:   # Notes in cover satisfy on beat constraints.
                continue

            deltas = constraint.values(pdi, cover_note)
            successful_delta = False
            for delta in deltas:
                new_pdi = pdi.clone()
                new_pdi.alter_at(cover, delta)
                # test of all notes in cover are solved
                bad_constraint = None
                for n in self.reverse_coverage_map[cover]:
                    constraint = self.node_constraint_map[n]
                    if constraint.verify(new_pdi):
                        continue
                    bad_constraint = constraint
                if bad_constraint is not None:
                    continue
                successful_delta = True
                if i + 1 < len(self.coverage_node_list):
                    new_results = self._visit(i + 1, new_pdi)
                    if new_results is not None:
                        results = results + new_results
                else:
                    results.append(new_pdi)
            if not successful_delta:
                return None
            break

        return results

    def _compute_on_beat_notes(self):
        on_beat_notes = list()
        notes = self.line.get_all_notes()
        for constraint in self.on_beat_constraints:
            if not isinstance(constraint, OnBeatConstraint):
                raise Exception('Expecting OnBeatConstraint, have {0}.'.format(type(constraint)))
            n = constraint.actor
            if n not in notes:
                raise Exception('Note \'{0}\' from constraint not in line.'.format(n))
            on_beat_notes.append(n)
        return sorted(on_beat_notes, key=lambda note: note.get_absolute_position().position)  # sort by position lo->hi

    def _compute_coverage_structures(self):
        coverage_map = dict()
        reverse_coverage_map = dict()
        coverage_node_list = list()
        for n in self.__on_beat_notes:
            c = n
            while not isinstance(c.parent, Line):
                c = c.parent
            coverage_map[n] = c

            if c not in reverse_coverage_map:
                reverse_coverage_map[c] = list()
                coverage_node_list.append(c)
            reverse_coverage_map[c].append(n)

        return coverage_map, reverse_coverage_map, coverage_node_list
'''
    def apply(self, pdi, line_copy=True):
        """
        Apply a position delta info to a the pdi's line.
        :param pdi: PositionDeltaInfo
        :param line_copy: True - make a copy of the line; False - apply directly to line.
        :return:
        """
        return pdi.apply(line_copy)
        '''
