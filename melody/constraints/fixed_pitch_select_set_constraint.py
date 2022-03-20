"""

File: fixed_pitch_select_set_constraint.py

Purpose: Constraint that fixes choice of pitches for a note from a specific set of pitches.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from misc.ordered_set import OrderedSet


class FixedPitchSelectSetConstraint(AbstractConstraint):
    """
    Constraint holding the target note to one of a given set of pitches.
    Rule: If fixed pitches has enharmonic in target tonality, we use that pitch representation.
    Rule: The source context (actor_note) note need not be at the fixed pitch - the actor note is a place holder.
    """

    def __init__(self, actor_note, pitches):
        """
        Constructor.
        :param actor_note:  note as actor for this constraint.
        :param pitch: list of pitches
        """
        AbstractConstraint.__init__(self, [actor_note])

        self.__pitches = list(pitches)

    @property
    def pitches(self):
        return list(self.__pitches)

    @property
    def actor_note(self):
        return self.actors[0]

    def clone(self, new_actors=None):
        return FixedPitchSelectSetConstraint(new_actors[0] if new_actors is not None else self.actor_note, self.pitches)

    def verify(self, parameter_map):
        if parameter_map is None or self.actor_note not in parameter_map:
            raise Exception('Improper parameter map')
        if parameter_map[self.actor_note].note is None:
            return False

        for p in self.pitches:
            if parameter_map[self.actor_note].note.diatonic_pitch.chromatic_distance == p.chromatic_distance:
                return True
        return False

    def values(self, p_map, v_note):
        if v_note != self.actor_note:
            raise Exception("Illegal v_note {0} for constraint".format(v_note))
        if p_map[v_note].note is not None:
            if p_map[v_note].note.diatonic_pitch.chromatic_distance in (p.chromatic_distance for p in self.pitches):
                return OrderedSet[p_map[v_note].note]
            raise Exception('Fixed Pitch Select Set Constraint Violated has {0} not in pitch set'.format(
                p_map[v_note].note.diatonic_pitch))

        # Return all pitches (self.pitches) except though, for each
        # select a representation closest to the target tonality, if it exists.
        tonality = p_map[self.actor_note].policy_context.harmonic_context.tonality
        result_pitches = []
        for pitch in self.pitches:
            found_pitch = pitch
            for p in pitch.enharmonics():
                if p.diatonic_tone in tonality.annotation:
                    found_pitch = p
                    break
            result_pitches.append(found_pitch)

        result = OrderedSet()
        for p in result_pitches:
            result.add(Note(p, self.actor_note.base_duration, self.actor_note.num_dots))
        return result
        # return {Note(p, self.actor_note.base_duration, self.actor_note.num_dots) for p in result_pitches}
