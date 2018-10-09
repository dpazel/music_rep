import unittest
from tonalmodel.modality import ModalityType, ModalitySpec, Modality


class TestDiatonicModality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_defined_modality(self):
        modality_type = ModalityType('my_modality')
        incremental_interval_strs = [
            'P:1', 'm:2', 'M:3', 'm:2', 'm:2', 'M:2', 'A:2'
        ]
        modality_spec = ModalitySpec(modality_type, incremental_interval_strs)
        modality = Modality(modality_spec)

        assert modality.modality_type == modality_type
        assert modality.get_number_of_tones() == 6

        intervals = modality.incremental_intervals
        assert len(intervals) == 7
        assert str(intervals[0]) == 'P:1'
        assert str(intervals[1]) == 'm:2'
        assert str(intervals[2]) == 'M:3'
        assert str(intervals[3]) == 'm:2'
        assert str(intervals[4]) == 'm:2'
        assert str(intervals[5]) == 'M:2'
        assert str(intervals[6]) == 'A:2'