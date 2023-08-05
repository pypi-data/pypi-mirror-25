# Author: Michal Ciesielczyk
# Licence: MIT
import unittest
import math
from ..tensor_operations import mean_squared_error, hosvd
from .. import DenseTensor


class Test(unittest.TestCase):

    def test_mean_squared_error(self):
        print("Test mean_squared_error... ", end="", flush=True)
        try:
            t1 = DenseTensor.zeros((2, 2, 2))
            t1[0, 0, 0] = 1
            t2 = DenseTensor.zeros((2, 2, 2))
            t2[0, 0, 0] = 1
            assert mean_squared_error(t1, t2) == 0.0
            t1[0, 0, 1] = 1
            assert mean_squared_error(t1, t2) == 0.125

            t1 = DenseTensor.random((4, 4, 4))
            t2 = DenseTensor.random((4, 4, 4))
            assert math.isclose(mean_squared_error(t1, t2), ((t1 - t2) ** 2).mean(axis=None))
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_hosvd(self):
        print("Test hosvd... ", end="", flush=True)
        try:
            d = 32
            shape = (d, d, d)
            X = DenseTensor.random(shape)
            R = DenseTensor.random(shape)
            min_rmse = 0.0
            max_rmse = math.sqrt(mean_squared_error(X, R))
            for i in range(d, 0, -1):
                reduced_shape = [i for _ in range(len(shape))]
                U, core = hosvd(X, reduced_shape, compute_core=True)
                X2 = core.mult(U, transpose=True)
                rmse = math.sqrt(mean_squared_error(X, X2))
                assert min_rmse < rmse 
                assert max_rmse > rmse
                min_rmse = rmse
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testmean']
    unittest.main()
