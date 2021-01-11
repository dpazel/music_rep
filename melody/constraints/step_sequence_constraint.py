"""

File: step_sequence_policy.py

Purpose: Ordered list of notes that vary by a number of diatonic steps.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.pitch_scale import PitchScale


class StepSequenceConstraint(AbstractConstraint):
    """
    Multi-note constraint that in sequence varies each to each by a number of diatonic steps.
    """

    def __init__(self, note_sequence, variance_list):
        """
        Constructor.
        :param note_sequence: list of v_notes that vary in sequence by a number of diatonic steps.
        :param variance_list:  list of numbers representing variances.
        Note: len(variance_list) = len(note_sequence) - 1
        """
        AbstractConstraint.__init__(self, note_sequence)
        if len(note_sequence) <= 1:
            raise Exception('StepSequencePolicy must have two or v-more notes.')
        if len(note_sequence) - 1 != len(variance_list):
            raise Exception("Illegan size for variance list")

        self._variance_list = variance_list

    @property
    def variance_list(self):
        return self._variance_list

    def clone(self, new_actors=None):
        return StepSequenceConstraint(new_actors if new_actors is not None else self.actors,
                                      self.variance_list)

    def verify(self, p_map):
        """

        :param p_map:
        :return:
        """
        notes = self.actors
        for v_note in notes:
            if v_note not in p_map:
                raise Exception('Improper parameter map in equal note constraints.')
            if p_map[v_note].note is None:
                return False

        # We compare diatonic distances, as the notes may be enharmonic due to differing tonalities.
        for i in range(0, len(notes) - 1):
            if p_map[notes[i + 1]].note.diatonic_pitch.diatonic_distance() - \
                    p_map[notes[i]].note.diatonic_pitch.diatonic_distance() != self.variance_list[i]:
                return False
        return True

    def values(self, p_map, v_note):
        """

        :param p_map:
        :param v_note:
        :return:
        """

        index = self.actors.index(v_note) if v_note in self.actors else None
        if index is None:
            raise Exception('Cannot find v_note in constraints actors')

        if p_map[v_note].note is not None:
            return {p_map[v_note].note}

        # find the first assigned note
        assigned_index = None
        for i in range(0, len(self.actors)):
            if p_map[self.actors[i]].note is not None:
                assigned_index = i
                break

        if assigned_index is None:
            pitches = p_map.all_tonal_pitches(v_note)
            return [Note(p, v_note.base_duration, v_note.num_dots) for p in pitches]

        known_note = p_map[self.actors[assigned_index]].note
        if assigned_index < index:
            for i in range(assigned_index + 1, index + 1):
                unknown_contextual_note = p_map[self.actors[i]]
                unknown_note = unknown_contextual_note.note
                if unknown_note is not None:
                    known_note = unknown_note
                    continue

                lower_index = self.variance_list[i - 1] if self.variance_list[i - 1] < 0 else 0
                upper_index = self.variance_list[i - 1] if self.variance_list[i - 1] > 0 else 0
                pitches = PitchScale.compute_tonal_pitch_range(
                    unknown_contextual_note.policy_context.harmonic_context.tonality,
                    known_note.diatonic_pitch, lower_index, upper_index)
                pitch_index = self.variance_list[i - 1] + (len(pitches) - 1 if self.variance_list[i - 1] < 0 else 0)
                if pitch_index < 0 or pitch_index >= len(pitches):
                    if pitches is None or len(pitches) == 0:
                       return {}
                    pitch = pitches[0] if pitch_index < 0 else pitches[len(pitches) - 1]
                else:
                    pitch = pitches[pitch_index]
                known_note = Note(pitch, self.actors[i].base_duration, self.actors[i].num_dots)
            return {known_note}

        for i in range(assigned_index - 1, index - 1, -1):
            unknown_contextual_note = p_map[self.actors[i]]
            unknown_note = unknown_contextual_note.note
            if unknown_note is not None:
                known_note = unknown_note
                continue

            upper_index = -self.variance_list[i] if self.variance_list[i] < 0 else 0
            lower_index = -self.variance_list[i] if self.variance_list[i] > 0 else 0
            pitches = PitchScale.compute_tonal_pitch_range(
                unknown_contextual_note.policy_context.harmonic_context.tonality,
                known_note.diatonic_pitch, lower_index, upper_index)
            pitch_index = -self.variance_list[i] + (len(pitches) - 1 if self.variance_list[i] > 0 else 0)
            if pitch_index < 0:
                pitch_index = 0
            elif pitch_index >= len(pitches):
                pitch_index = len(pitches) - 1
            pitch = pitches[pitch_index]
            known_note = Note(pitch, self.actors[i].base_duration, self.actors[i].num_dots)
        return {known_note}
