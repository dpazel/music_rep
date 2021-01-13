import unittest

from function.discrete_function import DiscreteFunction

import logging
import sys


class TestDiscreteFunction(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_function(self):
        # domain = {'a', 'b', 'c'}
        # range = {1, 2, 3, 4}
        initializer = {'a': 2, 'b': 1, 'c': 3}
        df = DiscreteFunction(initializer)

        assert 2 == df['a']
        assert 1 == df['b']
        assert 3 == df['c']

        df['b'] = 4
        assert 4 == df['b']

        del df['a']
        assert df['a'] is None

        try:
            df['b'] = 9
            assert False
        except Exception as e:
            print('Passed - Exception {0}'.format(e))

        try:
            df['x'] = 1
            assert False
        except Exception as e:
            print('Passed - Exception {0}'.format(e))

    def test_simple_with_none(self):
        # domain = {'a', 'b', 'c'}
        # range = {1, 2, 3, 4}
        initializer = {'a': None, 'b': 1, 'c': None}
        df = DiscreteFunction(initializer)

        assert df['a'] is None
        assert 1 == df['b']
        assert df['c'] is None
