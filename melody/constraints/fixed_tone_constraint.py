"""
File: fixed_tone_constraint.py

Purpose: Policy to ensure the mapped note (of a given note) is fixed to a tone.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.pitch_scale import PitchScale
from tonalmodel.chromatic_scale import ChromaticScale


class FixedToneConstraint(AbstractConstraint):
    """
    Class representing constraint ensuring mapped tone to constructor note is fixed to a specific tone.
    """

    def __init__(self, actor_note, tone):
        """
        Constructor.
        :param actor_note: ContextualNote
        :param tone:
        """

        AbstractConstraint.__init__(self, [actor_note])

        self._tone = tone

    @property
    def tone(self):
        return self._tone

    @property
    def actor_note(self):
        return self.actors[0]

    def clone(self, new_actors=None):
        return FixedToneConstraint(new_actors[0] if new_actors is not None else self.actor_note, self.tone)

    def values(self, p_map, v_note):
        if v_note != self.actor_note:
            raise Exception("Illegal v_note {0} for constraints".format(v_note))
        if p_map[v_note].note is not None:
            if p_map[v_note].note.diatonic_pitch.diatonic_tone == self.tone:
                return {p_map[v_note].note}
            raise Exception('Fixed Tone Policy Violated has {0} should be {1}'.format(
                p_map[v_note].note.diatonic_pitch.diatonic_tone, self.tone))

        contextual_note = p_map[self.actor_note]
        policy_context = contextual_note.policy_context
        pitch_range = contextual_note.policy_context.pitch_range
        start_partition = max(ChromaticScale.index_to_location(pitch_range.start_index)[0] - 1, 0)
        end_partition = min(ChromaticScale.index_to_location(pitch_range.end_index)[0] + 1,
                            ChromaticScale.CHROMATIC_END[0])

        # Try to find that tone in target's tonality/scale.
        tone = self.tone
        for t_str in self.tone.enharmonics():
            t = DiatonicToneCache.get_tone(t_str)
            for scale_tone in PitchScale(policy_context.harmonic_context.tonality,
                                         policy_context.pitch_range).tone_scale:
                if scale_tone == t:
                    tone = t
                    break

        valid_set = set()
        for i in range(start_partition, end_partition + 1):
            pitch = DiatonicPitch(i, tone)
            if pitch_range.is_pitch_inbounds(pitch):
                note = Note(pitch, self.actor_note.note.base_duration, self.actor_note.note.num_dots)
                valid_set.add(note)

        return valid_set

    def verify(self, parameter_map):
        if parameter_map is None or self.actor_note not in parameter_map:
            raise Exception('Improper parameter map')
        contextual_note = parameter_map[self.actor_note]
        return parameter_map[self.actor_note].note.diatonic_pitch.diatonic_tone.placement == self.tone.placement and \
            contextual_note.policy_context.pitch_range.is_pitch_inbounds(
                parameter_map[self.actor_note].note.diatonic_pitch)
