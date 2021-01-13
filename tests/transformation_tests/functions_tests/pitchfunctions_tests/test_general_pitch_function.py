import logging
import sys
import unittest

from tonalmodel.diatonic_pitch import DiatonicPitch
from transformation.functions.pitchfunctions.general_pitch_function import GeneralPitchFunction


class TestGeneralPitchFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_pitch_function(self):

        p_map = {'A:7': 'Ab:7', 'Bb:6': 'B:6', 'Db:5': 'D:5'}

        gpf = GeneralPitchFunction(p_map)

        assert DiatonicPitch.parse('Ab:7') == gpf['A:7']
        assert DiatonicPitch.parse('B:6') == gpf['Bb:6']
        assert DiatonicPitch.parse('D:5') == gpf['Db:5']

        print(gpf)

        # Test assignment
        gpf['Db:5'] = 'Ab:7'

        assert DiatonicPitch.parse('Ab:7') == gpf['A:7']
        assert DiatonicPitch.parse('B:6') == gpf['Bb:6']
        assert DiatonicPitch.parse('Ab:7') == gpf['Db:5']

        print(gpf)

    def test_none_setting(self):

        p_map = {'A:7': 'Ab:7', 'Bb:6': 'B:6', 'Db:5': None}

        gpf = GeneralPitchFunction(p_map)

        assert DiatonicPitch.parse('Ab:7') == gpf['A:7']
        assert DiatonicPitch.parse('B:6') == gpf['Bb:6']
        assert gpf['Db:5'] is None

        gpf['A:7'] = None

        assert gpf['A:7'] is None
        assert DiatonicPitch.parse('B:6') == gpf['Bb:6']
        assert gpf['Db:5'] is None
        print(gpf)

        gpf['A:7'] = None
        assert gpf['A:7'] is None
        assert DiatonicPitch.parse('B:6') == gpf['Bb:6']
        assert gpf['Db:5'] is None
