"""

File: comparative_pitch_policy.py

Purpose: Defines a two note policy where the second note's pitch and first note's pitch must meet a comparative
         relationship.

"""
from melody.constraints.abstract_constraint import AbstractConstraint
from structure.note import Note
from tonalmodel.pitch_range import PitchRange
from tonalmodel.pitch_scale import PitchScale
from misc.ordered_set import OrderedSet


class ComparativePitchConstraint(AbstractConstraint):
    """
    Two note constraints that claims that both notes have the same pitch value.
    """

    LESS_THAN = 0
    LESS_EQUAL = 1
    EQUAL = 2
    GREATER_EQUAL = 3
    GREATER_THAN = 4

    def __init__(self, note_one, note_two, comparative):
        """
        Constructor.  Note: 'note_one rel note_two'.
        :param note_one: 
        :param note_two: 
        :param comparative: 
        """
        AbstractConstraint.__init__(self, [note_one, note_two])

        self._comparative = comparative

    @property
    def note_one(self):
        return self.actors[0]

    @property
    def note_two(self):
        return self.actors[1]

    @property
    def comparative(self):
        return self._comparative

    def comp_str(self):
        if self.comparative == 0:
            return '<'
        elif self.comparative == 1:
            return '<='
        elif self.comparative == 2:
            return '=='
        elif self.comparative == 3:
            return '>='
        else:
            return '>'

    def __str__(self):
        return '{0} {1} {2}'.format(self.note_one.diatonic_pitch, self.comp_str(), self.note_two.diatonic_pitch)

    def clone(self, new_actors=None):
        return ComparativePitchConstraint(new_actors[0] if new_actors is not None else self.note_one,
                                          new_actors[1] if new_actors is not None else self.note_two,
                                          self.comparative)

    def verify(self, p_map):
        """
        Determine if comparative pitch constraint is satisfied.
        :param p_map: 
        :return: 
        """
        first_contextual_note = p_map[self.note_one]
        second_contextual_note = p_map[self.note_two]
        if first_contextual_note.note is None or second_contextual_note.note is None:
            return False

        p1_d = first_contextual_note.note.diatonic_pitch.chromatic_distance
        p2_d = second_contextual_note.note.diatonic_pitch.chromatic_distance

        if self.comparative == ComparativePitchConstraint.LESS_THAN:
            return p1_d < p2_d
        elif self._comparative == ComparativePitchConstraint.LESS_EQUAL:
            return p1_d <= p2_d
        elif self._comparative == ComparativePitchConstraint.EQUAL:
            return p1_d == p2_d
        elif self._comparative == ComparativePitchConstraint.GREATER_EQUAL:
            return p1_d >= p2_d
        elif self._comparative == ComparativePitchConstraint.GREATER_THAN:
            return p1_d > p2_d
        else:
            raise Exception('Unknown comparative value {0}.'.format(self.comparative))

    def values(self, p_map, v_note):
        """
        Compute possible values for v_note's target.
        :param p_map: note-->contextual_note
        :param v_note: Note
        :return: Candidate Notes.

        Note: Here is why the intervals are reversed for solving for note_one:
              Suppose x --> [x-a, x + b].  Then for some value y, 
              for t with y-b<=t<=y+a, we have t -->[t-a, t+b], but
              from the inequalities, t-a<=y<t+b - so the reverse map is
              [y-b, y+a] <-- y, which is exactly what happens below.
        """
        if v_note == self.note_two:
            source = self.note_one
            target = self.note_two
            comparative = self.comparative
        elif v_note == self.note_one:
            source = self.note_two
            target = self.note_one
            comparative = 4 - self.comparative
        else:
            raise Exception('v_note specification does not match any v_note in constraints.')

        if p_map[target].note is not None:
            return {p_map[target].note}

        if p_map[source].note is None:
            answer_range = p_map[target].policy_context.pitch_range
            source_pitch = None
        else:
            # Establish a pitch range commensurate with comparative.
            qrange = p_map[target].policy_context.pitch_range
            source_pitch = p_map[source].note.diatonic_pitch

            if comparative > 2:
                answer_range = PitchRange(qrange.start_index, source_pitch.chromatic_distance)
            elif comparative < 2:
                answer_range = PitchRange(source_pitch.chromatic_distance, qrange.end_index)
            else:
                answer_range = PitchRange(source_pitch.chromatic_distance, source_pitch.chromatic_distance)

        pitches = PitchScale.compute_tonal_pitches(p_map[target].policy_context.harmonic_context.tonality,
                                                   answer_range)
        if comparative == 4 and len(pitches) > 0 and source_pitch is not None and \
                source_pitch.chromatic_distance == pitches[-1].chromatic_distance:
            pitches.pop(-1)
        if comparative == 0 and len(pitches) > 0 and source_pitch is not None and \
                source_pitch.chromatic_distance == pitches[0].chromatic_distance:
            del pitches[0]

        answer = OrderedSet()
        for pitch in pitches:
            answer.add(Note(pitch, target.base_duration, target.num_dots))
        return answer

