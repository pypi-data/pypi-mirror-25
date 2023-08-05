# Author: Michal Ciesielczyk
# Licence: MIT
import unittest
import math
import numpy as np
from ..matrix_operations import svd


class Test(unittest.TestCase):

    def test_svd(self):
        print("Test svd... ", end="", flush=True)
        try:
            m = np.array([[1.0, 2.0], [3.0, 4.0]])
            U, S, V = svd(m, 2)
            assert np.allclose(m, np.dot(U, np.dot(np.diag(S), V)))

            U, S, V = svd(m, 0.95)
            assert np.allclose(m, np.dot(U, np.dot(np.diag(S), V)))

            rm = np.random.randn(128, 256)
            U, S, V = svd(rm, 120)
            assert np.allclose(rm, np.dot(U, np.dot(np.diag(S), V)), rtol=0.5, atol=0.5)

            rm = np.random.randn(128, 256)
            U, S, V = svd(rm, 0.99)
            assert np.allclose(rm, np.dot(U, np.dot(np.diag(S), V)), rtol=0.1, atol=0.5)

            U, S, V = svd(rm, 0.99, algorithm='randomized')
            assert np.allclose(rm, np.dot(U, np.dot(np.diag(S), V)), rtol=0.1, atol=0.5)

            randomizedS = svd(rm, 0.99, False, False, algorithm='randomized')[0]
            arpackS = svd(rm, 0.99, False, False, algorithm='arpack')[0]
            lapackS = svd(rm, 0.95, False, False, algorithm='lapack')[0]
            assert math.isclose(randomizedS, arpackS)
            assert math.isclose(randomizedS, lapackS)
            assert math.isclose(lapackS, arpackS)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testSVD']
    unittest.main()
