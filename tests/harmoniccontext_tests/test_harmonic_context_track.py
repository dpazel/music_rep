import unittest
from harmoniccontext.harmonic_context_track import HarmonicContextTrack
from harmoniccontext.harmonic_context import HarmonicContext
from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone
from harmonicmodel.tertian_chord_template import TertianChordTemplate
from timemodel.duration import Duration
from timemodel.position import Position

import logging


class TestInterval(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_append(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))

        assert len(hc_track) == 3
        assert hc_track[Position(0)].duration == Duration(1, 2)
        assert hc_track[Position(1, 2)].duration == Duration(1, 4)
        assert hc_track[Position(3, 4)].duration == Duration(1, 3)

    def test_append_first(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append_first(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append_first(HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))
        hc_track.append_first(HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))

        assert len(hc_track) == 3
        assert hc_track[Position(0)].duration == Duration(1, 3)
        assert hc_track[Position(1, 3)].duration == Duration(1, 4)
        assert hc_track[Position(7, 12)].duration == Duration(1, 2)

    def test_insert(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))
        hc_track.insert(Position(1, 2), HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))

        assert len(hc_track) == 3
        assert hc_track[Position(0)].duration == Duration(1, 2)
        assert hc_track[Position(1, 2)].duration == Duration(1, 4)
        assert hc_track[Position(3, 4)].duration == Duration(1, 3)

        hc_track = HarmonicContextTrack()
        hc_track.insert(Position(0), HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))
        hc_track.insert(Position(0), HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))
        hc_track.insert(Position(0), HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))

        assert len(hc_track) == 3
        assert hc_track[Position(0)].duration == Duration(1, 2)
        assert hc_track[Position(1, 2)].duration == Duration(1, 3)
        assert hc_track[Position(5, 6)].duration == Duration(1, 4)

        assert len(hc_track) == 3

    def test_replace(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))

        hc_track.replace(Position(1, 2), HarmonicContext(diatonic_tonality, chord, Duration(1, 8)))

        assert len(hc_track) == 3
        assert hc_track.duration == Duration(23, 24)  # 1/2 + 1/8 + 1/3
        assert hc_track[Position(0)].duration == Duration(1, 2)
        assert hc_track[Position(1, 2)].duration == Duration(1, 8)
        assert hc_track[Position(5, 8)].duration == Duration(1, 3)

    def test_remove(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        chord_t = TertianChordTemplate.parse('tIV')
        chord = chord_t.create_chord(diatonic_tonality)

        hc_track = HarmonicContextTrack()
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 2)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 4)))
        hc_track.append(HarmonicContext(diatonic_tonality, chord, Duration(1, 3)))

        remove_item = hc_track[Position(1, 2)]
        hc_track.remove(remove_item)

        assert len(hc_track) == 2
        assert hc_track[Position(0)].duration == Duration(1, 2)
        assert hc_track[Position(1, 2)].duration == Duration(1, 3)


if __name__ == "__main__":
    unittest.main()
