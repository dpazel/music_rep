"""

File: equal_pitch_policy.py

Purpose: Defines a two note policy where the second note's pitch must equal first note's pitch.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.pitch_scale import PitchScale


class EqualPitchConstraint(AbstractConstraint):
    """
    Multi-note constraints that claims that both notes have the same pitch value.
    """

    def __init__(self, equal_notes):
        """
        Constructor
        :param equal_notes: list of all v_notes that map to notes, mapped notes all same pitch.
        """
        AbstractConstraint.__init__(self, equal_notes)
        if len(equal_notes) <= 1:
            raise Exception('EqualNotePolicy must have two or v-more notes.')

    def clone(self, new_actors=None):
        return EqualPitchConstraint(new_actors if new_actors is not None else self.actors)

    def verify(self, p_map):
        """
        Ensure the two mapped actors have identical pitches.
        :param p_map:
        :return:
        """
        equal_notes = self.actors
        for v_note in equal_notes:
            if v_note not in p_map:
                raise Exception('Improper parameter map in equal note constraints.')
            if p_map[v_note].note is None:
                return False

        # We compare diatonic distances, as the notes may be enharmonic due to differing tonalities.
        for i in range(0, len(equal_notes) - 1):
            if p_map[equal_notes[i]].note.diatonic_pitch.diatonic_distance != \
                    p_map[equal_notes[i + 1]].note.diatonic_pitch.diatonic_distance:
                return False
        return True

    def values(self, p_map, v_note):
        assigned = p_map.assigned_actors(self)
        unassigned = p_map.unassigned_actors(self)
        if len(assigned) == 0:
            pitches = p_map.all_tonal_pitches(v_note)
            return {Note(p, v_note.base_duration, v_note.num_dots) for p in pitches}
        if v_note in assigned:
            return {p_map[v_note].note}
        if v_note not in unassigned:
            raise Exception('{0} is not in actor list of equal pitch constraints.'.format(v_note.note))
        return EqualPitchConstraint.compute_note(p_map, assigned[0], v_note)

    @staticmethod
    def compute_note(p_map, assigned_note, unassigned_note):
        """
        For an assigned note and an unassigned note, return for unassigned, a note the same as assigned, but with
        pitch enharmonic to its tonality.
        :param p_map: 
        :param assigned_note: 
        :param unassigned_note: 
        :return: 
        """

        # select a pitch representation closest to the tonality, if it exists.
        policy_context = p_map[unassigned_note].policy_context
        pitch = p_map[assigned_note].note.diatonic_pitch
        for p in pitch.enharmonics():
            for t in PitchScale(policy_context.harmonic_context.tonality, policy_context.pitch_range).tone_scale:
                if p.diatonic_tone == t:
                    pitch = p
                    break

        actual_note = Note(pitch, unassigned_note.base_duration, unassigned_note.num_dots)
        return {actual_note}

    def __str__(self):
        note_str = ','.join([str(x) for x in self.actors])
        return 'e.p.p{0}'.format(note_str)
