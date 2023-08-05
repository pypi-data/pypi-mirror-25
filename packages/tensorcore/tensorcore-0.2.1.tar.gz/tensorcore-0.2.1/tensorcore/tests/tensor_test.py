# Author: Michal Ciesielczyk
# Licence: MIT
import unittest
import math
import numpy as np
from abc import abstractmethod
from random import random, shuffle, randint
from itertools import product
from .. import CooTensor, DokTensor, DenseTensor


class CommonTensorTests(object):
    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def create_empty(self, shape):
        pass

    @abstractmethod
    def create_random(self, shape):
        pass

    @abstractmethod
    def construct_tensor(self, shape, indices, values):
        pass

    def test_ndim(self):
        print("Test %s.ndim... " % self.name, end="", flush=True)
        try:
            for d in range(1, 6):
                shape = [2 for _ in range(d)]
                assert d == self.create_empty(tuple(shape)).ndim
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_nnz(self):
        print("Test %s.nnz... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4, 4)
            indices = [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 1, 0)]
            values = [1.0, -1.0, 0.0001, -0.0000001]
            t = self.construct_tensor(shape, indices, values)
            assert t.nnz == 4
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_copy(self):
        print("Test %s.copy()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            T = self.create_random(shape)
            C = T.copy()
            assert T == C
            assert T is not C
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_iter(self):
        print("Test %s.__iter__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            T = self.create_random(shape)
            nnz = T.nnz
            norm = T.norm()
            count = 0
            sum2 = 0
            for _, val in T:
                count += 1
                sum2 += val * val
            assert count == nnz
            assert np.isclose(norm, math.sqrt(sum2))
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_equal(self):
        print("Test %s.__equal__()... " % self.name, end="", flush=True)
        try:
            shape = (5, 5, 5)
            T = self.create_random(shape)
            T2 = T.copy()
            assert T == T2
            T2 = self.create_random(shape)
            assert not T == T2
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_norm(self):
        print("Test %s.norm()... " % self.name, end="", flush=True)
        try:
            t = self.create_random((4, 4, 4))
            norm2 = math.sqrt(t.aggregate(lambda x, y: x + y, lambda x: x * x))
            assert math.isclose(t.norm(), norm2)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_sum(self):
        print("Test %s.sum()... " % self.name, end="", flush=True)
        try:
            X = self.create_empty((2, 2, 2, 2, 2))
            X = X.sum(0)
            assert X.ndim == 4
            assert X.size == 16

            X = X.sum((1, 2))
            assert X.ndim == 2
            assert X.size == 4

            X = self.create_random((4, 4, 4)).to_dense()
            expected = X.sum((1, 2))
            result = X.sum((1, 2))
            assert result == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_transpose(self):
        print("Test %s.transpose()... " % self.name, end="", flush=True)
        try:
            shape = (2, 2)
            indices = [(0, 0), (0, 1), (1, 0), (1, 1)]
            values = [0, 1, 2, 3]
            values_t = [0, 2, 1, 3]
            t1 = self.construct_tensor(shape, indices, values)
            t2 = self.construct_tensor(shape, indices, values_t)

            assert t1.transpose(modes=[1, 0]) == t2
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_assign(self):
        print("Test %s.assign()... " % self.name, end="", flush=True)
        try:
            s = 4
            shape = (s, s, s)
            t = self.create_empty(shape)
            t.assign(lambda _: 1.0)
            for v in t.values():
                assert v == 1.0
            t.assign(lambda x: x * 2.0)
            for v in t.values():
                assert v == 2.0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_aggregate(self):
        print("Test %s.aggregate()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            indices = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (2, 0, 3)]
            values = [1, 2, 3, 4]
            t = self.construct_tensor(shape, indices, values)

            assert t.aggregate(lambda x, y: x + y) == 10
            assert t.aggregate(lambda x, y: x + y, lambda x: x * 2) == 20
            assert t.aggregate(lambda x, y: x + y, lambda x: x * -1.5) == -15
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_unfold(self):
        print("Test %s.unfold()... " % self.name, end="", flush=True)
        try:
            shape = (2, 2, 2)
            indices = list(product(*[range(0, 2)] * 3))
            values = list(range(8))
            t = self.construct_tensor(shape, indices, values)

            f0 = np.array([[0, 2, 1, 3], [4, 6, 5, 7]])
            assert (f0 == t.unfold(0)).all()
            f1 = np.array([[0, 4, 1, 5], [2, 6, 3, 7]])
            assert (f1 == t.unfold(1)).all()
            f2 = np.array([[0, 4, 2, 6], [1, 5, 3, 7]])
            assert (f2 == t.unfold(2)).all()

            f01 = np.array([[0, 1], [2, 3], [4, 5], [6, 7]])
            assert (f01 == t.unfold([0, 1])).all()
            f12 = np.array([[0, 4], [1, 5], [2, 6], [3, 7]])
            assert (f12 == t.unfold([1, 2])).all()
            f02 = np.array([[0, 2], [1, 3], [4, 6], [5, 7]])
            assert (f02 == t.unfold([0, 2])).all()
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_fold(self):
        print("Test %s.fold()... " % self.name, end="", flush=True)
        try:
            X = self.create_random((2, 2, 2, 2, 2))
            assert X.unfold(1).fold() == X

            shape = (2, 2, 2)
            indices = list(product(*[range(0, 2)] * 3))
            values = list(range(8))
            X = self.construct_tensor(shape, indices, values)
            assert X.unfold(0).fold() == X
            assert X.unfold(1).fold() == X
            assert X.unfold(2).fold() == X

            assert X.unfold([0, 1]).fold() == X
            assert X.unfold([0, 2]).fold() == X
            assert X.unfold([1, 2]).fold() == X
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_zeros(self):
        print("Test %s.zeros()... " % self.name, end="", flush=True)
        try:
            s = 4
            shape = (s, s, s)
            t = self.create_empty(shape)
            for v in t.values():
                assert v == 0.0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


class DenseTensorTest(unittest.TestCase, CommonTensorTests):
    @property
    def name(self):
        return "DenseTensor"

    def create_empty(self, shape):
        return DenseTensor.zeros(shape)

    def create_random(self, shape):
        return DenseTensor.random(shape)

    def construct_tensor(self, shape, indices, values):
        t = DenseTensor.zeros(shape)
        for ind, val in zip(indices, values):
            t[ind] = val
        return t

    @classmethod
    def setUpClass(cls):
        X = DenseTensor(((2, 2), (2, 2), (2, 2)))
        assert X.shape[0] == 3
        assert X.shape[1] == 2

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_innerprod(self):
        print("Test %s.innerprod()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            t = DenseTensor.random(tuple(shape))
            assert t.innerprod(t) == (t * t).sum()
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_outerprod(self):
        print("Test %s.outerprod()... " % self.name, end="", flush=True)
        try:
            s = 16
            X = DenseTensor.random((s, s, s))
            v = np.ones(s) * s
            np.array_equal(X.outerprod(v), np.multiply.outer(X, v))
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_mult(self):
        print("Test %s.mult()... " % self.name, end="", flush=True)
        try:
            tshape = (4, 4)
            vshape = (4, 2)
            X = self.create_random(tshape)
            V = np.asarray(np.random.rand(*vshape))

            assert np.allclose(X.mult(V, 0), X.T.dot(V).T)

            tshape = (4, 4, 4)
            X = self.create_random(tshape)
            assert X.mult(V).shape == (2, 2, 2)
            assert X.mult([V, V, V]).shape == (2, 2, 2)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_center(self):
        print("Test %s.center()... " % self.name, end="", flush=True)
        try:
            X = DenseTensor(np.arange(8).reshape(2, 2, 2), dtype=float)
            X0 = X.copy()
            X0.center(0)
            expected = X.copy()
            expected[0] -= 1.5
            expected[1] -= 5.5
            assert X0 == expected

            X1 = X.copy()
            X1.center(1)
            expected = X.copy()
            expected[:, 0] -= 2.5
            expected[:, 1] -= 4.5
            assert X1 == expected

            X2 = X.copy()
            X2.center(2)
            expected = X.copy()
            expected[:, :, 0] -= 3
            expected[:, :, 1] -= 4
            assert X2 == expected

            expected = X.copy()
            expected -= 3.5
            X.center()
            assert X == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


class CooTensorTest(unittest.TestCase, CommonTensorTests):
    @property
    def name(self):
        return "CooTensor"

    def create_empty(self, shape):
        return CooTensor([], [], shape, dtype=float)

    def construct_tensor(self, shape, indices, values):
        return CooTensor(indices, values, shape)

    def create_random(self, shape, fill=0.1):
        all_idx = []
        for s in shape:
            all_idx.append(range(0, s))
        all_idx = list(product(*all_idx))
        shuffle(all_idx)

        size = np.prod(shape)
        nnz = int(size * fill)
        idx = all_idx[0:nnz]
        vals = []
        for _ in range(nnz):
            vals.append(random())
        return CooTensor(idx, vals, shape)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal_dok(self):
        print("Test %s.__equal__()... " % self.name, end="", flush=True)
        try:
            shape = (5, 5, 5)
            T = self.create_random(shape)
            T2 = T.copy().to_dok()
            assert T == T2
            T2 = self.create_random(shape).to_dok()
            assert not T == T2
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_mul(self):
        print("Test %s.__mul__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            int_val = randint(1, 100)
            float_val = random()

            assert (T * int_val) == (T.to_dense() * int_val)
            assert (T * float_val) == (T.to_dense() * float_val)
            assert (T * 0).nnz == 0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_imul(self):
        print("Test %s.__imul__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)

            val = randint(1, 100)
            expected = T.to_dense() * val
            T *= val
            assert T == expected

            val = random()
            expected = T.to_dense() * val
            T *= val
            assert T == expected

            T *= 0
            assert T.nnz == 0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_div(self):
        print("Test %s.__div__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            int_val = randint(1, 100)
            float_val = random()

            assert (T / int_val) == (T.to_dense() / int_val)
            assert (T / float_val) == (T.to_dense() / float_val)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_idiv(self):
        print("Test %s.__idiv__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)

            val = randint(1, 100)
            expected = T.to_dense() / val
            T /= val
            assert T == expected

            val = random()
            expected = T.to_dense() / val
            T /= val
            assert T == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_neg(self):
        print("Test %s.__neg__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            assert -T == -(T.to_dense())
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_innerprod(self):
        print("Test %s.innerprod()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            t = self.create_random(shape, 0.5)
            expected_result = sum(v * v for v in t.values())

            # test with dense
            assert t.innerprod(t.to_dense()) == expected_result
            # test with dok
            assert t.innerprod(t.to_dok()) == expected_result
            # test with coo
            assert t.innerprod(t) == expected_result
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_outerprod(self):
        print("Test %s.outerprod()... " % self.name, end="", flush=True)
        try:
            s = 16
            X = self.create_random((s, s, s), 0.5)
            V = self.create_random((s,), 0.5)
            expected = DenseTensor(
                np.multiply.outer(X.to_dense(), V.to_dense()))
            assert X.outerprod(V.to_dense()) == expected
            assert X.outerprod(V) == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_mult(self):
        print("Test %s.mult()... " % self.name, end="", flush=True)
        try:
            tshape = (4, 4)
            vshape = (4, 2)
            X = self.create_random(tshape)
            V = np.asarray(np.random.rand(*vshape))

            assert np.allclose(X.mult(V, 0).to_dense(), X.to_dense().T.dot(V).T)

            tshape = (4, 4, 4)
            X = self.create_random(tshape)
            assert X.mult(V).shape == (2, 2, 2)
            assert X.mult([V, V, V]).shape == (2, 2, 2)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_sum_to_dense(self):
        print("Test %s.sum(to_dense=True)... " % self.name, end="",
              flush=True)
        try:
            X = self.create_empty((2, 2, 2, 2, 2))
            X = X.sum(0, to_dense=True)
            assert X.ndim == 4
            assert X.size == 16

            X = self.create_empty((2, 2, 2, 2))
            X = X.sum([1, 2], to_dense=True)
            assert X.ndim == 2
            assert X.size == 4
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_to_dense(self):
        print("Test %s.to_dense()... " % self.name, end="", flush=True)
        try:
            shape = (2, 2)
            indices = [(0, 0), (0, 1), (1, 0), (1, 1)]
            values = [0, 1, 2, 3]
            assert self.construct_tensor(shape, indices,
                                         values).to_dense() == DenseTensor(
                [[0, 1], [2, 3]])

            ts = self.create_random((3, 3, 3), 0.5)
            td = ts.to_dense()
            assert ts == td
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


class DokTensorTest(unittest.TestCase, CommonTensorTests):
    @property
    def name(self):
        return "DokTensor"

    def create_empty(self, shape):
        return DokTensor(shape, dtype=float)

    def construct_tensor(self, shape, indices, values):
        t = DokTensor(shape)
        for ind, val in zip(indices, values):
            t[ind] = val
        return t

    def create_random(self, shape, fill=0.1):
        all_idx = []
        for s in shape:
            all_idx.append(range(0, s))
        all_idx = list(product(*all_idx))
        shuffle(all_idx)

        size = np.prod(shape)
        nnz = int(size * fill)
        idx = all_idx[0:nnz]
        vals = []
        for _ in range(nnz):
            vals.append(random())
        return CooTensor(idx, vals, shape).to_dok()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal_coo(self):
        print("Test %s.__equal__()... " % self.name, end="", flush=True)
        try:
            shape = (5, 5, 5)
            T = self.create_random(shape)
            T2 = T.copy().to_coo()
            assert T == T2
            T2 = self.create_random(shape).to_coo()
            assert not T == T2
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_innerprod(self):
        print("Test %s.innerprod()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            t = self.create_random(shape, 0.5)
            expected_result = sum(v * v for v in t.values())

            # test with dense
            assert t.innerprod(t.to_dense()) == expected_result
            # test with dok
            assert t.innerprod(t) == expected_result
            # test with coo
            assert t.innerprod(t.to_coo()) == expected_result
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_outerprod(self):
        print("Test %s.outerprod()... " % self.name, end="", flush=True)
        try:
            s = 16
            X = self.create_random((s, s, s), 0.5)
            V = self.create_random((s,), 0.5)
            expected = DenseTensor(
                np.multiply.outer(X.to_dense(), V.to_dense()))
            assert X.outerprod(V.to_dense()) == expected
            assert X.outerprod(V) == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_mult(self):
        print("Test %s.mult()... " % self.name, end="", flush=True)
        try:
            tshape = (4, 4)
            vshape = (4, 2)
            X = self.create_random(tshape)
            V = np.asarray(np.random.rand(*vshape))

            assert np.allclose(X.mult(V, 0).to_dense(), X.to_dense().T.dot(V).T)

            tshape = (4, 4, 4)
            X = self.create_random(tshape)
            assert X.mult(V).shape == (2, 2, 2)
            assert X.mult([V, V, V]).shape == (2, 2, 2)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_sum_to_dense(self):
        print("Test %s.sum(to_dense=True)... " % self.name, end="",
              flush=True)
        try:
            X = self.create_empty((2, 2, 2, 2, 2))
            X = X.sum(0, to_dense=True)
            assert X.ndim == 4
            assert X.size == 16

            X = self.create_empty((2, 2, 2, 2))
            X = X.sum([1, 2], to_dense=True)
            assert X.ndim == 2
            assert X.size == 4
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_to_dense(self):
        print("Test %s.to_dense()... " % self.name, end="", flush=True)
        try:
            shape = (2, 2)
            indices = [(0, 0), (0, 1), (1, 0), (1, 1)]
            values = [0, 1, 2, 3]
            assert self.construct_tensor(shape, indices,
                                         values).to_dense() == DenseTensor(
                [[0, 1], [2, 3]])

            ts = self.create_random((3, 3, 3), 0.5)
            td = ts.to_dense()
            assert ts == td
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_add(self):
        print("Test %s.__add__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            dok_T = self.create_random(shape, fill)
            coo_T = self.create_random(shape, fill).to_coo()
            dense_T = self.create_random(shape, fill).to_dense()

            assert (dok_T + dok_T) == (dok_T.to_dense() + dok_T.to_dense())
            assert (dok_T + coo_T) == (dok_T.to_dense() + coo_T.to_dense())
            assert (dok_T + dense_T) == (dok_T.to_dense() + dense_T)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_iadd(self):
        print("Test %s.__iadd__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill)
            expected = t1.to_dense() + t2.to_dense()
            t1 += t2
            assert t1 == expected

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill).to_coo()
            expected = t1.to_dense() + t2.to_dense()
            t1 += t2
            assert t1 == expected

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill).to_dense()
            expected = t1.to_dense() + t2
            t1 += t2
            assert t1 == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_sub(self):
        print("Test %s.__sub__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            dok_T = self.create_random(shape, fill)
            coo_T = self.create_random(shape, fill).to_coo()
            dense_T = self.create_random(shape, fill).to_dense()

            assert (dok_T - dok_T) == (dok_T.to_dense() - dok_T.to_dense())
            assert (dok_T - coo_T) == (dok_T.to_dense() - coo_T.to_dense())
            assert (dok_T - dense_T) == (dok_T.to_dense() - dense_T)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_isub(self):
        print("Test %s.__isub__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill)
            expected = t1.to_dense() - t2.to_dense()
            t1 -= t2
            assert t1 == expected

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill).to_coo()
            expected = t1.to_dense() - t2.to_dense()
            t1 -= t2
            assert t1 == expected

            t1 = self.create_random(shape, fill)
            t2 = self.create_random(shape, fill).to_dense()
            expected = t1.to_dense() - t2
            t1 -= t2
            assert t1 == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_mul(self):
        print("Test %s.__mul__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            int_val = randint(1, 100)
            float_val = random()

            assert (T * int_val) == (T.to_dense() * int_val)
            assert (T * float_val) == (T.to_dense() * float_val)
            assert (T * 0).nnz == 0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_imul(self):
        print("Test %s.__imul__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)

            val = randint(1, 100)
            expected = T.to_dense() * val
            T *= val
            assert T == expected

            val = random()
            expected = T.to_dense() * val
            T *= val
            assert T == expected

            T *= 0
            assert T.nnz == 0
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_div(self):
        print("Test %s.__div__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            int_val = randint(1, 100)
            float_val = random()

            assert (T / int_val) == (T.to_dense() / int_val)
            assert (T / float_val) == (T.to_dense() / float_val)
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_idiv(self):
        print("Test %s.__idiv__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)

            val = randint(1, 100)
            expected = T.to_dense() / val
            T /= val
            assert T == expected

            val = random()
            expected = T.to_dense() / val
            T /= val
            assert T == expected
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")

    def test_neg(self):
        print("Test %s.__neg__()... " % self.name, end="", flush=True)
        try:
            shape = (4, 4, 4)
            fill = 0.5
            T = self.create_random(shape, fill)
            assert -T == -(T.to_dense())
        except Exception as e:
            print("Failed.")
            raise e
        else:
            print("OK.")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
