"""

File: t_patsub.py

Purpose: To replace an image of the pattern in a host line, with a substitution, accounting for harmonic changes.

"""
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from melody.constraints.chordal_pitch_constraint import ChordalPitchConstraint
from melody.constraints.comparative_pitch_constraint import ComparativePitchConstraint
from search.melodicsearch.melodic_search_analysis import NotePairInformation
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
from transformation.harmonictranscription.t_harmonic_transcription import THarmonicTranscription
from transformation.patsub.substitution_pattern import SubstitutionPattern
from transformation.transformation import Transformation


class TPatSub(Transformation):
    """
    TPatSub: Construct a target_pattern instance from a SubstitutionPattern and a source_pattern_instance.
    """

    def __init__(self, substitution_pattern):
        """
        Constructor
        :param substitution_pattern: SubstitutionPattern
        """
        self.__substitution_pattern = substitution_pattern

        Transformation.__init__(self)

    @staticmethod
    def create(source_pattern_expr, target_pattern_expr, target_hc_exprs):
        substitution_pattern = SubstitutionPattern.create(source_pattern_expr, target_pattern_expr, target_hc_exprs)
        return TPatSub(substitution_pattern)

    @property
    def substitution_pattern(self):
        return self.__substitution_pattern

    @property
    def target_height(self):
        return self.substitution_pattern.target_height

    def apply(self, source_instance_line, source_instance_hct, window_anchor_pitch, tag_map=None,
              window_height=None, num_solutions=-1):
        """
        Apply for TPatSub.
        :param source_instance_line:
        :param source_instance_hct:
        :param window_anchor_pitch:
        :param tag_map:
        :param window_height:
        :param num_solutions:
        :return:  MCSResults, target hct.
        """
        window_anchor_pitch = DiatonicPitch.parse(window_anchor_pitch) if isinstance(window_anchor_pitch, str) \
            else window_anchor_pitch

        target_hct = self._build_target_hct(source_instance_hct)

        transform = THarmonicTranscription(self.substitution_pattern.target_pattern_line,
                                           self.substitution_pattern.target_pattern_hct,
                                           self.substitution_pattern.target_melodic_form)

        results = transform.apply(target_hct, window_anchor_pitch, tag_map, window_height, num_solutions)

        return results, target_hct

    def _build_target_hct(self, source_instance_hct):
        target_hct = HarmonicContextTrack()

        source_pat_hc_list = source_instance_hct.hc_list()
        target_pat_hc_list = self.substitution_pattern.target_pattern_hct.hc_list()
        for hc_expr, target_pat_hc in zip(self.substitution_pattern.target_hc_exprs, target_pat_hc_list):
            hc = hc_expr.interpret(source_pat_hc_list, target_pat_hc.duration)
            target_hct.append(hc)

        return target_hct

    def _build_target_line(self):
        target_line = Line()
        initial_pitch = DiatonicPitch.parse('C:4')
        source_notes = self.substitution_pattern.target_pattern_line.get_all_notes()
        for note in source_notes:
            t_note = note.clone()
            t_note.diatonic_pitch = initial_pitch
            target_line.append(t_note)

        return target_line

    def _build_constraints(self, pattern_to_target):
        pair_annotations = self.substitution_pattern.target_analysis.note_pair_annotation
        note_annotations = self.substitution_pattern.target_analysis.note_annotation

        constraints = list()

        for pair_annotation in pair_annotations:
            t1 = pattern_to_target[pair_annotation.first_note]
            t2 = pattern_to_target[pair_annotation.second_note]
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
                constraint = ChordalPitchConstraint(pattern_to_target[annotation.note])
                constraints.append(constraint)

        # Get the constraints off the motifs
        if self.substitution_pattern.target_melodic_form:
            form_constraints = self.substitution_pattern.target_melodic_form.constraints
            for c in form_constraints:
                c_prime = c.clone([pattern_to_target[n] for n in c.actors])
                constraints.append(c_prime)

        return constraints

    @staticmethod
    def _build_default_time_sig_tempo():
        tempo_seq = TempoEventSequence()
        ts_seq = EventSequence()
        tempo_seq.add(TempoEvent(Tempo(60, Duration(1, 4)), Position(0)))
        ts_seq.add(TimeSignatureEvent(TimeSignature(3, Duration(1, 4), 'sww'), Position(0)))
        return ts_seq, tempo_seq
