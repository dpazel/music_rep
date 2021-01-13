import unittest

from function.permutation import Permutation

import logging
import sys


class TestPermutation(unittest.TestCase):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_permutation_function(self):
        domain = {1, 2, 3}
        cycles = [[1, 3, 2]]
        p = Permutation(domain, cycles)
        print(p)

        assert 3 == p[1]
        assert 2 == p[3]
        assert 1 == p[2]

        cycles = [[1, 3, 2], [1, 2]]
        p = Permutation(domain, cycles)
        print(p)

        assert 1 == p[1]
        assert 2 == p[3]
        assert 3 == p[2]

    def test_permutation_multiplication(self):
        domain = {1, 2, 3, 4}
        cycles_1 = [[1, 3, 2]]
        cycles_2 = [[1, 3], [2, 4]]

        p1 = Permutation(domain, cycles_1)
        print('p1={0}'.format(p1))
        p2 = Permutation(domain, cycles_2)
        print('p2={0}'.format(p2))

        p3 = p1 * p2
        print('p1 * p2 = {0}'.format(p3))

        p3 = p2 * p1
        print('p2 * p1 = {0}'.format(p3))

    def test_inversion(self):
        domain = {1, 2, 3, 4}
        cycles = [[1, 3, 4, 2]]
        p = Permutation(domain, cycles)

        inverse = p.inverse()

        assert 2 == inverse[1]
        assert 4 == inverse[2]
        assert 1 == inverse[3]
        assert 3 == inverse[4]

        id = p * inverse

        assert 1 == id[1]
        assert 2 == id[2]
        assert 3 == id[3]
        assert 4 == id[4]

        id = inverse * p

        assert 1 == id[1]
        assert 2 == id[2]
        assert 3 == id[3]
        assert 4 == id[4]

