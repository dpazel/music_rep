"""

File: pitch_range_constraint.py

Purpose: An N-note constraint directing that actor notes fall within a specific pitch range.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.pitch_scale import PitchScale


class PitchRangeConstraint(AbstractConstraint):

    def __init__(self, range_notes, pitch_range):
        """
        Constructor
        :param range_notes: list of all v_notes, map notes all same pitch range.
        :param pitch_range:
        """
        AbstractConstraint.__init__(self, range_notes)

        self._pitch_range = pitch_range

    @property
    def pitch_range(self):
        return self._pitch_range

    def clone(self, new_actors=None):
        return PitchRangeConstraint(new_actors if new_actors is not None else self.actors, self.pitch_range)

    def verify(self, p_map):
        for v_note in self.actors:
            if v_note not in p_map:
                raise Exception('Improper parameter map in pitch range constraints.')
            if p_map[v_note].note is None:
                return False

        for i in range(0, len(self.actors)):
            if not self.pitch_range.is_pitch_inbounds(p_map[self.actors[i]].note.diatonic_pitch):
                return False
        return True

    def values(self, p_map, v_note):
        assigned = p_map.assigned_actors(self)
        unassigned = p_map.unassigned_actors(self)
        if v_note in unassigned:
            tonality = p_map[v_note].policy_context.harmonic_context.tonality
            pitches = PitchScale.compute_tonal_pitches(tonality, self.pitch_range)
            return {Note(p, v_note.base_duration, v_note.num_dots) for p in pitches}

        if v_note in assigned:
            return {p_map[v_note].note}

        raise Exception('{0} is not in actor list for pitch range constraints.'.format(v_note.note))

    def __str__(self):
        note_str = ','.join([str(x) for x in self.actors])
        return 'p.r.p{0}: {1}'.format(note_str, self.pitch_range)
