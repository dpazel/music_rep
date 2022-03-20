"""

File: pitch_step_constraint.py

Purpose: Constraint that compute a second pitch from the first based on a number of diatonic steps.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from tonalmodel.pitch_scale import PitchScale
from structure.note import Note
from misc.ordered_set import OrderedSet


class PitchStepConstraint(AbstractConstraint):
    """
    Class representing constraints that computes a second note based on the pitch of the first and a number of 
    diatonic steps, either up or down.
    """

    UP = True
    Down = False

    def __init__(self, note_one, note_two, n_steps=1, up_down=UP):
        """
        Constructor
        :param note_one: The proxy note for the first note
        :param note_two: The proxy note for the second note
        :param n_steps: Positive number, number of steps
        :param up_down: UP (True) or DOWN (False)
        """
        AbstractConstraint.__init__(self, [note_one, note_two])

        self._n_steps = n_steps
        self._up_down = up_down

    @property
    def note_one(self):
        return self.actors[0]

    @property
    def note_two(self):
        return self.actors[1]

    @property
    def n_steps(self):
        return self._n_steps

    @property
    def up_down(self):
        return self._up_down

    def clone(self, new_actors=None):
        return PitchStepConstraint(new_actors[0] if new_actors is not None else self.note_one,
                                   new_actors[1] if new_actors is not None else self.note_two,
                                   self.n_steps,
                                   self.up_down)

    def verify(self, parameter_map):
        """
        Verify that the note pitch of the first proxy and the note pitch of the second proxy meet the constraints
        diatonic distance.
        :param parameter_map: 
        :return: 
        """
        first_contextual_note = parameter_map[self.note_one]
        second_contextual_note = parameter_map[self.note_two]
        if str(first_contextual_note.policy_context.harmonic_context.tonality) != \
                str(second_contextual_note.policy_context.harmonic_context.tonality):
            raise Exception('Note one and two of tonal step constraints must match')

        pitch_scale = PitchScale(first_contextual_note.policy_context.harmonic_context.tonality,
                                 first_contextual_note.policy_context.pitch_range)
        scale = pitch_scale.pitch_scale

        if first_contextual_note.note is None or second_contextual_note.note is None:
            return False

        first_pitch = first_contextual_note.note.diatonic_pitch
        second_pitch = second_contextual_note.note.diatonic_pitch

        first_index = scale.index(first_pitch) if first_pitch in scale else None
        second_index = scale.index(second_pitch) if second_pitch in scale else None

        if first_index is None or second_index is None:
            return False

        return second_index - first_index == self.n_steps * (1 if self.up_down == PitchStepConstraint.UP else -1)

    def values(self, p_map, v_target_note):
        if v_target_note == self.note_two:
            up_down = self.up_down
            v_source_note = self.note_one
        elif v_target_note == self.note_one:
            up_down = not self.up_down
            v_source_note = self.note_two
        else:
            raise Exception('v_note specification does not match any v_note in constraints.')

        if p_map[v_target_note].note is not None:
            return OrderedSet([p_map[v_target_note].note])

        arg_contextual_note = p_map[v_source_note]
        target_contextual_note = p_map[v_target_note]

        if arg_contextual_note.note is None:
            pitches = p_map.all_tonal_pitches(v_target_note)
            result = OrderedSet()
            for p in pitches:
                result.add(Note(p, v_target_note.base_duration, v_target_note.num_dots))
            return result
            #return {Note(p, v_target_note.base_duration, v_target_note.num_dots) for p in pitches}

        return self.compute_result(arg_contextual_note, target_contextual_note, up_down)

    def compute_result(self, arg_contextual_note, target_contextual_note, up_down):
        """
        Compute the target note from the arg note basecd on up_down and self.n_steps.
        
        :param arg_contextual_note: Given note
        :param target_contextual_note: Note to find based on constraints.
        :param up_down: 
        :return: 
        """
        if str(arg_contextual_note.policy_context.harmonic_context.tonality) != \
                str(target_contextual_note.policy_context.harmonic_context.tonality):
            raise Exception('Note one and two of tonal step constraints must match on tonality')

        starting_pitch = arg_contextual_note.note.diatonic_pitch

        pitch_scale = PitchScale(target_contextual_note.policy_context.harmonic_context.tonality,
                                 target_contextual_note.policy_context.pitch_range)
        scale = pitch_scale.pitch_scale
        pitch_index = scale.index(starting_pitch) if starting_pitch in scale else None
        if pitch_index is None:
            return None

        end_index = pitch_index + (self.n_steps * (1 if up_down == PitchStepConstraint.UP else -1))
        if end_index not in range(0, len(scale)):
            return None

        end_pitch = scale[end_index]
        return OrderedSet([Note(end_pitch, self.note_two.base_duration, self.note_two.num_dots)])
