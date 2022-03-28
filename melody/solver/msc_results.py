"""

File: msc_results.py

Purpose: Maintains results from MelodicConstraintSolver.solve().

"""


class MCSResults(object):

    def __init__(self, line, tempo_event_sequence, ts_event_sequence, hct, beat_results, pitch_results):
        """
        Constructor.
        :param line: Line
        :param tempo_event_sequence: TempoEventSequence
        :param ts_event_sequence: EventSequence fo TimeSignatureEvents
        :param hct: HarmonicContextTrack
        :param beat_results: List of PositionDeltaInfo's
        :param pitch_results: List of PMap's
        """
        self.__line = line
        self.__tempo_event_sequence = tempo_event_sequence
        self.__ts_event_sequence = ts_event_sequence
        self.__hct = hct

        self.__beat_results = beat_results
        self.__pitch_results = pitch_results

    @property
    def line(self):
        return self.__line

    @property
    def tempo_event_sequence(self):
        return self.__tempo_event_sequence

    @property
    def ts_event_sequence(self):
        return self.__ts_event_sequence

    @property
    def beat_results(self):
        return self.__beat_results

    @property
    def pitch_results(self):
        return self.__pitch_results

    def apply(self, beat_result=None, pitch_result=None, line_copy=True):
        """
        Produce a line based on a PositionDeltaInfo and a PMap, and specify if applied to original line or copy.
        :param beat_result: PositionDeltaInfo
        :param pitch_result: PMap
        :param line_copy: True means to copy original line and administer the constraint solutions chosen
        :return: Line
        """
        if beat_result is not None and beat_result not in self.beat_results:
            raise Exception('Given beat result not a member of beat results.')
        if pitch_result is not None and pitch_result not in self.pitch_results:
            raise Exception('Given pitch result not a member of pitch results.')

        beat_line = beat_result.apply(line_copy) if beat_result is not None else None
        pitch_line = pitch_result.apply(self.line, line_copy) if pitch_result is not None else None

        if beat_line is None:
            return pitch_line
        if pitch_line is None:
            return beat_line

        if beat_line != pitch_line:
            note_map = {a: b for a, b in zip(pitch_line.get_all_notes(), beat_line.get_all_notes())} \
                       if pitch_line != self.line else None

            for pitch_note in pitch_line.get_all_notes():
                beat_note = note_map[pitch_note]
                beat_note.diatonic_pitch = pitch_note.diatonic_pitch

        return beat_line
