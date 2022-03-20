"""

File: relative_step_constraint.py

Purpose: Constraint that computes a second pitch from the first based on relative number of scalar steps.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.pitch_scale import PitchScale
from misc.ordered_set import OrderedSet


class RelativeScalarStepConstraint(AbstractConstraint):
    """
    Class representing constraint that computes a second note based on the pitch of the first and within an interval
    bounded a range of diatonic steps.
    """

    def __init__(self, note_one, note_two, lower_steps, upper_steps):
        """
        Constructor.
        :param note_one: 
        :param note_two: 
        :param lower_steps: Number of 'note two' tonality steps below lower match.
        :param upper_steps: Number of 'note two' tonality steps above upper match.
        """
        AbstractConstraint.__init__(self, [note_one, note_two])

        if lower_steps > upper_steps:
            raise Exception('Relative steps require first arg {0} <= second {1}.'.format(lower_steps, upper_steps))

        self._lower_steps = lower_steps
        self._upper_steps = upper_steps

    @property
    def note_one(self):
        return self.actors[0]

    @property
    def note_two(self):
        return self.actors[1]

    @property
    def lower_steps(self):
        return self._lower_steps

    @property
    def upper_steps(self):
        return self._upper_steps

    def clone(self, new_actors=None):
        return RelativeScalarStepConstraint(new_actors[0] if new_actors is not None else self.note_one,
                                            new_actors[1] if new_actors is not None else self.note_two,
                                            self.lower_steps,
                                            self.upper_steps)

    def verify(self, parameter_map):
        """
        Verify that p_map has values satisfying the constraint.
        :param parameter_map: 
        :return: 
        """
        first_contextual_note = parameter_map[self.note_one]
        second_contextual_note = parameter_map[self.note_two]
        if first_contextual_note.note is None or second_contextual_note.note is None:
            return False

        pitches = PitchScale.compute_tonal_pitch_range(
            second_contextual_note.policy_context.harmonic_context.tonality,
            first_contextual_note.note.diatonic_pitch,
            self.lower_steps,
            self.upper_steps)

        return second_contextual_note.note.diatonic_pitch in pitches

    def values(self, p_map, v_note):
        """
        Compute possible values for v_note's target.
        :param p_map: 
        :param v_note: 
        :return: 

        Note: Here is why the intervals are reversed for solving for note_one:
              Suppose x --> [x-a, x + b].  Then for some value y, 
              for t with y-b<=t<=y+a, we have t -->[t-a, t+b], but
              from the inequalities, t-a<=y<t+b - so the reverse map is
              [y-b, y+a] <-- y, which is exactly what happens below.
        """
        if v_note == self.note_two:
            source = self.note_one
            target = self.note_two
            up_steps = self.upper_steps
            down_steps = self.lower_steps
        elif v_note == self.note_one:
            source = self.note_two
            target = self.note_one
            up_steps = -self.lower_steps
            down_steps = -self.upper_steps
        else:
            raise Exception('v_note specification does not match any v_note in constraints.')

        if p_map[target].note is not None:
            return OrderedSet([p_map[target].note])

        arg_contextual_note = p_map[source]
        target_contextual_note = p_map[target]

        if arg_contextual_note.note is None:
            pitches = p_map.all_tonal_pitches(v_note)
            answer = OrderedSet()
            for p in pitches:
                answer.add(Note(p, v_note.base_duration, v_note.num_dots))
            return answer

        return self.compute_result(arg_contextual_note, target_contextual_note, down_steps, up_steps)

    def compute_result(self, arg_contextual_note, target_contextual_note, down_steps, up_steps):
        arg_pitch = arg_contextual_note.note.diatonic_pitch

        pitches = PitchScale.compute_tonal_pitch_range(
            target_contextual_note.policy_context.harmonic_context.tonality,
            arg_pitch,
            down_steps,
            up_steps)

        result = OrderedSet()
        for pitch in pitches:
            result.add(Note(pitch, self.note_two.base_duration, self.note_two.num_dots))

        return result
