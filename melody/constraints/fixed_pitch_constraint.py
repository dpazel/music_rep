"""

File: fixed_pitch_constraint.py

Purpose: Constraint that affirms a single note must comply to have a specified pitch.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note


class FixedPitchConstraint(AbstractConstraint):
    """
    Constraint holding the target note to a given fixed pitch.
    Rule: If fixed pitch has enharmonic in target tonality, we use that pitch representation.
    Rule: The source context (actor_note) note need not be at the fixed pitch - the actor note is a place holder.
    """

    def __init__(self, actor_note, pitch):
        """
        Constructor.
        :param actor_note:  Note as actor for this constraint.
        :param pitch:
        """
        AbstractConstraint.__init__(self, [actor_note])

        self.__pitch = pitch

    @property
    def pitch(self):
        return self.__pitch

    @property
    def actor_note(self):
        return self.actors[0]

    def clone(self, new_actors=None):
        return FixedPitchConstraint(new_actors[0] if new_actors is not None else self.actor_note, self.pitch)

    def verify(self, p_map):
        if p_map is None or self.actor_note not in p_map:
            raise Exception('Improper parameter map')
        if p_map[self.actor_note].note is None:
            return False
        return p_map[self.actor_note].note.diatonic_pitch.chromatic_distance == self.pitch.chromatic_distance

    def values(self, p_map, v_note):
        if v_note != self.actor_note:
            raise Exception("Illegal v_note {0} for constraint".format(v_note))
        if p_map[v_note].note is not None:
            if p_map[v_note].note.diatonic_pitch.chromatic_distance == self.pitch.chromatic_distance:
                return {p_map[v_note].note}
            raise Exception('Fixed Pitch Constraint Violated has {0} should be {1}'.format(
                p_map[v_note].note.diatonic_pitch, self.pitch))

        # select a pitch representation closest to the target tonality, if it exists.
        policy_context = p_map[self.actor_note].policy_context
        pitch = self.pitch
        for p in self.pitch.enharmonics():
            if p.diatonic_tone in policy_context.harmonic_context.tonality.annotation:
                pitch = p
                break

        actual_note = Note(pitch, self.actor_note.base_duration, self.actor_note.num_dots)
        return {actual_note}
