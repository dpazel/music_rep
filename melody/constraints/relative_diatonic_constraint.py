"""

File: relative_diatonic_constraint.py

Purpose: Constraint that compute a second pitch from the first based on interval ranges.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from tonalmodel.pitch_scale import PitchScale
from tonalmodel.pitch_range import PitchRange
from structure.note import Note


class RelativeDiatonicConstraint(AbstractConstraint):
    """
    Class representing constraints that computes a second note based on the pitch of the first and within an interval 
    bounded by upper and lower intervals.
    """

    def __init__(self, note_one, note_two, up_interval, down_interval):
        """
        
        :param note_one: 
        :param note_two: 
        :param up_interval: 
        :param down_interval: 
        """
        AbstractConstraint.__init__(self, [note_one, note_two])

        self._up_interval = up_interval
        self._down_interval = down_interval

    @property
    def note_one(self):
        return self.actors[0]

    @property
    def note_two(self):
        return self.actors[1]

    @property
    def up_interval(self):
        return self._up_interval

    @property
    def down_interval(self):
        return self._down_interval

    def clone(self, new_actors=None):
        return RelativeDiatonicConstraint(new_actors[0] if new_actors is not None else self.note_one,
                                          new_actors[1] if new_actors is not None else self.note_two,
                                          self.up_interval,
                                          self.down_interval)

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

        diff = second_contextual_note.note.diatonic_pitch.chromatic_distance - \
            first_contextual_note.note.diatonic_pitch.chromatic_distance
        total_distance = self.up_interval.chromatic_distance + self.down_interval.chromatic_distance
        return abs(diff) <= total_distance

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
            up_intvl = self.up_interval
            down_intvl = self.down_interval
        elif v_note == self.note_one:
            source = self.note_two
            target = self.note_one
            up_intvl = self.down_interval
            down_intvl = self.up_interval
        else:
            raise Exception('v_note specification does not match any v_note in constraints.')

        if p_map[target].note is not None:
            return {p_map[target].note}

        arg_contextual_note = p_map[source]
        target_contextual_note = p_map[target]

        if arg_contextual_note.note is None:
            pitches = p_map.all_tonal_pitches(v_note)
            return {Note(p, v_note.base_duration, v_note.num_dots) for p in pitches}

        return self.compute_result(arg_contextual_note, target_contextual_note, up_intvl, down_intvl)

    def compute_result(self, arg_contextual_note, target_contextual_note, up_intvl, down_intvl):
        """
        
        :param arg_contextual_note: 
        :param target_contextual_note: 
        :param up_intvl: 
        :param down_intvl: 
        :return: 
        """

        starting_pitch = arg_contextual_note.note.diatonic_pitch
        chromatic_distance_start = starting_pitch.chromatic_distance - down_intvl.chromatic_distance
        chromatic_distance_end = starting_pitch.chromatic_distance + up_intvl.chromatic_distance

        r_start = max(chromatic_distance_start, target_contextual_note.policy_context.pitch_range.start_index)
        r_end = min(chromatic_distance_end, target_contextual_note.policy_context.pitch_range.end_index)

        if r_start > r_end:
            return {}

        pitch_range = PitchRange(r_start, r_end)
        pitch_scale = PitchScale(target_contextual_note.policy_context.harmonic_context.tonality, pitch_range)

        v_result = {Note(pitch, self.note_two.base_duration, self.note_two.num_dots)
                    for pitch in pitch_scale.pitch_scale}

        return v_result
