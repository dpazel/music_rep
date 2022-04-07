"""

File: t_retrograde.py

Purpose: Transform to reverse a melody (and harmony).

"""
from transformation.harmonictranscription.t_harmonic_transcription import THarmonicTranscription
from transformation.patsub.min_contour_filter import MinContourFilter
from transformation.transformation import Transformation
from fractions import Fraction
from misc.interval import Interval as NumericInterval
from tonalmodel.diatonic_pitch import DiatonicPitch
from structure.note import Note


class TRetrograde(Transformation):
    """
    TRetrograde: Transform to reshape a melody into it reversal, or retrograde. The harmony will be reversed as well,
                 unless otherwise specified.
    """

    def __init__(self, score):
        """
        Constructor.
        :param score: Score containing the melody line to be reversed. (LiteScore)
        """

        self.__score = score
        self.__reverse_harmony = True
        self.__time_interval = None

        Transformation.__init__(self)

    @property
    def score(self):
        return self.__score

    @property
    def reverse_harmony(self):
        return self.__reverse_harmony

    @property
    def time_interval(self):
        return self.__time_interval

    def apply(self, reverse_harmony=True, time_interval=None, transcription=True, results_sample_size=200):
        """
        Extract and reverse a melodic segment of the score.
        :param reverse_harmony: Boolean indicating if harmony should be reversed.
        :param time_interval: Interval (numeric) bounds of the melody to be reversed
        :param transcription: True means apply harmonic transcription, only whenever_harmony==False.
        :param results_sample_size: Number of results from which to generate a best.
        :return: reversed line, hct
        Note: if reverse_harmony is False, a Harmonic Transcription is applied to the line.
        Note: as to assist when reverse_harmony is False, we make 2 optimization on harmonic transcription:
              1) We take the first note to the closest chord tone.
              2) We increase the height by 6 tones (half octave)
        """
        from tonalmodel.interval import Interval, IntervalType

        self.__reverse_harmony = reverse_harmony
        self.__time_interval = time_interval if time_interval is not None else \
            NumericInterval(Fraction(0), self.score.line.duration.duration)

        reduced_line, first_position, duration = self.score.line.sub_line(self.time_interval)
        reduced_reversed_line = reduced_line.clone()
        reduced_reversed_line.reverse()

        reduced_hct = self.score.hct.sub_hct(NumericInterval(first_position.position,
                                                             first_position.position + duration.duration))

        reduced_reversed_hct = reduced_hct.reverse()

        # If reversing harmony OR if reversing harmony and not doing transposition
        # These cases do not require transcription:
        #  a) reverse harmony and no transcription - return reversed line + reversed harmony
        #  b) no reverse harmony and no transcription - return reversed_line + original hct
        #  c) reverse harmony and transcription - return reversed_line and reversed harmony.
        if reverse_harmony or not transcription:
            return reduced_reversed_line, reduced_reversed_hct if reverse_harmony else reduced_hct

        # Case: not reversing harmony AND requiring a transposition
        # Must specify reversed line here, but ANALYZE against reversed_hct, which is the original harmony
        # making the correct analysis of the original melody.
        t_ht = THarmonicTranscription(reduced_reversed_line, reduced_reversed_hct)

        # Find lowest tone:
        notes = reduced_reversed_line.get_all_notes()
        note_index, _ = min(enumerate(notes), key=lambda n: n[1].diatonic_pitch.chromatic_distance)
        lowest_pitch = notes[note_index].diatonic_pitch

        # Adapt reversed melody to original harmony.
        tag_map = gen_tag_map(notes[0], reduced_hct.hc_list()[0])
        results = t_ht.apply(reduced_hct,
                             lowest_pitch,
                             tag_map, t_ht.height + 6, results_sample_size,
                             tunnel_half_interval=Interval(4, IntervalType.Perfect))

        filtered_results = MinContourFilter(reduced_reversed_line, results.pitch_results)
        scored_filtered_results = filtered_results.scored_results

        if len(scored_filtered_results) == 0:
            return None, None

        return scored_filtered_results[0][0], reduced_hct


def duration_ltr(duration):
    if duration.duration == Fraction(1, 16):
        return 's'
    elif duration.duration == Fraction(3, 16):
        return 'i@'
    elif duration.duration == Fraction(1, 8):
        return 'i'
    elif duration.duration == Fraction(3, 8):
        return 'q@'
    elif duration.duration == Fraction(1, 4):
        return 'q'
    elif duration.duration == Fraction(1, 2):
        return 'h'
    elif duration.duration == Fraction(1):
        return 'w'
    return '>'


def str_line(line):
    notes = line.get_all_notes()
    prior_octave = None
    prior_duration = None
    note_annotations = list()
    for note in notes:
        annotation = ''
        d = duration_ltr(note.duration)
        if d != prior_duration:
            annotation += d
            prior_duration = d
        annotation += str(note.diatonic_pitch.diatonic_tone.diatonic_symbol) if note.diatonic_pitch is not None else 'R'
        o = note.diatonic_pitch.octave if note.diatonic_pitch is not None else prior_octave
        if o != prior_octave:
            annotation += ":" + str(o)
            prior_octave = o
        note_annotations.append(annotation)
    s = ' '.join(annotation for annotation in note_annotations)
    return s


def gen_tag_map(note, hc):
    if note.diatonic_pitch is None:
        return None

    octave = note.diatonic_pitch.octave
    octaves = []
    if octave - 1 > 0:
        octaves.append(octave - 1)
    octaves.append(octave)
    if octave + 1 < 8:
        octaves.append(octave + 1)

    chordals = hc.chord.tones

    closest_pitch = None
    dist = 10000
    for tone_info in chordals:
        t = tone_info[0].diatonic_symbol
        for octave in octaves:
            p = DiatonicPitch.parse(t + ':' + str(octave))
            d = abs(p.chromatic_distance - note.diatonic_pitch.chromatic_distance)
            if d < dist:
                dist = d
                closest_pitch = p

    return {0: closest_pitch}
