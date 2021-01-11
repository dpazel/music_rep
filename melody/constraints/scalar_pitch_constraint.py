from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.chromatic_scale import ChromaticScale
from tonalmodel.diatonic_pitch import DiatonicPitch


class ScalarPitchConstraint(AbstractConstraint):
    """
    Class representing constraints to ensure some one note is scalar (to the contextual tonality), or within
    some subset of tones of the tonality.
    """

    def __init__(self, note, scalar_roles=list()):
        '''
        Constraint constuctor.
        :param note: Actor affected by constraint.
        :param scalar_roles: List of integer indices to tones in the current tonality, to which the actor must conform.
        '''
        AbstractConstraint.__init__(self, [note])

        self.__scalar_notes = list(scalar_roles)

    @property
    def actor_note(self):
        return self.actors[0]

    @property
    def scalar_roles(self):
        return self.__scalar_notes

    def clone(self, new_actors=None):
        pass

    def verify(self, parameter_map):
        contextual_note = parameter_map[self.actor_note]
        if contextual_note.note is None:
            return False

        tone = contextual_note.note.diatonic_pitch.diatonic_tone
        if len(self.scalar_roles) == 0:
            return tone in contextual_note.policy_context.harmonic_context.tonality.annotation
        else:
            index = contextual_note.policy_context.harmonic_context.tonality.annotation.index(tone)
            return index in self.scalar_roles

    def values(self, p_map, v_note):
        if v_note != self.actor_note:
            raise Exception('v_note {0} not in ScalarConstraint actors.'.format(v_note.note))

        policy_context = p_map[self.actor_note].policy_context
        tones = list(policy_context.harmonic_context.tonality.annotation)
        tones = tones[:-1]   # remove final note (same as first)
        if len(self.scalar_roles) != 0:
            tones = [tones[i] for i in self.scalar_roles]
        if p_map[v_note].note is not None:
            tone = p_map[v_note].note.diatonic_pitch.diatonic_tone
            return {self.actor_note} if tone in tones else None

        pitch_range = policy_context.pitch_range
        start_partition = max(ChromaticScale.index_to_location(pitch_range.start_index)[0] - 1, 0)
        end_partition = min(ChromaticScale.index_to_location(pitch_range.end_index)[0] + 1,
                            ChromaticScale.CHROMATIC_END[0])

        valid_set = set()

        for tone in tones:
            for j in range(start_partition, end_partition + 1):
                pitch = DiatonicPitch(j, tone)
                if pitch_range.is_pitch_inbounds(pitch):
                    note = Note(pitch, self.actor_note.base_duration, self.actor_note.num_dots)
                    valid_set.add(note)

        return valid_set
