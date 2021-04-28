import unittest
from harmonicmodel.secondary_chord_template import SecondaryChordTemplate

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone

import logging


class TestSecondaryChordTemplate(unittest.TestCase):

    logging.basicConfig(level=logging.DEBUG)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sample(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        
        template = SecondaryChordTemplate.parse('qVIPPaa/iv[Major]')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'D, G, C, F#, B#'
        
        template = SecondaryChordTemplate.parse('qIIIPPaa/V[MelodicMinor]')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'Bb, Eb, Ab, D, G#'
        
    def test_standards(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("G"))
        
        template = SecondaryChordTemplate.parse('V/ii')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'E, G#, B'  
        
        template = SecondaryChordTemplate.parse('V/IV')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'G, B, D' 
        
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("G"))
        template = SecondaryChordTemplate.parse('V/ii')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'E, G#, B' 
        
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("Bb"))
        template = SecondaryChordTemplate.parse('VI/ii')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'A, C, Eb' 
        
    def test_interesting(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("F"))
        
        template = SecondaryChordTemplate.parse('V/V[NaturalMinor]')
        print(template)
        t_chord = template.create_chord(diatonic_tonality)
        print(t_chord)
        
        s = ', '.join(str(tone[0].diatonic_symbol) for tone in t_chord.tones)
        print(s)
        assert s == 'G, Bb, D'

    def test_book_examples(self):
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("A"))

        template = SecondaryChordTemplate.parse('V/V')
        if template:
            print('succeeded')
            chord = template.create_chord(diatonic_tonality)
            print(chord)
        else:
            print("failed")

        template = SecondaryChordTemplate.parse('III/II')
        chord = template.create_chord(diatonic_tonality)
        print(chord)

        template = SecondaryChordTemplate.parse('CMaj7/II')
        chord = template.create_chord(diatonic_tonality)
        print(chord)

        template = SecondaryChordTemplate.parse('V/V[NaturalMinor]')
        chord = template.create_chord(diatonic_tonality)
        print(chord)

        template = SecondaryChordTemplate.parse('V/V[Phrygian]')
        chord = template.create_chord(diatonic_tonality)
        print(chord)

        template = SecondaryChordTemplate.parse('QVIPPAP@2/V')
        chord = template.create_chord(diatonic_tonality)
        print(chord)



if __name__ == "__main__":
    unittest.main()
