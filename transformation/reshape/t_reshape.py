"""

File: t_reshape.py

Purpose: Transform to reshape a melody to a curve.

"""
from function.function_pitch_range import FunctionPitchRange
from melody.constraints.contextual_note import ContextualNote
from melody.constraints.fit_pitch_to_function_constraint import FitPitchToFunctionConstraint
from melody.constraints.fixed_pitch_constraint import FixedPitchConstraint
from melody.constraints.fixed_pitch_select_set_constraint import FixedPitchSelectSetConstraint
from melody.constraints.on_beat_constraint import OnBeatConstraint
from melody.constraints.policy_context import PolicyContext
from melody.solver.beat_constraint_solver import BeatConstraintSolver
from melody.solver.p_map import PMap
from melody.solver.pitch_constraint_solver import PitchConstraintSolver
from structure.lite_score import LiteScore
from tonalmodel.pitch_range import PitchRange
from transformation.functions.pitchfunctions.pitch_fit_function import PitchFitFunction
from transformation.transformation import Transformation

from collections import OrderedDict

'''
Notes on TRESHAPE:

The idea is to temporarily add an extra constraint to a melody that can be handled by the pitch constraint engine.
The new constraint is labeled non-essential, meaning that:
1) If there are essential constraints affecting a note - they must be met.  Then the non-essentials are tried. 
   We do not allow the non-essentials to negate the essential results. 
2) If there are no essential contraints, the non-essentials are tried, and if solved, we use those solutions.

Note: There may be a difference in key between the a non-essential constraint's harmonic context and that of the 
      pitch function. We defer to the key of the pitch function, except where a function result has an enharmonic
      equivalent in the hc's key - we use that. 
Note: If a pitch evaluation gives a pitch for a note on a strong beat, and that note is a 1/2 pitch off of some
      note in the harmonic context's chord, we flag a failure, i.e. we return an empty set.
'''


class TReshape(Transformation):
    """
    TReshape: Transform to reshape a melody to a user defined curve. The curve can be defined using
              FunctionPitchRange.
    """

    def __init__(self, score, pitch_function, time_range, melodic_form, optimize=True):
        """
        Constructor
        :param score: LiteScore
        :param pitch_function: FunctionPitchRange
        :param time_range: Range
        :param melodic_form: MelodicForm based on score's line.
        :param optimize: Attempt of add restrictive pitch constraints based on reshape function
        """
        self.__score = score
        self.__pitch_function = pitch_function
        self.__time_range = time_range
        self.__melodic_form = melodic_form
        self.__optimize = optimize

        self.pitch_fit_function = PitchFitFunction(self.pitch_function, self.score.tempo_sequence,
                                                   self.score.time_signature_sequence, self.score.hct)

        if not isinstance(self.pitch_function, FunctionPitchRange):
            raise Exception('Function must be subclass of FunctionPitchRange.')

        Transformation.__init__(self)

    @property
    def score(self):
        return self.__score

    @property
    def pitch_function(self):
        return self.__pitch_function

    @property
    def time_range(self):
        return self.__time_range

    @property
    def melodic_form(self):
        return self.__melodic_form

    @property
    def optimize(self):
        return self.__optimize

    def apply(self):
        """
        Apply the TReshape transformation.
        :return: A list of LiteScore's of valid application of the transformation.
        """
        constraints = self._get_melodic_form_constraints()

        on_beat_constraints = [constraint for constraint in constraints
                               if isinstance(constraint, OnBeatConstraint)]
        beat_score_results = self._build_on_beat_solution(on_beat_constraints) if len(on_beat_constraints) > 0 else None

        pitch_constraints = {constraint for constraint in constraints
                             if not isinstance(constraint, OnBeatConstraint)}

        if self.optimize:
            pitch_constraints = pitch_constraints.union(self._reshape_optimize(pitch_constraints, self.score))

        return self._build_pitch_solutions(beat_score_results, pitch_constraints)

    def _generate_reshape_constraints(self, line, tempo_sequence, time_signature_sequence, ignore_notes):
        constraints = list()

        for note in line.get_all_notes():
            if note not in ignore_notes:
                if self.time_range.is_inbounds(note.get_absolute_position().position):
                    constraint = FitPitchToFunctionConstraint(note,
                                                              self.pitch_function,
                                                              tempo_sequence,
                                                              time_signature_sequence)
                    constraints.append(constraint)
        return constraints

    def _generate_reshape_map(self, line, ignore_notes):
        """
        Map each non-ignore note in line, to its curve fit solutions
        :param line:
        :param ignore_notes: notes presumably satisfied by constraints
        :return:
        """
        note_to_pitch_map = dict()

        for note in line.get_all_notes():
            if note not in ignore_notes:
                if self.time_range.is_inbounds(note.get_absolute_position().position):
                    note_to_pitch_map[note] = self.pitch_fit_function(note.get_absolute_position())
        return note_to_pitch_map

    def _get_melodic_form_constraints(self):
        constraints = list()
        all_notes = self.score.line.get_all_notes()
        for constraint in self.melodic_form.constraints:
            invalid_constraint = False
            for actor in constraint.actors:
                if not self.time_range.is_inbounds(actor.get_absolute_position()) or actor not in all_notes:
                    invalid_constraint = True
                    break
            if not invalid_constraint:
                constraints.append(constraint)
        return constraints

    def _build_on_beat_solution(self, on_beat_constraints):
        """
        Solve the on-beat constraints
        :param on_beat_constraints:get_hc_by_position
        :return: Set of (PositionDeltaInfo, LiteScore)'s that are solutions to the on-beat constraints.
        """
        beat_solver = BeatConstraintSolver(self.score.line, self.score.tempo_sequence,
                                           self.score.time_signature_sequence, self.score.hct, on_beat_constraints)
        results = beat_solver.solve()  # list of PositionDeltaInfo's

        score_beat_results = []
        if results is not None:
            for result in results:
                new_line = result.apply(self.score.line)
                lite_score = LiteScore(new_line, result.hct, self.score.instrument, result.tempo_event_sequence,
                                       result.ts_event_sequence)
                score_beat_results.append((result, lite_score))

        return score_beat_results

    def _build_pitch_solutions(self, beat_score_results, pitch_constraints):
        """
        Build the final results using the beat results, then the pitch results, then the reshape constraints.
        :param beat_score_results: Set of (PositionDeltaInfo, LiteScore)'s
        :param pitch_constraints: Set of Constraints
        :return:
        """
        final_results = list()
        pitch_results = list()

        # Solve the pitch constraints using the beat constraint results.
        if beat_score_results is not None:
            for beat_result_pdi, beat_result_score in beat_score_results:
                revised_constraints = TReshape._regenerate_constraints(pitch_constraints,
                                                                       self.score.line, beat_result_score.line)
                pitch_solver = PitchConstraintSolver(revised_constraints)
                p_map_dict = PMap(self._build_p_map_dict(beat_result_pdi.hct, revised_constraints))
                pitch_solver_results, _ = pitch_solver.solve(p_map_dict)
                for pitch_pmap in pitch_solver_results:
                    line = pitch_pmap.apply(beat_result_score.line)
                    pitch_results.append((pitch_pmap, beat_result_score,
                                          LiteScore(line,
                                                    beat_result_pdi.hct,
                                                    self.score.instrument,
                                                    beat_result_pdi.tempo_event_sequence,
                                                    beat_result_pdi.ts_event_sequence)))

        else:
            pitch_solver = PitchConstraintSolver(pitch_constraints)
            p_map_dict = PMap(self._build_p_map_dict(self.score.hct, pitch_constraints))
            pitch_solver_results, _ = pitch_solver.solve(p_map_dict)
            for pitch_pmap in pitch_solver_results:
                line = pitch_pmap.apply(self.score.line)
                pitch_results.append((pitch_pmap, self.score, LiteScore(line, self.score.hct, self.score.instrument,
                                      self.score.tempo_sequence, self.score.time_signature_sequence)))

        # Solve the reshape constraints using the pitch constraint solutions.
        for pitch_result_pmap, beat_result_score, pitch_result_score in pitch_results:
            # pitch_result_pmap: self.score.line --> pitch_result_score.line
            q = {key: value for key, value in zip(beat_result_score.line.get_all_notes(),
                                                  pitch_result_score.line.get_all_notes())}

            # ignore_notes are notes that were satisfied by constraints.
            ignore_notes = {q[n] for n in pitch_result_pmap.keys()
                            if pitch_result_pmap[n].note is not None}

            # note_to_pitch_map maps each ignore-note in line to a curve fit pitch.
            note_to_pitch_map = self._generate_reshape_map(pitch_result_score.line, ignore_notes)

            # Map pitch result score notes to their resolved pitches
            master_map = dict()

            # mm: beat_result_score.line --> pitch_reslt_score.line (self.score or beat_result_score)
            # For pitch constraint notes, map them to their pitch constraint results.
            mm = {key: value for key, value in zip(beat_result_score.line.get_all_notes()
                                                   if beat_result_score else self.score.line.get_all_notes(),
                                                   pitch_result_score.line.get_all_notes())}
            # Put the constraint based notes into master
            for note in pitch_result_pmap.keys():
                # map notes in pitch_result_score to what beat_score_result would
                if pitch_result_pmap[note].note is None:
                    raise Exception('Note at {0} not solved for value in constraint.'.format(
                        note.get_absolute_position()))
                master_map[mm[note]] = pitch_result_pmap[note].note.diatonic_pitch

            # Map reshaped notes in pitch_result_score to their resolved notes into master
            for note in note_to_pitch_map.keys():
                if note not in master_map.keys():
                    master_map[note] = note_to_pitch_map[note]

            # Clone pitch_result_score, and build a map from pitch_result_score.line to the clone's notes (mmm)
            line_answer = pitch_result_score.line.clone()
            mmm = {key: value for key, value in zip(pitch_result_score.line.get_all_notes(),
                                                    line_answer.get_all_notes())}
            # A shallow form of apply (use mmm and master_map to reset the diatonic pitches on line_answer.
            for note in master_map.keys():
                if master_map[note] is not None:
                    mmm[note].diatonic_pitch = master_map[note]

            final_results.append(LiteScore(line_answer, pitch_result_score.hct,
                                           pitch_result_score.instrument,
                                           pitch_result_score.tempo_sequence,
                                           pitch_result_score.time_signature_sequence))

        return final_results

    def _build_p_map_dict(self, hct, pitch_constraints):
        actors = set()
        for p in pitch_constraints:
            actors = actors.union(p.actors)

        d = OrderedDict()
        for note in actors:
            hc = hct[note.get_absolute_position().position]
            if hc is None:
                raise Exception('Cannot locate harmonic context for note \'{0}\''.format(note))
            pitch_range = self.score.instrument.sounding_pitch_range() if self.score.instrument is not None \
                else PitchRange.create('A:0', 'C:8')
            contextual = ContextualNote(PolicyContext(hc, pitch_range))
            d[note] = contextual

        return d

    def _reshape_optimize(self, pitch_constraints, score):
        constraint_map = TReshape._build_v_constraint_map(pitch_constraints)
        new_constraints = set()
        for note in score.line.get_all_notes():
            time = note.get_absolute_position()
            if self.time_range.is_inbounds(time):
                if note in constraint_map:
                    new_constraints = new_constraints.union(self._optimize_note_domain(note,
                                                                                       constraint_map[note], score))

        return new_constraints

    def _optimize_note_domain(self, note, constraints, score):
        """
        For note, get all values it can take satisfying all its constraints.
        Then if there is only one, build a fixed pitch constraint for it.
        If there are more than two, use the curve fits values to make a fixed pitch to set.
        :param note:
        :param constraints:
        :param score:
        :return:
        """
        domain = set()
        first = True
        for constraint in constraints:
            pmap = PMap()
            for n in constraint.actors:
                hc = score.hct.get_hc_by_position(n.get_absolute_position())
                pmap[n] = ContextualNote(PolicyContext(hc,
                                                       score.instrument.sounding_pitch_range()
                                                       if score.instrument is not None else
                                                       PitchRange.create('A:0', 'C:8')))
            values = {n.diatonic_pitch for n in constraint.values(pmap, note)}
            if first:
                domain = values
                first = False
            else:
                domain = domain.intersection(values)

        if len(domain) == 0:
            return set()

        pitch_list = list(domain)
        if len(domain) > 2:
            # Find 2 pitches in domain that are closest to the curve fit
            valuation = self.pitch_function.eval_as_nearest_pitch(note.get_absolute_position().position)
            candidates = [(p, abs(p.chromatic_distance - valuation.chromatic_distance)) for p in domain]
            candidates = sorted(candidates, key=lambda candidate: candidate[1])
            pitch_list = [candidates[0][0], candidates[1][0]]

        if len(pitch_list) == 1:
            return {FixedPitchConstraint(note, pitch_list[0])}
        (first, second) = (pitch_list[0], pitch_list[1]) if pitch_list[0].chromatic_distance <= \
            pitch_list[1].chromatic_distance else \
            (pitch_list[1], pitch_list[0])

        return {FixedPitchSelectSetConstraint(note, [first, second])}

    @staticmethod
    def _build_v_constraint_map(constraints):
        """
        Map notes to constraints wherein they are the first actor.
        :param constraints:
        :return: map: note --> set of constraints having note as first actor.
        """
        constraint_map = dict()
        for p in constraints:
            v_note = p.actors[0]
            if v_note not in constraint_map:
                constraint_map[v_note] = []
            constraint_map[v_note].append(p)
        return constraint_map

    @staticmethod
    def _regenerate_constraints(pitch_constraints, old_line, new_line):
        conversion_map = {key: value for key, value in zip(old_line.get_all_notes(), new_line.get_all_notes())}
        constraints = []
        for c in pitch_constraints:
            new_actors = [conversion_map[v_note] for v_note in c.actors]
            constraints.append(c.clone(new_actors))
        return constraints

    # Deprecated to _build_pitch_solutions() above.
    # This is the solution wherein we use fit_pitch_function_constraints - which for these simpler cases is
    # overkill.  If function fitting starts to return multiple answers though, this is the kind of solution you need.
    def _build_pitch_solutions_old(self, beat_score_results, pitch_constraints):
        """
        Build the final results using the beat results, then the pitch results, then the reshape constraints.
        :param beat_score_results: Set of (PositionDeltaInfo, LiteScore)'s
        :param pitch_constraints: Set of Constraints
        :return:
        """
        final_results = list()
        pitch_results = list()

        # Solve the pitch constraints using the beat constraint results.
        if beat_score_results is not None:
            for beat_result_pdi, beat_result_score in beat_score_results:
                revised_constraints = TReshape._regenerate_constraints(pitch_constraints,
                                                                       self.score.line, beat_result_score.line)
                pitch_solver = PitchConstraintSolver(revised_constraints)
                p_map_dict = PMap(self._build_p_map_dict(beat_result_pdi.hct, revised_constraints))
                pitch_solver_results = pitch_solver.solve(p_map_dict)
                for pitch_pmap in pitch_solver_results:
                    line = pitch_pmap.apply(beat_result_score.line)
                    pitch_results.append((pitch_pmap, beat_result_score,
                                          LiteScore(line,
                                                    beat_result_pdi.hct,
                                                    self.score.instrument,
                                                    beat_result_pdi.tempo_event_sequence,
                                                    beat_result_pdi.ts_event_sequence)))

        else:
            pitch_solver = PitchConstraintSolver(pitch_constraints)
            p_map_dict = PMap(self._build_p_map_dict(self.score.hct, pitch_constraints))
            pitch_solver_results = pitch_solver.solve(p_map_dict)
            for pitch_pmap in pitch_solver_results:
                line = pitch_pmap.apply(self.score.line)
                pitch_results.append((pitch_pmap, self.score, LiteScore(line, self.score.hct, self.score.instrument,
                                      self.score.tempo_sequence, self.score.time_signature_sequence)))

        # Solve the reshape constraints using the pitch constraint solutions.
        for pitch_result_pmap, beat_result_score, pitch_result_score in pitch_results:
            # Issue 1. we generate constraints for ALL NOTES on pitch_result_score's line, note that this means
            #          we cannot reliably use pitch_result_pmap further on since pitch_result_score is buily with
            #          an apply - meaning the notes are in the pmap's range, not domain.
            # tersely:  pitch_result_pmap: self.score.line --> pitch_result_score.line
            q = {key: value for key, value in zip(beat_result_score.line.get_all_notes(),
                                                  pitch_result_score.line.get_all_notes())}
            ignore_notes = {q[n] for n in pitch_result_pmap.keys()
                            if pitch_result_pmap[n].note is not None}
            reshape_constraints = self._generate_reshape_constraints(pitch_result_score.line,
                                                                     pitch_result_score.tempo_sequence,
                                                                     pitch_result_score.time_signature_sequence,
                                                                     ignore_notes)

            p_map = PMap()
            for c in reshape_constraints:
                note = c.actor_note
                hc = pitch_result_score.hct[note.get_absolute_position().position]
                if hc is None:
                    raise Exception('Cannot locate harmonic context for note \'{0}\''.format(note))
                contextual = ContextualNote(PolicyContext(hc,
                                                          pitch_result_score.instrument.sounding_pitch_range()
                                                          if pitch_result_score.instrument is not None
                                                          else PitchRange.create('A:0', 'C:8')))
                # Note: p_map maps from pitch_result_score's line notes to something else (does not matter)
                p_map[note] = contextual

            pitch_solver = PitchConstraintSolver(reshape_constraints)
            reshape_results = pitch_solver.solve(p_map)
            # reshape_pmap_result maps pitch_result_score's line notes to something else with a pitch designation.
            # Issue 2): we are getting failures on some notes due to being too close to chord on beat. In these cases,
            #           the solve is not failing, but giving back a partial result.
            for reshape_pmap_result in reshape_results:
                master_pmap = PMap()
                # Not sure  pitch_result_pmap maps from beat_score_result.line notes to a note with pitch desig.
                # reshape_pmap_result pitch_result_score's line notes to something else with a pitch designation.
                # mm: beat_result_score --> self.score or beat_result_score
                mm = {key: value for key, value in zip(beat_result_score.line.get_all_notes()
                                                       if beat_result_score else self.score.line.get_all_notes(),
                                                       pitch_result_score.line.get_all_notes())}
                for note in pitch_result_pmap.keys():
                    # map notes in pitch_result_score to what beat_score_result would
                    master_pmap[mm[note]] = pitch_result_pmap[note]
                for note in reshape_pmap_result.keys():
                    if note not in master_pmap.keys():
                        master_pmap[note] = reshape_pmap_result[note]
                line_answer = master_pmap.apply(pitch_result_score.line)
                final_results.append(LiteScore(line_answer, pitch_result_score.hct,
                                               pitch_result_score.instrument,
                                               pitch_result_score.tempo_sequence,
                                               pitch_result_score.time_signature_sequence))

        return final_results
