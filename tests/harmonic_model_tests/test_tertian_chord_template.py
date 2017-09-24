import unittest
from harmonicmodel.tertian_chord_template import TertianChordTemplate, TertianChordType

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone

import logging


class TestTertianTemplateChord(unittest.TestCase):
    
    logging.basicConfig(level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_chord_parse(self):
        ltrs = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        i = 1
        for t in ltrs:
            chord_t = TertianChordTemplate.parse('t' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            print('{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type))
            
            i += 1
            
        ltrs = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        i = 1
        for t in ltrs:
            chord_t = TertianChordTemplate.parse('T' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            print('{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type))
            
            i += 1
            
        tones = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'ab', 'bb', 'cb', 'db', 'eb', 'fb', 'gb', 'a#', 'b#', 'c#', 'd#',
                 'e#', 'f#', 'g#']
        for t in tones:
            chord_t = TertianChordTemplate.parse(t)
            print(chord_t)
            tone = chord_t.diatonic_basis
            cap_t = t[0:1].upper() + (t[1:2] if len(t) == 2 else '')
            assert cap_t == tone.diatonic_symbol
            
        torsions = ['+9+b11', '+2', '+b2', '+#2']
        for t in torsions:
            template = TertianChordTemplate.parse('TIII' + t)
            print(template)
            
        template = TertianChordTemplate.parse('IVMaj7+b9@3')
        assert template
        print(template)
        assert template.inversion == 3
        
    def test_stationary_diatonic_tone_chords(self):
        ltr = 'A'
        answers = {'Maj': ['A', 'C#', 'E'],
                   'MajSus2': ['A', 'B', 'E'],
                   'MajSus4': ['A', 'D', 'E'],
                   'MajSus': ['A', 'D', 'E'],
                   'Min': ['A', 'C', 'E'],
                   'Dim': ['A', 'C', 'Eb'],
                   'Aug': ['A', 'C#', 'E#'],
                   'Maj7': ['A', 'C#', 'E', 'G#'],
                   'Maj7Sus2': ['A', 'B', 'E', 'G#'],
                   'Maj7Sus4': ['A', 'D', 'E', 'G#'],
                   'Maj7Sus': ['A', 'D', 'E', 'G#'],
                   'Min7': ['A', 'C', 'E', 'G'],
                   'Dom7': ['A', 'C#', 'E', 'G'],
                   'Dom7Sus2': ['A', 'B', 'E', 'G'],
                   'Dom7Sus4': ['A', 'D', 'E', 'G'],
                   'Dom7Sus': ['A', 'D', 'E', 'G'],
                   'Dim7': ['A', 'C', 'Eb', 'Gb'],
                   'HalfDim7': ['A', 'C', 'Eb', 'G'],
                   'MinMaj7': ['A', 'C', 'E', 'G#'],
                   'AugMaj7': ['A', 'C#', 'E#', 'G#'],
                   'Aug7': ['A', 'C#', 'E#', 'G'],
                   'DimMaj7': ['A', 'C', 'Eb', 'G#'],
                   'Dom7Flat5': ['A', 'C#', 'Eb', 'G'],
                   'Maj6': ['A', 'C#', 'E', 'F#'],
                   'Min6': ['A', 'C', 'E', 'F#'],
                   'Fr': ['F##', 'A', 'B', 'D#'],
                   'Ger': ['F##', 'A', 'C', 'D#'],
                   'It': ['F##', 'A', 'D#'],
                   'N6': ['F', 'Bb', 'D'],
                   }
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
 
        for ctype, value in list(answers.items()):
            template = TertianChordTemplate.parse(ltr + ctype)
            chord = template.create_chord(diatonic_tonality)
        
            tones = chord.tones
            print(', '.join(tone[0].diatonic_symbol for tone in tones))
            assert TestTertianTemplateChord.verify(tones, value), 'Fail #{0}, {1}'.format(
                ctype, ', '.join(tone[0].diatonic_symbol for tone in tones))
            
    def test_scale_degree_with_chord_spec(self):
        scale_degree = 'VI'
        answers = {'Maj': ['A', 'C#', 'E'],
                   'MajSus2': ['A', 'B', 'E'],
                   'MajSus4': ['A', 'D', 'E'],
                   'MajSus': ['A', 'D', 'E'],
                   'Min': ['A', 'C', 'E'],
                   'Dim': ['A', 'C', 'Eb'],
                   'Aug': ['A', 'C#', 'E#'],
                   'Maj7': ['A', 'C#', 'E', 'G#'],
                   'Maj7Sus2': ['A', 'B', 'E', 'G#'],
                   'Maj7Sus4': ['A', 'D', 'E', 'G#'],
                   'Maj7Sus': ['A', 'D', 'E', 'G#'],
                   'Min7': ['A', 'C', 'E', 'G'],
                   'Dom7': ['A', 'C#', 'E', 'G'],
                   'Dom7Sus2': ['A', 'B', 'E', 'G'],
                   'Dom7Sus4': ['A', 'D', 'E', 'G'],
                   'Dom7Sus': ['A', 'D', 'E', 'G'],
                   'Dim7': ['A', 'C', 'Eb', 'Gb'],
                   'HalfDim7': ['A', 'C', 'Eb', 'G'],
                   'MinMaj7': ['A', 'C', 'E', 'G#'],
                   'AugMaj7': ['A', 'C#', 'E#', 'G#'],
                   'Aug7': ['A', 'C#', 'E#', 'G'],
                   'DimMaj7': ['A', 'C', 'Eb', 'G#'],
                   'Dom7Flat5': ['A', 'C#', 'Eb', 'G'],
                   'Maj6': ['A', 'C#', 'E', 'F#'],
                   'Min6': ['A', 'C', 'E', 'F#'],
                   'Fr': ['F##', 'A', 'B', 'D#'],
                   'Ger': ['F##', 'A', 'C', 'D#'],
                   'It': ['F##', 'A', 'D#'],
                   'N6': ['F', 'Bb', 'D'],
                   }
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
 
        for ctype, value in list(answers.items()):
            template = TertianChordTemplate.parse(scale_degree + ctype)
            chord = template.create_chord(diatonic_tonality)
        
            tones = chord.tones
            print(', '.join(tone[0].diatonic_symbol for tone in tones))
            assert TestTertianTemplateChord.verify(tones, value), \
                'Fail #{0}, {1}'.format(scale_degree + ctype, ', '.join(tone[0].diatonic_symbol for tone in tones))
            
    def test_inversion(self):
        ctype = 'ADom7'
        chords = {1: ['A', 'C#', 'E', 'G'],
                  2: ['C#', 'A', 'E', 'G'],
                  3: ['E', 'A', 'C#', 'G'],
                  4: ['G', 'A', 'C#', 'E']}
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        
        for i in range(1, 5):
            template = TertianChordTemplate.parse(ctype + '@' + str(i))
            chord = template.create_chord(diatonic_tonality)
            
            tones = chord.tones
            print(', '.join(tone[0].diatonic_symbol for tone in tones))
            assert TestTertianTemplateChord.verify(tones, chords[i]), \
                'Fail #{0}, {1}'.format(ctype + '@' + str(i), ', '.join(tone[0].diatonic_symbol for tone in tones))
            
    def test_tensions(self):
        c_type = 'DbDom7'
        
        answers = {'+9': ['Db', 'F', 'Ab', 'Cb', 'Eb'],
                   '+b9': ['Db', 'F', 'Ab', 'Cb', 'Ebb'],
                   '+#9': ['Db', 'F', 'Ab', 'Cb', 'E'],
                   '+bb9': ['Db', 'F', 'Ab', 'Cb', 'Ebbb'],
                   '+9+11+13': ['Db', 'F', 'Ab', 'Cb', 'Eb', 'Gb', 'Bb'],
                   '+b9+#13': ['Db', 'F', 'Ab', 'Cb', 'Ebb', 'B'],
                   '+6': ['Db', 'F', 'Ab', 'Cb', 'Bb'],
                   '+8': ['Db', 'F', 'Ab', 'Cb', 'Db'],
                   }
        
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("Db"))
        for t, value in list(answers.items()):
            template = TertianChordTemplate.parse(c_type + t)
            chord = template.create_chord(diatonic_tonality)
        
            tones = chord.tones
            print(', '.join(tone[0].diatonic_symbol for tone in tones))
            assert TestTertianTemplateChord.verify(tones, value), \
                'Fail #{0}, {1}'.format(c_type + '+' + t, ', '.join(tone[0].diatonic_symbol for tone in tones))
            
    def test_duplicate(self):
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("Db"))
        template = TertianChordTemplate.parse('DbDom7+8')
        chord = template.create_chord(diatonic_tonality)
        print(chord)
        
        tones = chord.tones
        print(', '.join(tone[0].diatonic_symbol for tone in tones))
        assert TestTertianTemplateChord.verify(tones,
                                               ['Db', 'F', 'Ab', 'Cb', 'Db']), 'Fail #{0}, {1}'.format(
            'DbDom7+8', ', '.join(tone[0].diatonic_symbol for tone in tones))
        
        template = TertianChordTemplate.parse('DbDom7+8@4')
        chord = template.create_chord(diatonic_tonality)
        tones = chord.tones
        print(', '.join(tone[0].diatonic_symbol for tone in tones))
        assert TestTertianTemplateChord.verify(tones, ['Cb', 'Db', 'F', 'Ab', 'Db']), \
            'Fail #{0}, {1}'.format('DbDom7+8', ', '.join(tone[0].diatonic_symbol for tone in tones))
        
        tones = chord.sorted_tones()
        print(', '.join(tone[0].diatonic_symbol for tone in tones))
        assert TestTertianTemplateChord.verify(tones, ['Db', 'F', 'Ab', 'Cb', 'Db']), \
            'Fail #{0}, {1}'.format('DbDom7+8', ', '.join(tone[0].diatonic_symbol for tone in tones))

    def test_triad_generation(self):
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        ret_types = [TertianChordType.Maj, TertianChordType.Min, TertianChordType.Min, TertianChordType.Maj,
                     TertianChordType.Maj,
                     TertianChordType.Min, TertianChordType.Dim]
        for i in range(1, 8):
            chord = TertianChordTemplate.get_triad(diatonic_tonality, i)       
            print(chord)
            assert chord.chord_type.value == ret_types[i - 1]
            
    @staticmethod
    def verify(tones, answer):
        if len(tones) != len(answer):
            return False
        for i in range(0, len(tones)):
            if tones[i][0].diatonic_symbol != answer[i]:
                return False
        return True

if __name__ == "__main__":
    unittest.main()
