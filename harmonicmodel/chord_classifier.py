"""
File: chrod_classifier.py

Purpose: Utility class to determine the chord given a set of tones and/or tonality.

"""
from tonalmodel.diatonic_tone_cache import DiatonicToneCache
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.interval import Interval
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType
from harmonicmodel.quartal_chord_template import QuartalChordTemplate, QuartalChordType
from harmonicmodel.secundal_chord_template import SecundalChordTemplate, SecundalChordType
from harmonicmodel.tertian_chord import TertianChord
from harmonicmodel.quartal_chord import QuartalChord
from harmonicmodel.secundal_chord import SecundalChord


class ChordClassifier(object):
    """
    Utility class to determine chord type from a set of tones and/or tonality.
    """

    def __init__(self, tones, root_tone, tonality=None):
        """
        Constructor.
        :param tones: (textusl) set of tones of which chord is comprised.
        :param root_tone: The root tone of chord, must be in tones.
        :param tonality: Tonality behind chord. If set, used to get chord diatonic index.
        """
        self._chord_tones = ChordClassifier.to_tones(tones)
        self._root_tone = DiatonicToneCache.get_tone(root_tone) if isinstance(root_tone, str) else root_tone
        self._tonality = tonality

        if self._root_tone is not None and self._root_tone not in self.chord_tones:
            raise Exception('Root tone \'{0}\' not in tones arguments \'[{1}]\'.'.format(
                self._root_tone, ', '.join(str(v.diatonic_symbol) for v in self.chord_tones)))

    def classify_tones_as_chord(self):
        chords = self.find_tertian_chords()
        chords.extend(self.find_quartal_chords())
        chords.extend(self.find_secundal_chords())
        return chords

    def classify_tones_as_chord_all_roots(self):
        chords = list()
        for tone in self.chord_tones:
            self._root_tone = tone
            chords.extend(self.classify_tones_as_chord())
        return chords

    @property
    def chord_tones(self):
        return self._chord_tones

    @property
    def root_tone(self):
        return self._root_tone

    @property
    def tonality(self):
        return self._tonality

    @staticmethod
    def classify(tones, root_tone, tonality=None):
        """
        Classify tones for chords, ala root over a tonality.
        :param tones:
        :param root_tone:
        :param tonality:
        :return:
        """
        return ChordClassifier(tones, root_tone, tonality).classify_tones_as_chord()

    @staticmethod
    def classify_all_roots(tones, tonality=None):
        """
        Classify tones for chords, wherein any tone can be a root.
        :param tones:
        :param tonality:
        :return:
        """
        return ChordClassifier(tones, None, tonality).classify_tones_as_chord_all_roots()

    @staticmethod
    def to_tones(tone_list):
        r = list()
        for t in tone_list:
            r.append(DiatonicToneCache.get_tone(t) if isinstance(t, str) else t)
        return r

    def find_tertian_chords(self):
        results = list()
        for chord_type, interval_list in TertianChordTemplate.TERTIAN_CHORD_TYPE_MAP.items():
            chord_tones = list()
            for interval in interval_list:
                chord_tones.append(interval.get_end_tone(self.root_tone))
            if set(chord_tones) <= set(self.chord_tones):
                if self.chord_tones[0] not in chord_tones:
                    continue
                ct = TertianChordType(chord_type)
                results.append((ct, chord_tones))

        results.sort(key=lambda x: len(x[1]), reverse=True)
        rr = [x for x in results if len(x[1]) == len(results[0][1])]
        chords = list()
        if len(rr):
            for answer in rr:
                # inversion computed - must be a chordal tone
                # if self.chord_tones[0] not in answer[1]:
                #    raise Exception('Inversion tone \'{0}\' must be a chord tone in [{1}]'.format(
                #        self.chord_tones[0], ', '.join(v.diatonic_symbol for v in answer[1])))
                inversion = answer[1].index(self.chord_tones[0]) + 1
                tensions = list()
                remainder = set(self.chord_tones) - set(answer[1])
                for r in remainder:
                    p1 = DiatonicPitch(4, self.root_tone)
                    p2 = DiatonicPitch(5 if DiatonicPitch.crosses_c(self.root_tone, r) else 4, r)
                    interval = Interval.create_interval(p1, p2)
                    if interval.diatonic_distance < 5:  # We don't want M:13 nor M:14
                        interval = Interval(interval.diatonic_distance + 8, interval.interval_type)
                    tensions.append(interval)

                if self.tonality is not None:
                    index = self.tonality.annotation.index(self.root_tone) \
                        if self.root_tone in self.tonality.annotation else None
                    if index is None:
                        continue
                        # raise Exception('Root tone {0} is not in tonality {1}'.format(self.root_tone, self.tonality))
                    template = TertianChordTemplate(None, index + 1, answer[0], tensions, inversion)
                else:
                    template = TertianChordTemplate(self.root_tone, None, answer[0], tensions, inversion)
                chords.append(TertianChord(template, self.tonality))

        return chords

    def find_quartal_chords(self):
        results = list()
        for chord_type, interval_list in QuartalChordTemplate.QUARTAL_CHORD_TYPE_MAP.items():
            chord_tones = list()
            last_tone = self.root_tone
            for interval in interval_list:
                chord_tones.append(interval.get_end_tone(last_tone))
                last_tone = chord_tones[-1]
            if set(chord_tones) <= set(self.chord_tones):
                qt = QuartalChordType(chord_type)
                results.append((qt, list(chord_tones)))

        results.sort(key=lambda x: len(x[1]), reverse=True)
        rr = [x for x in results if len(x[1]) == len(results[0][1])]
        chords = list()
        if len(rr):
            for answer in rr:
                remainder = set(self.chord_tones) - set(answer[1])
                if len(remainder) > 0:
                    #  Tensions not supported in quartal chords
                    continue
                # inversion computed - must be a chordal tone
                inversion = answer[1].index(self.chord_tones[0]) + 1
                if self.tonality is not None:
                    index = self.tonality.annotation.index(self.root_tone) \
                        if self.root_tone in self.tonality.annotation else None
                    if index is None:
                        raise Exception('Root tone {0} is not in tonality {1}'.format(self.root_tone, self.tonality))
                    template = QuartalChordTemplate(None, index + 1, answer[0], list(), inversion)
                else:
                    template = QuartalChordTemplate(self.root_tone, None, answer[0], list(), inversion)
                chords.append(QuartalChord(template, self.tonality))

        return chords

    def find_secundal_chords(self):
        results = list()
        for chord_type, interval_list in SecundalChordTemplate.SECUNDAL_CHORD_TYPE_MAP.items():
            chord_tones = list()
            last_tone = self.root_tone
            for interval in interval_list:
                chord_tones.append(interval.get_end_tone(last_tone))
                last_tone = chord_tones[-1]
            if set(chord_tones) <= set(self.chord_tones):
                qt = SecundalChordType(chord_type)
                results.append((qt, list(chord_tones)))

        results.sort(key=lambda x: len(x[1]), reverse=True)
        rr = [x for x in results if len(x[1]) == len(results[0][1])]
        chords = list()
        if len(rr):
            for answer in rr:
                remainder = set(self.chord_tones) - set(answer[1])
                if len(remainder) > 0:
                    #  Tensions not supported in secundal chords
                    continue
                # inversion computed - must be a chordal tone
                inversion = answer[1].index(self.chord_tones[0]) + 1
                if self.tonality is not None:
                    index = self.tonality.annotation.index(self.root_tone) \
                        if self.root_tone in self.tonality.annotation else None
                    if index is None:
                        raise Exception('Root tone {0} is not in tonality {1}'.format(self.root_tone, self.tonality))
                    template = SecundalChordTemplate(None, index + 1, answer[0], list(), inversion)
                else:
                    template = SecundalChordTemplate(self.root_tone, None, answer[0], list(), inversion)
                chords.append(SecundalChord(template, self.tonality))

        return chords
