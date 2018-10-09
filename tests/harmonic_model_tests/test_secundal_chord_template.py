import unittest
from harmonicmodel.secundal_chord_template import SecundalChordTemplate

from tonalmodel.modality import ModalityType
from tonalmodel.tonality import Tonality
from tonalmodel.diatonic_tone import DiatonicTone


class TestSecundalChordTemplate(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_triads(self):
        print('test_simple_triads')
        ltrs = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        answers = ['C, D, E MajMaj',
                   'D, E, F MajMin',
                   'E, F, G MinMaj',
                   'F, G, A MajMaj',
                   'G, A, B MajMaj',
                   'A, B, C MajMin',
                   'B, C, D MinMaj',
                   ]
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        i = 1
        for t in ltrs:
            chord_t = SecundalChordTemplate.parse('s' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == answers[i - 1], '{0} != {1}'.format(s, answers[i - 1])
            
            i += 1
        
        print('-----')
        ltrs = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        i = 1
        for t in ltrs:
            chord_t = SecundalChordTemplate.parse('s' + t)
            assert chord_t.scale_degree == i, '{0} vs {1}'.format(chord_t.scale_degree, i)
            
            chord = chord_t.create_chord(diatonic_tonality)
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == answers[i - 1], '{0} != {1}'.format(s, answers[i - 1])
            
            i += 1
            
        tones = {Tonality.create(ModalityType.Major, DiatonicTone("C")): (['a', 'b', 'c', 'd', 'e', 'f', 'g'],
                                                                   ['A, B, C MajMin', 'B, C, D MinMaj',
                                                                    'C, D, E MajMaj', 'D, E, F MajMin',
                                                                    'E, F, G MinMaj', 'F, G, A MajMaj',
                                                                    'G, A, B MajMaj']),
                 Tonality.create(ModalityType.Major, DiatonicTone("Db")):
                     (['ab', 'bb',  'db', 'eb', 'gb'],
                      ['Ab, Bb, C MajMaj', 'Bb, C, Db MajMin', 'Db, Eb, F MajMaj', 'Eb, F, Gb MajMin',
                       'Gb, Ab, Bb MajMaj']),
                 Tonality.create(ModalityType.Major, DiatonicTone("B")):
                     (['a#', 'c#', 'd#', 'f#', 'g#'], ['A#, B, C# MinMaj', 'C#, D#, E MajMin', 'D#, E, F# MinMaj',
                                                       'F#, G#, A# MajMaj', 'G#, A#, B MajMin']),
                 Tonality.create(ModalityType.MelodicMinor, DiatonicTone("Ab")): (['Cb'], ['Cb, Db, Eb MajMaj']),
                 Tonality.create(ModalityType.Major, DiatonicTone("C#")): (['B#'], ['B#, C#, D# MinMaj'])}
        for tonality, tone_ltrs_answers in list(tones.items()):
            for t, a in zip(tone_ltrs_answers[0], tone_ltrs_answers[1]):
                chord_t = SecundalChordTemplate.parse('s' + t)
                print(chord_t)
                tone = chord_t.diatonic_basis
                cap_t = t[0:1].upper() + (t[1:2] if len(t) == 2 else '')
                assert cap_t == tone.diatonic_symbol
            
                chord = chord_t.create_chord(tonality)
                tones = chord.tones
                s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
                print(s)
                assert s == a, '{0} != {1}'.format(s, a)
                
    def test_special_chords(self):
        print('test_special_chords')
        triads = ['MajMaj', 'MajMin', 'MinMaj', 'MinMin']
        answers = ['C, D, E MajMaj', 'C, D, Eb MajMin', 'C, Db, Eb MinMaj', 'C, Db, Ebb MinMin']
        tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        for triad, a in zip(triads, answers):
            chord_t = SecundalChordTemplate.parse('SC' + triad)
            print(chord_t)
            chord = chord_t.create_chord(tonality)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == a, '{0} != {1}'.format(s, a)
        
        answers = ['A, B, C# MajMaj', 'A, B, C MajMin', 'A, Bb, C MinMaj', 'A, Bb, Cb MinMin']    
        for triad, a in zip(triads, answers):
            chord_t = SecundalChordTemplate.parse('Svi' + triad)
            print(chord_t)
            chord = chord_t.create_chord(tonality)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == a, '{0} != {1}'.format(s, a)
            
    def test_Mm_4_chords(self):
        print('test_Mm_4_chords')
        chord_types = ['MMM', 'MMm', 'MmM', 'Mmm', 'mMM', 'mMm', 'mmM', 'mmm']
        answers = ['C, D, E, F# MMM', 'C, D, E, F MMm', 'C, D, Eb, F MmM', 'C, D, Eb, Fb Mmm', 'C, Db, Eb, F mMM',
                   'C, Db, Eb, Fb mMm', 'C, Db, Ebb, Fb mmM', 'C, Db, Ebb, Fbb mmm']
        tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        for triad, a in zip(chord_types, answers):
            chord_t = SecundalChordTemplate.parse('SC' + triad)
            print(chord_t)
            chord = chord_t.create_chord(tonality)
            print(chord)
            tones = chord.tones    
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == a, '{0} != {1}'.format(s, a)           
            
    def test_inversion(self):
        print('test_inversion')
        ctype = 'MMM'
        answers = ['C, D, E, F# MMM', 'D, C, E, F# MMM', 'E, C, D, F# MMM', 'F#, C, D, E MMM'
                   ]
        diatonic_tonality = Tonality.create(ModalityType.Major, DiatonicTone("C"))
        
        for i, a in zip(range(1, 5), answers):
            template = SecundalChordTemplate.parse('SC' + ctype + '@' + str(i))
            chord = template.create_chord(diatonic_tonality)
            
            tones = chord.tones
            s = '{0} {1}'.format(', '.join(tone[0].diatonic_symbol for tone in tones), chord.chord_type)
            print(s)
            assert s == a, '{0} != {1}'.format(s, a)
            

if __name__ == "__main__":
    unittest.main()
