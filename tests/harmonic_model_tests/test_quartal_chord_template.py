import unittest
from harmonicmodel.quartal_chord_template import QuartalChordTemplate

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone


class TestQuartalChordTemplate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_triads(self):
        print 'test_simple_triads'
        ltrs = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        answers = ['C, F, B PerAug',
                   'D, G, C PerPer',
                   'E, A, D PerPer',
                   'F, B, E AugPer',
                   'G, C, F PerPer',
                   'A, D, G PerPer',
                   'B, E, A PerPer',
                   ]
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        i = 1
        for t, a in zip(ltrs, answers):
            chord_t = QuartalChordTemplate.parse('q' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s
            assert s == a, '{0} != {1}'.format(s, answers[i - 1])
            
            i += 1
            
        print '-----'    
        ltrs = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        i = 1
        for t, a in zip(ltrs, answers):
            chord_t = QuartalChordTemplate.parse('q' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s
            assert s == a, '{0} != {1}'.format(s, answers[i - 1])
            
            i += 1

        tones = {Tonality(ModalityType.Major, DiatonicTone("C")): (['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                                                                   ['A, D, G PerPer', 'B, E, A PerPer',
                                                                    'C, F, B PerAug', 'D, G, C PerPer',
                                                                    'E, A, D PerPer', 'F, B, E AugPer',
                                                                    'G, C, F PerPer']),
                 Tonality(ModalityType.Major, DiatonicTone("Db")): (['ab', 'bb',  'db', 'eb', 'gb'],
                                                                    ['Ab, Db, Gb PerPer', 'Bb, Eb, Ab PerPer',
                                                                     'Db, Gb, C PerAug', 'Eb, Ab, Db PerPer',
                                                                     'Gb, C, F AugPer']),
                 Tonality(ModalityType.Major, DiatonicTone("B")):
                     (['a#', 'c#', 'd#', 'f#', 'g#'], ['A#, D#, G# PerPer', 'C#, F#, B PerPer',
                                                       'D#, G#, C# PerPer', 'F#, B, E PerPer', 'G#, C#, F# PerPer']),
                 Tonality(ModalityType.MelodicMinor, DiatonicTone("Ab")): (['Cb'], ['Cb, F, Bb AugPer']),
                 Tonality(ModalityType.Major, DiatonicTone("C#")): (['B#'], ['B#, E#, A# PerPer'])}
        for tonality, tone_ltrs_answers in tones.iteritems():
            for t, a in zip(tone_ltrs_answers[0], tone_ltrs_answers[1]):
                chord_t = QuartalChordTemplate.parse('q' + t)
                print chord_t
                tone = chord_t.diatonic_basis
                cap_t = t[0:1].upper() + (t[1:2] if len(t) == 2 else '')
                assert cap_t == tone.diatonic_symbol
            
                chord = chord_t.create_chord(tonality)
                tones = chord.tones
                s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
                print s
                assert s == a, '{0} != {1}'.format(s, a)
                
    def test_special_chords(self):
        print 'test_special_chords'
        triads = ['PerPer', 'AugPer', 'PerAug']
        answers = ['C, F, Bb PerPer', 'C, F#, B AugPer', 'C, F, B PerAug']
        tonality = Tonality(ModalityType.Major, DiatonicTone("C"))  
        for triad, a in zip(triads, answers):
            chord_t = QuartalChordTemplate.parse('qC' + triad)
            print chord_t
            chord = chord_t.create_chord(tonality)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s  
            assert s == a, '{0} != {1}'.format(s, a)
        
        answers = ['A, D, G PerPer', 'A, D#, G# AugPer', 'A, D, G# PerAug']    
        for triad, a in zip(triads, answers):
            chord_t = QuartalChordTemplate.parse('qvi' + triad)
            print chord_t
            chord = chord_t.create_chord(tonality)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s  
            assert s == a, '{0} != {1}'.format(s, a)
            
    def test_pa_4_chords(self):
        print 'test_pa_4_chords'
        chord_types = ['PPP', 'PPA', 'PAP', 'PAA', 'APP', 'APA', 'AAP', 'AAA']
        answers = ['C, F, Bb, Eb PPP', 'C, F, Bb, E PPA', 'C, F, B, E PAP', 'C, F, B, E# PAA', 'C, F#, B, E APP',
                   'C, F#, B, E# APA', 'C, F#, B#, E# AAP', 'C, F#, B#, E## AAA']
        tonality = Tonality(ModalityType.Major, DiatonicTone("C"))  
        for triad, a in zip(chord_types, answers):
            chord_t = QuartalChordTemplate.parse('qC' + triad)
            print chord_t
            chord = chord_t.create_chord(tonality)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s  
            assert s == a, '{0} != {1}'.format(s, a) 
            
    def test_inversion(self):
        print 'test_inversion'
        ctype = 'PPPP'
        answers = ['C, F, Bb, Eb, Ab PPPP', 'F, C, Bb, Eb, Ab PPPP', 'Bb, C, F, Eb, Ab PPPP', 'Eb, C, F, Bb, Ab PPPP',
                   'Ab, C, F, Bb, Eb PPPP'
                   ]
        diatonic_tonality = Tonality(ModalityType.Major, DiatonicTone("C"))
        
        for i, a in zip(range(1, 6), answers):
            template = QuartalChordTemplate.parse('qC' + ctype + '@' + str(i))
            chord = template.create_chord(diatonic_tonality)
            print chord
            
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print s  
            assert s == a, '{0} != {1}'.format(s, a) 

if __name__ == "__main__":
    unittest.main()
