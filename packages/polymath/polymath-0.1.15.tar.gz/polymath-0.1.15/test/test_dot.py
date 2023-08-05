import unittest
from numpy import array
from numpy.testing import assert_array_equal
import polymath

class TestDot(unittest.TestCase):

    def test_01(self):
        input_test = array([
            [[ 1, -1, -1], [1,  1,  1]],
            [[-1, -1,  1], [1, -1, -1]],
            [[ 1, -1,  1], [1, -1,  1]]
        ])
        weights = array([
            [0.3, -0.2, 1.5],
            [-0.7, 2.5, -1]
        ])
        dot = array([
            [-1. ,  0.8],
            [ 1.4, -2.2],
            [ 2. , -4.2]])

        assert_array_equal(
            polymath.dot(input_test, weights),
            dot,
            "Dot product fails."
        )
