import unittest
from numpy import array, prod
from numpy.random import RandomState
from numpy.testing import assert_array_equal
import pypuf_helper as ph


class TestCombinerXORNumpy(unittest.TestCase):

    def test_01(self):
        N = 1000
        k = 10
        random_instance = RandomState()
        responses = array(random_instance.choice((-1, +1), (N, k)))

        ph_xor = ph.combiner_xor(responses)
        numpy_xor = prod(responses, 1)

        assert_array_equal(
            ph_xor,
            numpy_xor,
            "Comparison of combiner_xor with numpy fails."
        )