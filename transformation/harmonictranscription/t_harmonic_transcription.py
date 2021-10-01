"""

File: t_harmonic_transcription.py

Purpose: Given a line and its hct, and a target hct as long as the prior said given, reproduce the line
         to the new target hct, based on its constraints plus those of the melodic search analysis.

"""
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint
from melody.constraints.comparative_pitch_constraint import ComparativePitchConstraint
from melody.constraints.pitch_range_constraint import PitchRangeConstraint
from melody.solver.melodic_constraint_solver import MelodicConstraintSolver
from search.melodicsearch.melodic_search_analysis import MelodicSearchAnalysis, NotePairInformation
from structure.LineGrammar.core.line_grammar_executor import LineGrammarExecutor
from structure.line import Line
from structure.tempo import Tempo
from structure.time_signature import TimeSignature
from timemodel.duration import Duration
from timemodel.event_sequence import EventSequence
from timemodel.position import Position
from timemodel.tempo_event import TempoEvent
from timemodel.tempo_event_sequence import TempoEventSequence
from timemodel.time_signature_event import TimeSignatureEvent
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.pitch_range import PitchRange
from tonalmodel.interval import Interval, IntervalType
from transformation.transformation import Transformation


class THarmonicTranscription(Transformation):
    """
    THarmonicTranscription: Construct a pattern with similar melodic structure to a source pattern, but given
        a specific hct to follow.
    """

    TUNNEL_HALF_INTERVAL = Interval(5, IntervalType.Perfect)

    def __init__(self, source_line, source_hct, source_melodic_form=None):
        """
        Constructor
        :param source_line: Source line.
        :param source_hct: Source line's hct.
        :param source_melodic_form: MelodicForm for the source line (optional).
        """
        self.__source_line = source_line
        self.__source_hct = source_hct
        self.__source_melodic_form = source_melodic_form

        self.__source_analysis = MelodicSearchAnalysis(self.source_line, self.source_hct)

        min_pitch, max_pitch = THarmonicTranscription.compute_min_max_pitches(self.source_line.get_all_notes())
        self.__height = max_pitch.chromatic_distance - min_pitch.chromatic_distance
        self.__tunnel_half_interval = THarmonicTranscription.TUNNEL_HALF_INTERVAL

        Transformation.__init__(self)

    @staticmethod
    def create(source_expression):
        lge = LineGrammarExecutor()

        source_line, source_hct = lge.parse(source_expression)
        return THarmonicTranscription(source_line, source_hct)

    @property
    def source_line(self):
        return self.__source_line

    @property
    def source_hct(self):
        return self.__source_hct

    @property
    def source_analysis(self):
        return self.__source_analysis

    @property
    def source_melodic_form(self):
        return self.__source_melodic_form

    @property
    def height(self):
        return self.__height

    @property
    def tunnel_half_interval(self):
        return self.__tunnel_half_interval

    def apply(self, target_hct,
              window_anchor_pitch,
              tag_map=None,
              window_height=None,
              num_solutions=-1,
              tunnel_half_interval=Interval(5, IntervalType.Perfect)):
        """
        Apply method for transformation.
        :param target_hct: Target hct for new target line.
        :param window_anchor_pitch: Pitch specifying the lowest pitch for the target line window.
        :param tag_map: map index of source/target note to specified pitch.
        :param window_height: Height of target pitch window (in semi-tones) - use source line height if None specified.
        :param num_solutions: Maximum number of solutions to return, -1 == unbounded.
        :param tunnel_half_interval: half-interval for pitch range on each target tone.
        :return: MCSResults
        """
        if self.source_hct.duration != target_hct.duration:
            raise Exception('Target hct duration {0} does not match source hct duration {1}.'.
                            format(target_hct.duration, self.source_hct.duration))

        window_anchor_pitch = DiatonicPitch.parse(window_anchor_pitch) if isinstance(window_anchor_pitch, str) \
            else window_anchor_pitch

        target_line = self._build_target_line()

        self.__tunnel_half_interval = tunnel_half_interval

        source_notes = self.source_line.get_all_notes()
        target_notes = target_line.get_all_notes()
        source_to_target = {source_note: target_note for source_note, target_note in zip(source_notes, target_notes)}

        constraints = self._build_constraints(source_to_target, tag_map)
        ts_seq, tempo_seq = THarmonicTranscription._build_default_time_sig_tempo()

        height = window_height if window_height else self.height
        pitch_range = PitchRange(window_anchor_pitch.chromatic_distance,
                                 window_anchor_pitch.chromatic_distance + height)

        solver = MelodicConstraintSolver(target_line, tempo_seq, ts_seq, target_hct, pitch_range, constraints)

        initial_map = {target_notes[k]: v for k, v in tag_map.items()} if tag_map else None
        results = solver.solve(initial_map, num_solutions)
        return results

    def _build_target_line(self):
        # Build a target line, all notes C:4 with onsets/durations of original line.
        target_line = Line()
        initial_pitch = DiatonicPitch.parse('C:4')
        source_notes = self.source_line.get_all_notes()
        for note in source_notes:
            t_note = note.clone()
            t_note.diatonic_pitch = initial_pitch
            target_line.append(t_note)

        return target_line

    def _build_constraints(self, source_to_target, tag_map):
        # Constraints:
        #    contour based on pair analysis
        #    chordal if original note is chordal
        #    melodic form constraints
        #    Tunnel: for diatonic notes, a pitch range constraint based on the specified "tunnel" over target notes.
        pair_annotations = self.source_analysis.note_pair_annotation
        note_annotations = self.source_analysis.note_annotation

        constraints = list()

        for pair_annotation in pair_annotations:
            t1 = source_to_target[pair_annotation.first_note]
            t2 = source_to_target[pair_annotation.second_note]
            if pair_annotation.relationship == NotePairInformation.Relationship.LT:
                rel = ComparativePitchConstraint.LESS_THAN
            elif pair_annotation.relationship == NotePairInformation.Relationship.GT:
                rel = ComparativePitchConstraint.GREATER_THAN
            else:
                rel = ComparativePitchConstraint.EQUAL
            constraint = ComparativePitchConstraint(t1, t2, rel)
            constraints.append(constraint)

        for annotation in note_annotations:
            if annotation.is_chordal:
                constraint = ChordalPitchConstraint(source_to_target[annotation.note])
                constraints.append(constraint)

        # Get the constraints off the motifs
        if self.source_melodic_form:
            form_constraints = self.source_melodic_form.constraints
            for c in form_constraints:
                c_prime = c.clone([source_to_target[n] for n in c.actors])
                constraints.append(c_prime)

        tunnel_constraints = self._build_tunnel_constraints(source_to_target, tag_map)
        constraints.extend(tunnel_constraints)

        return constraints

    def _build_tunnel_constraints(self, source_to_target, tag_map):
        if tag_map is None or len(tag_map) == 0:
            return []

        one_id = next(iter(tag_map.keys()))
        source_note = self.source_line.get_all_notes()[one_id]
        target_pitch = tag_map[one_id]

        mvmt_interval = Interval.create_interval(source_note.diatonic_pitch, target_pitch)

        constraints = list()
        note_annotations = self.source_analysis.note_annotation
        for annotation in note_annotations:
            if annotation.note.diatonic_pitch is None:
                continue
            target_note = source_to_target[annotation.note]

            dest_ctr_pitch = mvmt_interval.get_end_pitch(annotation.note.diatonic_pitch)
            low_pitch = self.tunnel_half_interval.get_start_pitch(dest_ctr_pitch)
            high_pitch = self.tunnel_half_interval.get_end_pitch(dest_ctr_pitch)
            p_range = PitchRange.create(low_pitch, high_pitch)

            constraint = PitchRangeConstraint([target_note], p_range)
            constraints.append(constraint)

        return constraints

    @staticmethod
    def _build_default_time_sig_tempo():
        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))
        return ts_seq, tempo_seq

    @staticmethod
    def compute_min_max_pitches(notes):
        min_pitch = None
        max_pitch = None
        for n in notes:
            p = n.diatonic_pitch
            if p is None:
                continue
            min_pitch = p if min_pitch is None else p if p.chromatic_distance < min_pitch.chromatic_distance else \
                min_pitch
            max_pitch = p if max_pitch is None else p if p.chromatic_distance > max_pitch.chromatic_distance else \
                max_pitch

        return min_pitch, max_pitch
