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

        id_array = p * inverse

        assert 1 == id_array[1]
        assert 2 == id_array[2]
        assert 3 == id_array[3]
        assert 4 == id_array[4]

        id_array = inverse * p

        assert 1 == id_array[1]
        assert 2 == id_array[2]
        assert 3 == id_array[3]
        assert 4 == id_array[4]

    def test_book_example(self):
        domain = {1, 2, 3, 4, 5, 6, 7}
        p_cycles = [[1, 3, 4, 2], [6, 5, 7]]
        p = Permutation(domain, p_cycles)
        print(p)

        q_cycles = [[1, 3], [2, 4], [5, 7]]
        q = Permutation(domain, q_cycles)
        print(q)

        p3 = p * q
        print('p * q = {0}'.format(p3))

        p3 = q * p
        print('q * p = {0}'.format(p3))

        i = p.inverse()
        print(i)
        print('p * i = {0}'.format(p * i))
        print('i * p = {0}'.format(i * p))
