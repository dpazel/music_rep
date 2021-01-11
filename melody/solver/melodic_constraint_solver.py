"""

File: melodic_constraint_solver.py

Purpose: Combines beat and pitch constraint solver in the context of a lite score or constituents thereof. Provides
         solutions to meet all beat and pitch constraints.

"""
from melody.constraints.contextual_note import ContextualNote
from melody.constraints.on_beat_constraint import OnBeatConstraint
from melody.constraints.policy_context import PolicyContext
from melody.solver.beat_constraint_solver import BeatConstraintSolver
from melody.solver.msc_results import MCSResults
from melody.solver.pitch_constraint_solver import PitchConstraintSolver

from collections import OrderedDict

from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch


class MelodicConstraintSolver(object):

    def __init__(self, line, tempo_event_sequence, ts_event_sequence, hct, pitch_range, constraints):
        """
        Constructor.
        :param line:
        :param tempo_event_sequence:
        :param ts_event_sequence:
        :param hct:
        :param pitch_range:
        :param constraints:
        """
        self.__line = line
        self.__tempo_event_sequence = tempo_event_sequence
        self.__ts_event_sequence = ts_event_sequence
        self.__constraints = constraints
        self.__hct = hct
        self.__pitch_range = pitch_range

        self.__on_beat_constraints, self.__pitch_constraints = self._separate_constraints()

    @staticmethod
    def create(lite_score, constraints):
        """
        Constructor using LiteScore
        :param lite_score: LiteScore
        :param constraints:
        :return:
        """
        return MelodicConstraintSolver(lite_score.line, lite_score.tempo_sequence, lite_score.time_signature_sequence,
                                       lite_score.hct, lite_score.instrument.sounding_pitch_range(), constraints)

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
    def hct(self):
        return self.__hct

    @property
    def constraints(self):
        return self.__constraints

    @property
    def on_beat_constraints(self):
        return self.__on_beat_constraints

    @property
    def pitch_constraints(self):
        return self.__pitch_constraints

    @property
    def pitch_range(self):
        return self.__pitch_range

    def solve(self, partial_pitch_results=None, num_solutions=-1):
        if partial_pitch_results is not None:
            if not isinstance(partial_pitch_results, dict):
                raise Exception('partial_pitch_results argument must be a dict.')

        beat_solver = BeatConstraintSolver(self.line, self.tempo_event_sequence,
                                           self.ts_event_sequence, self.hct, self.on_beat_constraints)
        beat_results = beat_solver.solve()   # list of PositionDeltaInfo's

        pitch_solver = PitchConstraintSolver(self.pitch_constraints)
        p_map_dict = self._build_p_map_dict(partial_pitch_results)
        full_results, pitch_results = pitch_solver.solve(p_map_dict, num_solutions)

        return MCSResults(self.line, self.tempo_event_sequence, self.ts_event_sequence, self.hct,
                          beat_results,
                          full_results)

    def _build_p_map_dict(self, partial_pitch_results=None):
        actors = set()
        for p in self.pitch_constraints:
            actors = actors.union(p.actors)

        d = OrderedDict()
        for note in actors:
            hc = self.hct[note.get_absolute_position().position]
            if hc is None:
                raise Exception('Cannot locate harmonic context for note \'{0}\''.format(note))
            contextual = ContextualNote(PolicyContext(hc, self.pitch_range))
            d[note] = contextual

        if partial_pitch_results is not None:
            for k, v in partial_pitch_results.items():
                if not isinstance(k, Note):
                    raise Exception('key of partial_pitch_results must be a Note.')
                if not isinstance(v, DiatonicPitch):
                    raise Exception('value of partial_pitch_results must be a DiatonicPitch.')
                if k not in d:
                    raise Exception('Note \'{0}\' of partial result is not a constraint actor.'.format(k))
                d[k].note = Note(v, k.base_duration, k.num_dots)

        return d

    def _separate_constraints(self):
        on_beat = []
        pitch = []
        for constraint in self.constraints:
            if isinstance(constraint, OnBeatConstraint):
                on_beat.append(constraint)
            else:
                pitch.append(constraint)
        return on_beat, pitch
