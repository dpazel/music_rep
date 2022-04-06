import unittest

import sys

from tonalmodel.interval import Interval, IntervalException
from tonalmodel.diatonic_pitch import DiatonicPitch
from tonalmodel.interval import IntervalType
from tonalmodel.diatonic_tone import DiatonicTone
from tonalmodel.diatonic_tone_cache import DiatonicToneCache


class TestInterval(unittest.TestCase):
    
    INTERVAL_TYPES = (IntervalType.Diminished,
                      IntervalType.Minor,
                      IntervalType.Major,
                      IntervalType.Perfect,
                      IntervalType.Augmented)
    
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_create_interval(self):
        pitch_a = DiatonicPitch(4, 'C')
        pitch_b = DiatonicPitch(5, 'C')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Perfect)
        assert interval.diatonic_distance == 7
        
        pitch_a = DiatonicPitch(4, 'C')
        pitch_b = DiatonicPitch(5, 'Cb')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Diminished)
        assert interval.diatonic_distance == 7

        pitch_a = DiatonicPitch(4, 'C')
        pitch_b = DiatonicPitch(5, 'Dbb')        
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Diminished)
        assert interval.diatonic_distance == 8
        
        pitch_a = DiatonicPitch(4, 'C')
        pitch_b = DiatonicPitch(5, 'Cb')        
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Diminished)
        assert interval.diatonic_distance == 7
        
        pitch_a = DiatonicPitch(4, 'C')
        pitch_b = DiatonicPitch(4, 'B#')        
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Augmented)
        assert interval.diatonic_distance == 6
        assert not interval.is_negative()

        pitch_a = DiatonicPitch(5, 'C')
        pitch_b = DiatonicPitch(4, 'Bb')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Major)
        assert interval.diatonic_distance == -1
        assert interval.is_negative()
        
        interval = Interval(9, IntervalType(IntervalType.Diminished))
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Diminished)
        assert interval.diatonic_distance == 8
        
        interval = Interval(3, IntervalType(IntervalType.Minor))
        pitch = interval.get_start_pitch(DiatonicPitch(4, 'E'))
        print(pitch)
        assert str(pitch) == 'C#:4'
    
    def test_all_c_same_octave_itervals(self):
        pitches = list('CDEFGAB')
        augs = ('bb', 'b', '',  '#', '##')
        example_count = 0
        exception_items = (1, 2, 5, 10, 15, 16, 20, 21, 25, 30, 35)
        for pitch in pitches:
            for aug in augs:
                example_count += 1
                a = DiatonicPitch(4, 'C')
                b = DiatonicPitch(4, pitch + aug)
                try:
                    interval = Interval.create_interval(a, b)
                    print('({0}): {1}, {2}) --> {3}'.format(example_count, a, b, interval))
                    assert b.diatonic_tone.diatonic_index - a.diatonic_tone.diatonic_index == interval.diatonic_distance
                    assert b.chromatic_distance - a.chromatic_distance == interval.chromatic_distance
                except Exception as e:
                    print('Exception ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e))
                    assert example_count in exception_items, \
                        'ASSERT ERROR ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e)
                    
    def test_all_g_same_octave_itervals(self):
        pitches = list('GABCDEF')
        octaves = [5, 5, 5, 6, 6, 6, 6]
        augs = ('bb', 'b', '',  '#', '##')
        example_count = 0
        exception_items = (1, 2, 5, 10, 15, 16, 20, 21, 25, 30, 31, 35)
        for i in range(0, 7):
            pitch = pitches[i]
            octave = octaves[i]
            for aug in augs:
                example_count += 1
                a = DiatonicPitch(5, 'G')
                b = DiatonicPitch(octave, pitch + aug)
                try:
                    interval = Interval.create_interval(a, b)
                    print('({0}): {1}, {2}) --> {3}'.format(example_count, a, b, interval))
                    
                    dist = b.diatonic_tone.diatonic_index - a.diatonic_tone.diatonic_index
                    if dist < 0:
                        dist += 7
                    assert dist == interval.diatonic_distance
                    assert b.chromatic_distance - a.chromatic_distance == interval.chromatic_distance
                except Exception as e:
                    print('Exception ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e))
                    assert example_count in exception_items, \
                        'ASSERT ERROR ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e)
                    
    def test_all_c_octave_up_itervals(self):
        pitches = list('CDEFGAB')
        augs = ('bb', 'b', '',  '#', '##')
        exception_items = (1, 5, 10, 15, 16, 20, 21, 25, 30, 35)
        example_count = 0
        for pitch in pitches:
            for aug in augs:
                example_count += 1
                a = DiatonicPitch(4, 'C')
                b = DiatonicPitch(5, pitch + aug)
                try:
                    interval = Interval.create_interval(a, b)
                    assert b.chromatic_distance - a.chromatic_distance == interval.chromatic_distance
                    print('({0}): {1}, {2}) --> {3}'.format(example_count, a, b, interval))
                except Exception as e:
                    print('Exception ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e))
                    assert example_count in exception_items, \
                        'Exception ({0}): ({1}, {2}) : {3}'.format(example_count, a, b, e)

    def test_upper_pitch(self):
        pitch = DiatonicPitch(4, 'C')
        for i in range(1, 13):
            for interval_type in TestInterval.INTERVAL_TYPES:
                if i == 1 and interval_type == IntervalType(IntervalType.Diminished):
                        continue
                if i == 1 or i == 4 or i == 5 or i == 8 or i == 11 or i == 12:
                    if interval_type == IntervalType(IntervalType.Minor) or \
                       interval_type == IntervalType(IntervalType.Major):
                        continue 
                else:
                    if interval_type == IntervalType(IntervalType.Perfect):
                        continue
                interval = Interval(i, interval_type)
                p = interval.get_end_pitch(pitch)
                print(p)
                assert p.diatonic_distance() == 4 * 7 + 0 + (i - 1)

    def test_lower_pitch(self):

        pitch = DiatonicPitch(4, 'C')
        for i in range(1, 13):
            for interval_type in TestInterval.INTERVAL_TYPES:
                if i == 1 and interval_type == IntervalType(IntervalType.Diminished):
                        continue
                if i == 1 or i == 4 or i == 5 or i == 8 or i == 11 or i == 12:
                    if interval_type == IntervalType(IntervalType.Minor) or \
                       interval_type == IntervalType(IntervalType.Major):
                        continue 
                else:
                    if interval_type == IntervalType(IntervalType.Perfect):
                        continue
                try:
                    interval = Interval(i, interval_type)
                    p = interval.get_start_pitch(pitch)
                except:
                    e = sys.exc_info()[0]
                    print('exception {0} for interval i={1} interval={2} pitch={3}'.format(e, i, interval_type, pitch))
                    raise Exception('exception {0} for creating interval i={1} type={2} pitch={3}'.format(e, i,
                                                                                                          interval_type,
                                                                                                          pitch))

                print(p)
                assert p.diatonic_distance() == 4 * 7 + 0 - (i - 1)

    def test_upper_tone_non_C(self):
        pitch = DiatonicPitch(4, 'E')
        for i in range(1, 13):
            for interval_type in TestInterval.INTERVAL_TYPES:
                if i == 1 or i == 4 or i == 5 or i == 8 or i == 11 or i == 12:
                    if i == 1 and interval_type == IntervalType(IntervalType.Diminished):
                        continue
                    if interval_type == IntervalType(IntervalType.Minor) or \
                       interval_type == IntervalType(IntervalType.Major):
                        continue 
                else:
                    if interval_type == IntervalType(IntervalType.Perfect):
                        continue
                interval = Interval(i, interval_type)
                print(interval)
                p = interval.get_end_pitch(pitch)
                print(p)
                assert p.diatonic_distance() == 4 * 7 + 2 + (i - 1), \
                    'dist {0} does not match computation {1} on {2}'.format(p.diatonic_distance(), 4 * 7 + 0 + (i - 1),
                                                                            interval)

    def test_semitones(self):
        answers = (
                    0,
                    1,
                    0,
                    1,
                    2,
                    3,
                    2,
                    3,
                    4,
                    5,
                    4,
                    5,
                    6,
                    6,
                    7,
                    8,
                    7,
                    8,
                    9,
                    10,
                    9,
                    10,
                    11,
                    12,
                    11,
                    12,
                    13,
                    12,
                    13,
                    14,
                    15,
                    14,
                    15,
                    16,
                    17,
                    16,
                    17,
                    18,
                    18,
                    19,
                    20)
        
        test_index = 0
        for i in range(1, 13):
            for interval_type in TestInterval.INTERVAL_TYPES:
                if i == 1 or i == 4 or i == 5 or i == 8 or i == 11 or i == 12:
                    if i == 1 and interval_type == IntervalType(IntervalType.Diminished):
                        continue
                    if interval_type == IntervalType(IntervalType.Minor) or interval_type == \
                       IntervalType(IntervalType.Major):
                        continue 
                else:
                    if interval_type == IntervalType(IntervalType.Perfect):
                        continue
            
                interval = Interval(i, interval_type)
                semitones = interval.semitones()
                print('{0} has {1} semitones'.format(interval, semitones))
                assert semitones == answers[test_index], \
                    'semitones {0} != {1}  interval {2}'.format(semitones, answers[test_index], interval)
                test_index += 1
                                               
    def test_diff_octaves(self):
        dta = DiatonicPitch(3, 'A')
        dtb = DiatonicPitch(4, 'D')
        interval = Interval.create_interval(dta, dtb)
        print(interval)
        assert interval.semitones() == 5, '{0} != 5'.format(interval.semitones())  
        
    def test_various(self):
        dta = DiatonicPitch(2, 'B#')
        dtb = DiatonicPitch(3, 'C')
        interval = Interval.create_interval(dta, dtb)
        semitones = interval.semitones()
        print('Interval "{0}" based on {1} and {2} has {3} semitones'.format(interval, dta, dtb, semitones))
        
        # get a major 3rd pitch
        interval = Interval.create_interval(DiatonicPitch(2, 'E'), DiatonicPitch(2, 'G#'))
        end_pitch = interval.get_end_pitch(DiatonicPitch(4, 'E'))
        print(end_pitch)
        assert str(end_pitch) == 'G#:4'
        
    def test_parse(self):
        interval = Interval.parse('P:5')
        assert str(interval) == 'P:5'
        
        assert str(Interval.parse('A:8')) == 'A:8'
        assert str(Interval.parse('d:8')) == 'd:8'
        assert str(Interval.parse('M:3')) == 'M:3'
        assert str(Interval.parse('m:6')) == 'm:6'
        
        assert Interval.parse('-d:1') == Interval.parse('A:1')
        assert Interval.parse('-A:1') == Interval.parse('d:1')
        
    def test_negation(self):
        assert Interval.parse('-d:1').negation() == Interval.parse('d:1')
        assert Interval.parse('-A:1').negation() == Interval.parse('A:1')
        
    def test_inversion(self):
        interval_strs = ['d:1', 'P:1', 'A:1', 'd:2', 'm:2', 'M:2', 'A:2', 'd:3', 'm:3', 'M:3', 'A:3',
                         'd:4', 'P:4', 'A:4', 'd:5', 'P:5', 'A:5',
                         'd:6', 'm:6', 'M:6', 'A:6', 'd:7', 'm:7', 'M:7', 'A:7', 'd:8', 'P:8', 'A:8']
        answers = ['A:8', 'P:8', 'd:8', 'A:7', 'M:7', 'm:7', 'd:7', 'A:6', 'M:6', 'm:6', 'd:6',
                   'A:5', 'P:5', 'd:5', 'A:4', 'P:4', 'd:4',
                   'A:3', 'M:3', 'm:3', 'd:3', 'A:2', 'M:2', 'm:2', 'd:2', 'A:1', 'P:1', 'd:1']
        intervals = [Interval.parse(s) for s in interval_strs]
        print('+++++')
        for interval, answer in zip(intervals, answers):
            print('{0} --> {1}'.format(interval, interval.inversion()))
            assert str(interval.inversion()) == answer
        print('-----')

        interval = Interval.parse('A:12')
        inversion = interval.inversion()
        print('int={0} inv={1}'.format(interval, inversion))
        
        # Test augmented and negative intervals
        interval_strs = ['A:15', 'P:15', 'd:15', 'A:14', 'M:14', 'm:14', 'd:14', 'A:13', 'M:13', 'm:13', 'd:13',
                         'A:12', 'P:12', 'd:12',
                         'A:11', 'P:11', 'd:11', 'A:10', 'M:10', 'm:10', 'd:10', 'A:9', 'M:9', 'm:9', 'd:9',
                         ]
        answers = ['d:1', 'P:1', 'A:1', 'd:2', 'm:2', 'M:2', 'A:2', 'd:3', 'm:3', 'M:3', 'A:3', 'd:4', 'P:4', 'A:4',
                   'd:5', 'P:5', 'A:5', 'd:6', 'm:6', 'M:6', 'A:6', 'd:7', 'm:7', 'M:7', 'A:7']
        intervals = [Interval.parse(s) for s in interval_strs]
        print('+++++')
        for interval, answer in zip(intervals, answers):
            print('{0} --> {1}  {2}'.format(interval, interval.inversion(), answer))
            assert str(interval.inversion()) == answer
        print('-----')
        
        interval_strs = ['-d:1', '-P:1', '-A:1', '-d:2', '-m:2', '-M:2', '-A:2', '-d:3', '-m:3', '-M:3', '-A:3',
                         '-d:4', '-P:4', '-A:4', '-d:5', '-P:5', '-A:5',
                         '-d:6', '-m:6', '-M:6', '-A:6', '-d:7', '-m:7', '-M:7', '-A:7', '-d:8', '-P:8', '-A:8']
        answers = ['d:8', 'P:8', 'A:8', '-A:7', '-M:7', '-m:7', '-d:7', '-A:6', '-M:6', '-m:6', '-d:6', '-A:5',
                   '-P:5', '-d:5', '-A:4', '-P:4', '-d:4',
                   '-A:3', '-M:3', '-m:3', '-d:3', '-A:2', '-M:2', '-m:2', '-d:2', 'd:1', 'P:1', 'A:1']
        intervals = [Interval.parse(s) for s in interval_strs]
        print('+++++')
        for interval, answer in zip(intervals, answers):
            print('{0} --> {1}'.format(interval, interval.inversion()))
            assert str(interval.inversion()) == answer
        print('-----')
        
        interval_strs = ['-A:15', '-P:15', '-d:15', '-A:14', '-M:14', '-m:14', '-d:14',
                         '-A:13', '-M:13', '-m:13', '-d:13', '-A:12', '-P:12', '-d:12',
                         '-A:11', '-P:11', '-d:11', '-A:10', '-M:10', '-m:10', '-d:10', '-A:9', '-M:9', '-m:9', '-d:9',
                         ]
        answers = ['A:1', 'P:1', 'd:1', 'd:2', 'm:2', 'M:2', 'A:2', 'd:3', 'm:3', 'M:3', 'A:3', 'd:4', 'P:4', 'A:4',
                   'd:5', 'P:5', 'A:5', 'd:6', 'm:6', 'M:6', 'A:6', 'd:7', 'm:7', 'M:7', 'A:7']
        intervals = [Interval.parse(s) for s in interval_strs]
        print('+++++')
        for interval, answer in zip(intervals, answers):
            print('{0} --> {1}  {2}'.format(interval, interval.inversion(), answer))
        print('-----')
        
    def test_negative_intervals(self):
        interval = Interval(-3, IntervalType.Major)
        assert interval.diatonic_distance == -2
        assert interval.chromatic_distance == -4
        assert str(interval) == '-M:3'
        print(interval)
        
        interval = Interval.parse('-P:5')
        assert interval.diatonic_distance == -4
        assert interval.chromatic_distance == -7
        assert str(interval) == '-P:5'
        print(interval)
        
        pitch_a = DiatonicPitch(5, 'C')
        pitch_b = DiatonicPitch(4, 'C')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Perfect)
        assert interval.diatonic_distance == -7
        
        pitch_a = DiatonicPitch(5, 'C')
        pitch_b = DiatonicPitch(4, 'Cb')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Augmented)
        assert interval.diatonic_distance == -7
        assert str(interval) == '-A:8'
        
        pitch_a = DiatonicPitch(5, 'C')
        pitch_b = DiatonicPitch(4, 'C#')
        interval = Interval.create_interval(pitch_a, pitch_b)
        print(interval)
        assert interval.interval_type == IntervalType(IntervalType.Diminished)
        assert interval.diatonic_distance == -7
        assert str(interval) == '-d:8'

        pitch_a = DiatonicPitch(5, 'C')
        lower_pitches = [DiatonicPitch(4, i) for i in list('CDEFGAB')]
        answers = ['-P:8', '-m:7', '-m:6', '-P:5', '-P:4', '-m:3', '-m:2']
        for (p, a) in zip(lower_pitches, answers):
            interval = Interval.create_interval(pitch_a, p)
            assert str(interval) == a
          
        lower_pitches = [DiatonicPitch(4, i) for i in 'Cb,Db,Eb,Fb,Gb,Ab,Bb'.split(',')]
        answers = ['-A:8', '-M:7', '-M:6', '-A:5', '-A:4', '-M:3', '-M:2']
        for (p, a) in zip(lower_pitches, answers):
            interval = Interval.create_interval(pitch_a, p)
            assert str(interval) == a

        lower_pitches = [DiatonicPitch(4, i) for i in 'C#,D#,E#,F#,G#,A#,B#'.split(',')]
        answers = ['-d:8', '-d:7', '-d:6', '-d:5', '-d:4', '-d:3', '-d:2']
        for (p, a) in zip(lower_pitches, answers):
            interval = Interval.create_interval(pitch_a, p)
            assert str(interval) == a

        interval = Interval.parse('-M:3')
        p = DiatonicPitch(4, 'Ab')
        end_p = interval.get_end_pitch(p)
        print(end_p)
        assert str(end_p) == 'Fb:4'
        
        interval = Interval.parse('-P:5')
        p = DiatonicPitch(4, 'D')
        end_p = interval.get_end_pitch(p)
        print(end_p)
        assert str(end_p) == 'G:3'

        interval_strs = ['-P:1', '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-P:8', '-M:9', '-M:10',
                         '-P:11', '-P:12', '-M:13', '-M:14', '-P:15']
        intervals = [Interval.parse(i) for i in interval_strs]
        p = DiatonicPitch(4, 'G')
        answers = ['G:4', 'F:4', 'Eb:4', 'D:4', 'C:4', 'Bb:3', 'Ab:3', 
                   'G:3', 'F:3', 'Eb:3', 'D:3', 'C:3', 'Bb:2', 'Ab:2',
                   'G:2'
                   ]
        end_ps = []
        for interval in intervals:
            end_p = interval.get_end_pitch(p)
            print(end_p)
            end_ps.append(end_p)
        for end_p, answer in zip(end_ps, answers):
            assert str(end_p) == answer
            
        # Negation tests
        interval_strs = ['P:1', 'M:2', 'M:3', 'P:4', 'P:5', 'M:6', 'M:7', 'P:8', 'M:9', 'M:10', 'P:11',
                         'P:12', 'M:13', 'M:14', 'P:15',
                         '-P:1', '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-P:8', '-M:9', '-M:10', '-P:11',
                         '-P:12', '-M:13', '-M:14', '-P:15']
        intervals = [Interval.parse(i) for i in interval_strs]
        count = 1
        for interval, i_str in zip(intervals, interval_strs):
            neg_interval = interval.negation()
            if count <= 15:
                assert str(neg_interval) == ('-' if count > 1 else '') + i_str
            else:
                assert str(neg_interval) == i_str[1:]
            count += 1
            
        interval_strs = ['-P:1', '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-P:8', '-M:9', '-M:10', '-P:11',
                         '-P:12', '-M:13', '-M:14', '-P:15']
        intervals = [Interval.parse(i) for i in interval_strs]
        p = DiatonicPitch(4, 'G')
        answers = ['G:4', 'A:4', 'B:4', 'C:5', 'D:5', 'E:5', 'F#:5', 
                   'G:5', 'A:5', 'B:5', 'C:6', 'D:6', 'E:6', 'F#:6',
                   'G:6'
                   ]
        end_ps = []
        print('+++++')
        for interval in intervals:
            end_p = interval.get_start_pitch(p)
            print(end_p)
            end_ps.append(end_p)
        print('-----')
        for end_p, answer in zip(end_ps, answers):
            assert str(end_p) == answer
            
    def test_add_intervals(self):
        interval_strs = ['P:1', 'd:2', 'm:2', 'M:2', 'm:3', 'M:3', 'd:4', 'P:4', 'P:5', 'm:6', 'M:6', 'm:7', 'M:7']
        TestInterval.add_intervals(interval_strs)
        
    def test_print_table_for_book(self):
        interval_strs = ['P:1', 'M:2', 'm:3', 'M:3', 'd:4', 'P:4', 'P:5', 'M:6',  'M:7']
        result = TestInterval.add_intervals(interval_strs)
        TestInterval.print_table(len(interval_strs), result)
        
    def test_print_simple_interval_add(self):
        print('--Simple Interval Addition')
        interval_strs = ['P:1', 'M:2', 'M:3', 'd:3', 'd:4']
        result = TestInterval.add_intervals(interval_strs)
        TestInterval.print_table(len(interval_strs), result)

    @staticmethod
    def add_intervals(interval_strs):
        intervals = [Interval.parse(x) for x in interval_strs]
        
        result = []
        for a in intervals:
            for b in intervals:
                # noinspection PyBroadException
                try:                
                    c = a + b
                    print('{0} + {1} = {2}'.format(a, b, c))
                    result.append(c)
                except Exception:
                    print('{0} + {1} = X'.format(a, b))
                    result.append(None)
        return result
        
    def test_plus_equals(self):
        a = Interval(3, IntervalType(IntervalType.Major))
        
        a += Interval(3, IntervalType(IntervalType.Minor))
        assert a == (Interval(5, IntervalType(IntervalType.Perfect)))
        
        a = Interval(2, IntervalType(IntervalType.Diminished))  
        
        with self.assertRaises(Exception):
            a += Interval(3, IntervalType(IntervalType.Minor))
        
    def test_reduction(self):
        
        interval_strs = ['d:1', 'P:1', 'A:1', 'M:2', 'M:3', 'P:4', 'P:5', 'M:6', 'M:7', 'd:8', 'P:8', 'A:8', 'M:9',
                         'M:10', 'P:11', 'P:12', 'M:13', 'M:14', 'd:15', 'P:15', 'A:15',
                         '-d:1', '-P:1', '-A:1', '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-d:8', '-P:8',
                         '-A:8', '-M:9', '-M:10', '-P:11', '-P:12', '-M:13', '-M:14', '-d:15', '-P:15', '-A:15']
        intervals = [Interval.parse(i) for i in interval_strs]  
        answers = ['d:1', 'P:1', 'A:1', 'M:2', 'M:3', 'P:4', 'P:5', 'M:6', 'M:7', 'd:8', 'P:8', 'A:8', 'M:2',
                   'M:3', 'P:4', 'P:5', 'M:6', 'M:7', 'd:8', 'P:8', 'A:8',
                   'A:1', 'P:1', 'd:1', '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-d:8', '-P:8', '-A:8',
                   '-M:2', '-M:3', '-P:4', '-P:5', '-M:6', '-M:7', '-d:8', '-P:8', '-A:8']
        for interval, answer in zip(intervals, answers):
            reduction = interval.reduction()
            print('reduce({0}) --> {1}, answer = {2}'.format(interval, reduction, answer))
            assert str(reduction) == answer, 'reduce({0}) --> {1}, answer = {2}'.format(interval, reduction, answer)
            
    def test_whole_note_scale_inrements(self):
        for i in range(0, 6):
            intervals = ['P:1']
            for count in range(0, 6):
                if i == count:
                    intervals.append('d:3')
                else:
                    intervals.append('M:2')
                    
            # test result
            answer = Interval.parse('P:1')
            answers = [answer]
            iterintervals = iter(intervals)
            next(iterintervals)
            for x in iterintervals:
                xi = Interval.parse(x)
                answer += xi
                answers.append(answer)
            incrementals = ', '.join(t for t in intervals)
            results = ', '.join(str(t) for t in answers)
            print('{0}   -->   {1}'.format(incrementals, results))
        print('end of test')
 
    def test_HW_Oct_scale_inrements(self):
        prime = ['P:1', 'm:2', 'M:2', 'm:2', 'M:2', 'm:2', 'M:2', 'm:2', 'M:2']
        for i in range(0, 4):
            intervals = ['P:1']
            for count in range(1, 9):
                if 2 * i + 1 == count:
                    intervals.append('A:1')
                else:
                    intervals.append(prime[count])
                    
            # test result
            answer = Interval.parse('P:1')
            answers = [answer]
            iterintervals = iter(intervals)
            next(iterintervals)
            for x in iterintervals:
                xi = Interval.parse(x)
                answer += xi
                answers.append(answer)
            incrementals = ', '.join(t for t in intervals)
            results = ', '.join(str(t) for t in answers)
            print('{0}   -->   {1}'.format(incrementals, results))
        print('end of test')

    def test_pure_distances(self):
        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('E'),
                                                  DiatonicToneCache.get_tone('C'))
        assert dd == 5
        assert cc == 8

        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('Ab'),
                                                  DiatonicToneCache.get_tone('B'))
        assert dd == 1
        assert cc == 3

        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('C'),
                                                  DiatonicToneCache.get_tone('B'))
        assert dd == 6
        assert cc == 11

        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('B'),
                                                  DiatonicToneCache.get_tone('C'))
        assert dd == 1
        assert cc == 1

        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('Ebb'),
                                                  DiatonicToneCache.get_tone('A#'))
        assert dd == 3
        assert cc == 8

        dd, cc = Interval.calculate_pure_distance(DiatonicToneCache.get_tone('A#'),
                                                  DiatonicToneCache.get_tone('Ebb'))
        assert dd == 4
        assert cc == 4

        end_tone = Interval.end_tone_from_pure_distance(DiatonicToneCache.get_tone('C'), 4, 6)
        assert 'Gb'== DiatonicTone.to_upper(end_tone.diatonic_symbol)

        end_tone = Interval.end_tone_from_pure_distance(DiatonicToneCache.get_tone('G'), 2, 5)
        assert 'B#'== DiatonicTone.to_upper(end_tone.diatonic_symbol)

        end_tone = Interval.end_tone_from_pure_distance(DiatonicToneCache.get_tone('Gb'), 4, 6, False)
        assert 'C'== DiatonicTone.to_upper(end_tone.diatonic_symbol)

        end_tone = Interval.end_tone_from_pure_distance(DiatonicToneCache.get_tone('B#'), 2, 5, False)
        assert 'G' == DiatonicTone.to_upper(end_tone.diatonic_symbol)
        
    def test_WH_Oct_scale_increments(self):
        print('test_WH_Oct_scale_increments')
        prime = ['P:1', 'M:2', 'm:2', 'M:2', 'm:2', 'M:2', 'm:2', 'M:2', 'm:2']
        for i in range(0, 4):
            intervals = ['P:1']
            for count in range(1, 9):
                if 2 * i + 2 == count:
                    intervals.append('A:1')
                else:
                    intervals.append(prime[count])
                    
            # test result
            answer = Interval.parse('P:1')
            answers = [answer]
            iterintervals = iter(intervals)
            next(iterintervals)
            for x in iterintervals:
                xi = Interval.parse(x)
                answer += xi
                answers.append(answer)
            incrementals = ', '.join(t for t in intervals)
            results = ', '.join(str(t) for t in answers)
            print('{0}   -->   {1}'.format(incrementals, results))
        print('end of test')

    def test_interval_exception(self):
        i1 = Interval.parse('d:4')
        i2 = Interval.parse('d:3')
        try:
            i = i1 + i2
        except IntervalException as e:
            print('caught exception ' + str(e))
            assert e

    def test_book_examples(self):
        # Interval Creation
        interval = Interval(5, IntervalType.Perfect)
        print(interval)
        interval = Interval.parse("m:10")
        print(interval)
        interval = Interval.create_interval(DiatonicPitch.parse("a:3"), DiatonicPitch.parse("f#:4"))
        print(interval)

        # Interval Addition/Subtraction
        i1 = Interval(5, IntervalType.Perfect)
        i2 = Interval.parse("M:3")
        interval = i1 + i2
        print(interval)
        interval = i1 - i2
        print(interval)
        interval += i2
        print(interval)
        interval -= i2
        print(interval)

        # compute end and start
        interval = Interval(5, IntervalType.Perfect)
        pitch = interval.get_end_pitch(DiatonicPitch.parse("F#:5"))
        print(pitch)
        pitch = interval.get_start_pitch(DiatonicPitch.parse("C:5"))
        print(pitch)

    @staticmethod
    def print_table(row_len, result):
        rows = len(result) // row_len
        
        # print('     |', end="")
        sys.stdout.write('     |')
        for i in range(0, row_len):
            # vprint('   {0}'.format(result[i]), end="")
            sys.stdout.write('   {0}'.format(result[i]))
        print()
        print('{0}{1}'.format('-----|', row_len * '-------'))
        
        index = 0
        for j in range(0, rows):
            # print('{0}  |'.format(result[j]), end="")
            sys.stdout.write('{0}  |'.format(result[j]))
            for i in range(0, row_len):
                if result[index]:
                    # print('   {0}'.format(result[index]), end="")
                    sys.stdout.write('   {0}'.format(result[index]))
                else:
                    # print('    X '.format(result[index]), end="")
                    sys.stdout.write('    X '.format(result[index]))
                index += 1
            print()

if __name__ == "__main__":
    unittest.main()
