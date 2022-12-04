"""

File: not_equal_pitch_constraint.py

Purpose: Defines a two note constraint where the second note's pitch must equal first note's pitch.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from misc.ordered_set import OrderedSet


class NotEqualPitchConstraint(AbstractConstraint):
    """
    
    """

    def __init__(self, not_equal_notes):
        """
        
        :param not_equal_notes: 
        """
        AbstractConstraint.__init__(self, not_equal_notes)
        if len(not_equal_notes) <= 1:
            raise Exception('NotEqualNotePolicy must have two or more v-notes.')

    def clone(self, new_actors=None):
        return NotEqualPitchConstraint(new_actors if new_actors is not None else self.actors)

    def verify(self, p_map):
        not_equal_notes = self.actors
        for v_note in not_equal_notes:
            if v_note not in p_map:
                raise Exception('Improper parameter map in equal note constraints.')
            if p_map[v_note].note is None:
                return False

        t_note_list = [p_map[cn].note for cn in not_equal_notes]
        return NotEqualPitchConstraint.validity_check(t_note_list)[0]

    def values(self, p_map, v_note):
        """
        Find value candidates for v_note target, given p_map.
        In this constraints, we are more interested in the set of values that v_note target cannot take.
        
        :param p_map: 
        :param v_note: 
        :return: 
        """
        assigned = p_map.assigned_actors(self)
        unassigned = p_map.unassigned_actors(self)
        if len(assigned) == 0:
            pitches = p_map.all_tonal_pitches(v_note)
            return {Note(p, v_note.note.base_duration, v_note.note.num_dots) for p in pitches}
        if v_note in assigned:
            return {p_map[v_note].note}
        if v_note not in unassigned:
            raise Exception('{0} is not in actor list of not equal pitch constraints.'.format(v_note.note))

        e_set = OrderedSet()
        for v in assigned:
            e_set.add(p_map[v].note)

        return NotEqualPitchConstraint.compute_full_result(p_map, v_note, e_set)

    @staticmethod
    def compute_full_result(p_map, v_note, e_set):
        pitches = p_map.all_tonal_pitches(v_note)
        e_chrm_list = [n.diatonic_pitch.chromatic_distance for n in e_set]
        del_set = OrderedSet()
        for p in pitches:
            if p.chromatic_distance in e_chrm_list:
                del_set.add(p)

        pitches = [p for p in pitches if p not in del_set]

        return OrderedSet([Note(p, v_note.base_duration, v_note.num_dots) for p in pitches])

    @staticmethod
    def validity_check(note_list):

        # We compare diatonic distances, as the notes may be enharmonic due to differing tonalities.
        for i in range(0, len(note_list)):
            for j in range(0, len(note_list)):
                if i != j:
                    if note_list[i].diatonic_pitch.diatonic_distance() == \
                            note_list[j].diatonic_pitch.diatonic_distance():
                        return False, note_list[i]
        return True, None
