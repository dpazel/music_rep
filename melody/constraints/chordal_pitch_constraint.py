"""
File: chordal_tone_policy.py

Purpose: A policy to ensure a pitch assigns to a chordal tone.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.chromatic_scale import ChromaticScale
from misc.ordered_set import OrderedSet


class ChordalPitchConstraint(AbstractConstraint):
    """
    Class representing a constraints for a tone to be a chordal pitch.
    """

    def __init__(self, actor_note):
        """
        Constructor.
        :param actor_note: single note or list with one note
        """
        if actor_note is None:
            raise Exception('ChordalPitchConstraint requires a note actor.')
        actor = actor_note[0] if isinstance(actor_note, list) else actor_note

        AbstractConstraint.__init__(self, [actor])

    @property
    def actor_note(self):
        return self.actors[0]

    def clone(self, new_actors=None):
        return ChordalPitchConstraint(new_actors if new_actors is not None else self.actors)

    def __str__(self):
        return '{0}'.format(self.actor_note.diatonic_pitch)

    def verify(self, parameter_map):
        if parameter_map is None or self.actor_note not in parameter_map:
            raise Exception('Improper parameter map')

        target_contextual_note = parameter_map[self.actor_note]
        if parameter_map[self.actor_note].note is None:
            return False

        tone = target_contextual_note.note.diatonic_pitch.diatonic_tone
        tones = [t[0] for t in target_contextual_note.policy_context.harmonic_context.chord.tones]
        if tone not in tones:
            return False
        return target_contextual_note.policy_context.pitch_range.is_pitch_inbounds(
            str(target_contextual_note.note.diatonic_pitch))

    def values(self, p_map, v_note):
        """
        Return a set of possible pitches that v_note can take that must be in p_map target's chord.
        :param p_map: 
        :param v_note: 
        :return: 
        """
        if v_note != self.actor_note:
            raise Exception('v_note {0} not in ChordalToneConstraint actors.'.format(v_note.note))

        policy_context = p_map[self.actor_note].policy_context
        tones = policy_context.harmonic_context.chord.tones
        if p_map[v_note].note is not None:
            note = p_map[v_note].note
            if note.diatonic_pitch.diatonic_tone in tones:
                return {note}
            raise Exception('Chordal Pitch Policy Violated has {0} should be member of chord {1}'.format(
                p_map[v_note].note.diatonic_pitch, policy_context.harmonic_context.chord))

        pitch_range = policy_context.pitch_range
        start_partition = max(ChromaticScale.index_to_location(pitch_range.start_index)[0] - 1, 0)
        end_partition = min(ChromaticScale.index_to_location(pitch_range.end_index)[0] + 1,
                            ChromaticScale.CHROMATIC_END[0])

        valid_set = OrderedSet()
        for tone in tones:
            for i in range(start_partition, end_partition + 1):
                pitch = DiatonicPitch(i, tone[0])
                if pitch_range.is_pitch_inbounds(str(pitch)):
                    note = Note(pitch, self.actor_note.base_duration, self.actor_note.num_dots)
                    valid_set.add(note)

        return valid_set
