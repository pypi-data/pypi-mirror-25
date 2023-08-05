# Author: Michal Ciesielczyk
# Licence: MIT
from scipy.sparse import spmatrix, csr_matrix, coo_matrix, issparse
from functools import reduce
from itertools import islice
from numbers import Number
import collections
import math
import operator
import scipy.sparse
import numpy as np
import tensorcore as tc
from .base import AbstractTensor, AbstractUnfolding
from ._pyutils import check_type
from .matrix_operations import sparse_mult

# SciPy patch
if scipy.__version__ in ("0.14.0", "0.14.1", "0.15.0", "0.15.1", "0.16.0",
                         "0.16.1", "0.17.0"):
    _get_index_dtype = scipy.sparse.sputils.get_index_dtype


    def _my_get_index_dtype(*a, **kw):
        kw.pop('check_contents', None)
        return _get_index_dtype(*a, **kw)


    scipy.sparse.compressed.get_index_dtype = _my_get_index_dtype
    scipy.sparse.csr.get_index_dtype = _my_get_index_dtype
    scipy.sparse.bsr.get_index_dtype = _my_get_index_dtype

MAXPRINT = 50


class CooTensor(AbstractTensor):
    """A sparse tensor in COOrdinate format."""

    _idx = None  # indices
    _vals = None  # values
    _shape = None  # shape
    _issorted = None  # is sorted by indices

    def __init__(self, indices, values, shape, dtype=None, issorted=False,
                 contains_duplicates=False):
        """Create a CooTensor object

        :param indices: list of indices
        :type indices: array_like
        :param values: list of values
        :type values: array_like
        :param shape: tensor shape
        :type shape: tuple of ints or list of ints
        """
        self._shape = tc.base._check_shape(shape)
        check_type("issorted", issorted, bool)
        self._issorted = issorted
        if len(indices) != len(values):
            raise ValueError("The number if indices must be equal to the "
                             "number of values.")
        if len(values) == 0:
            self._idx = np.ndarray(shape=(0, len(shape)), dtype=int)
            self._vals = np.asarray([], dtype=dtype)
        elif contains_duplicates:
            if not issorted:
                if isinstance(indices, list):
                    idx = [x for x, _ in sorted(enumerate(indices),
                                                key=lambda x: x[1])]
                elif isinstance(indices, np.ndarray):
                    idx = [x for x, _ in sorted(enumerate(indices),
                                                key=lambda x: tuple(x[1]))]
                indices = np.asarray(indices)[idx]
                values = np.asarray(values)[idx]
                self._issorted = True
            else:
                indices = np.asarray(indices)
                values = np.asarray(values)
            if indices.ndim == 1:
                indices = indices.reshape(-1, 1)
            idx = np.where(np.diff(indices, axis=0).any(axis=1))[0] + 1
            idx = np.concatenate(([0], idx, [len(indices)]))
            self._vals = np.zeros(len(idx) - 1, dtype=values.dtype)
            for i in range(len(idx) - 1):
                self._vals[i] = np.sum(values[idx[i]:idx[i + 1]])
            self._idx = indices[idx[:-1]]
        else:
            indices = np.asarray(indices)
            if indices.ndim == 1:
                indices = indices.reshape(-1, 1)
            self._idx = indices
            self._vals = np.asarray(values, dtype=dtype)

    @property
    def shape(self):
        """Returns the tensor shape.

        :return: tensor shape
        :rtype: tuple of ints
        """
        return self._shape

    @property
    def dtype(self):
        """Returns the type of data stored in the tensor.

        :return: data type
        :rtype: class
        """
        return self._vals.dtype

    @property
    def nnz(self):
        """Returns the number of non-zero values.

        :return: the number of non-zero values
        :rtype: int
        """
        return len(self._vals)

    def values(self):
        """Returns all values stored in the tensor.

        :return: tensor values
        :rtype: generator object
        """
        for x in self._vals:
            yield x

    def copy(self):
        """Return a copy of the tensor."""
        return CooTensor(self._idx.copy(), self._vals.copy(), self.shape,
                         self.dtype, self._issorted)

    def __iter__(self):
        return iter((tuple(i), v) for i, v in zip(self._idx, self._vals))

    def __eq__(self, other):
        if not isinstance(other, AbstractTensor):
            return False
        if self.shape != other.shape:
            return False

        if isinstance(other, CooTensor):
            if self.nnz != other.nnz:
                return False
            self._sort()
            other._sort()
            return np.array_equal(self._vals, other._vals) and \
                   np.array_equal(self._idx, other._idx)
        if isinstance(other, DokTensor):
            if self.nnz != other.nnz:
                return False
            return all(other[ind] == v for ind, v in self)
        if isinstance(other, tc.dense.DenseTensor):
            return np.array_equal(self.to_dense(), other)

        raise NotImplementedError("Type %s is unsupported for "
                                  "CooTensor.__eq__()." % type(other))

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            for i in range(self.nnz):
                if tuple(self._idx[i]) == idx:
                    return self._vals[i]
        elif self.ndim == 1:
            if isinstance(idx, (int, np.integer)):
                for i in range(self.nnz):
                    if self._idx[i, 0] == idx:
                        return self._vals[i]
            else:
                raise TypeError("Given index must be a tuple or an integer, "
                                "not a {}.".format(type(idx)))
        else:
            raise TypeError("Given index must be a tuple, not a {}.".
                            format(type(idx)))
        return 0.0

    def __mul__(self, other):  # self * other
        check_type("other", other, Number)
        if other == 0 or self.nnz == 0:
            return CooTensor([], [], self.shape, self.dtype, issorted=True)
        X = self.copy()
        X._vals = X._vals * other
        return X

    def __imul__(self, other):
        check_type("other", other, Number)
        if other == 0:
            self._idx = np.ndarray(shape=(0, self.ndim), dtype=int)
            self._vals = np.array([], self.dtype)
            self._issorted = True
        else:
            self._vals *= other
        return self

    def __truediv__(self, other):  # self / other
        check_type("other", other, Number)
        X = self.copy()
        X._vals = X._vals / other
        return X

    def __itruediv__(self, other):
        check_type("other", other, Number)
        self._vals /= other
        return self

    def __neg__(self):
        X = self.copy()
        X._vals = -self._vals
        return X

    # right side operations
    __rmul__ = __mul__

    def _sort(self):
        if self._issorted or self.nnz == 0:
            return
        sidx = np.lexsort(self._idx.T)
        # sidx = [x for x, _ in sorted(enumerate(self._idx),
        #                            key=lambda x: tuple(x[1]))]
        self._idx = self._idx[sidx]
        self._vals = self._vals[sidx]
        self._issorted = True

    def innerprod(self, other):
        """Returns the inner product with another tensor

        :return: the inner product with another tensor
        :rtype: dtype
        """
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            return ValueError("Tensor shapes does not match (%s != %s)."
                              % (self.shape, other.shape))

        if isinstance(other, tc.dense.DenseTensor):
            return np.sum(v * other[ind] for ind, v in self)
        if isinstance(other, DokTensor):
            return np.sum(v * other[ind] for ind, v in self)
        if isinstance(other, CooTensor):
            return np.sum(v * other[ind] for ind, v in self)

        raise NotImplementedError("Type %s is unsupported for "
                                  "DokTensor.innerprod()." % type(other))

    def outerprod(self, vector):
        """Returns the outer product with the specified vector."""
        if not isinstance(vector, (np.ndarray, DokTensor, CooTensor)):
            raise TypeError("Given vector must be a numpy.ndarray or a sparse "
                            "tensor (CooTensor or DokTensor), not %s."
                            % type(vector))
        if len(vector.shape) != 1:
            raise ValueError("vector parameter must be a vector (1-mode "
                             "tensor), not a %d-mode tensor."
                             % len(vector.shape))
        N = vector.shape[0]
        new_shape = self.shape + (N,)
        new_idx = []
        new_vals = []
        if isinstance(vector, np.ndarray):
            for i in range(N):
                vi = vector[i]
                if vi == 0.0:
                    continue
                for ind, val in self:
                    new_idx.append(ind + (i,))
                    new_vals.append(val * vi)
        else:
            for v_ind, v_val in vector:
                for t_ind, t_val in self:
                    new_idx.append(t_ind + v_ind)
                    new_vals.append(t_val * v_val)
        return CooTensor(new_idx, new_vals, new_shape, self.dtype)

    def mult(self, V, mode=None, transpose=False):
        """Multiplies the tensor with matrix along specified mode.

        :param V: matrix or a list of matrices
        :type V: matrix object or list
        :param mode: modes along which the multiplication should be performed,
            by default the tensor is multiplied along mode 0 (if mode parameter
            is an int) or along all modes (if mode parameter is a list)
        :type mode: int or list of ints, optional
        :param transpose: indicates whether the matrices in V should be
            transposed before multiplication, by default False
        :type transpose: boolean, optional
        :return: tensor multiplied with matrices along specified modes
        :rtype: tensor object
        """
        if mode is not None:
            check_type("mode", mode, (int, np.integer, list, tuple))
        if not isinstance(V, (list, tuple)):
            V = [V]
        for v in V:
            if not isinstance(v, (np.ndarray, spmatrix)):
                raise TypeError("V parameter must be a matrix or a list of "
                                "matrices.")

        X = self
        if mode is None:
            if len(V) == 1:
                for i in range(self.ndim):
                    X = X._mult(V[0], i, transpose)
                return X
            elif len(V) == self.ndim:
                for i in range(self.ndim):
                    X = X._mult(V[i], i, transpose)
                return X
            else:
                raise ValueError("Invalid number of matrices given (%d)."
                                 % len(V))
        elif isinstance(mode, (int, np.integer)):
            mode = [mode]
        elif len(mode) != len(V):
            raise ValueError("Modes defined in mode parameter must correspond "
                             "to matrices in V.")

        for i in range(len(mode)):
            X = X._mult(V[i], mode[i], transpose)
        return X

    def _mult(self, V, mode, transpose=False):
        if transpose:
            V = V.T
        shape = list(self.shape)
        shape[mode] = V.shape[1]

        # TODO: optimize and move to tc.matrix_operations.sparse_mult
        Z = self.unfold(mode, transpose=True)
        try:
            if self.nnz < 10 ** 4 or self.size > 5 * 10 ** 10:
                Z = sparse_mult(Z, V)
            elif self.nnz / self.size < 0.1 or self.size > 10 ** 8:
                Z = Z.tocsr().dot(csr_matrix(V))
            else:
                Z = Z.tocsr().dot(V)
        except MemoryError as e:
            raise Exception("Failed to multiply sparse matrix(size: %d and "
                            "nnz: %d) with another matrix(size: %d)" %
                            (self.size, self.nnz, V.size)) from e
        if issparse(Z):
            Z = Z.tocoo().T
            return CooUnfolding(Z.shape, Z.data, Z.row, Z.col,
                                [mode], None, tuple(shape)).fold()
        else:
            return tc.dense.DenseUnfolding(Z.T, mode, tuple(shape)).fold()

    def norm(self):
        """Returns the Frobenius norm of the tensor.

        :return: the Frobenius norm of the tensor.
        :rtype: float
        """
        return np.linalg.norm(self._vals)

    def sum(self, mode=None, to_dense=False):
        """Returns a flattened tensor along the specified modes.

        :param mode: Mode (or tuple of modes) along  which the tensor is
            flattened
        :type mode: int or tuple of ints, by default 0
        :param to_dense: if true, a dense tensor is returned
        :type to_dense: boolean
        :return: Tensor flattened along specified modes
        :rtype: tensor object
        """
        if mode is None or (isinstance(mode, tuple) and
                                    sorted(mode) == list(range(self.ndim))):
            return np.sum(self.values())
        if isinstance(mode, (int, np.integer)):
            mode = (mode,)
        if len(mode) == 0:
            return self.to_dense() if to_dense else self
        modes_left = np.setdiff1d(range(self.ndim), mode)

        new_shape = tuple(self.shape[m] for m in modes_left)
        if to_dense:
            ftensor = tc.dense.DenseTensor.zeros(new_shape)
            for ind, v in zip(self._idx, self._vals):
                ind = tuple(ind[m] for m in modes_left)
                ftensor[ind] += v
            return ftensor
        else:
            ftensor = DokTensor(new_shape, self.dtype)
            for ind, v in zip(self._idx, self._vals):
                ind = tuple(ind[m] for m in modes_left)
                ftensor[ind] += v
            return ftensor.to_coo()

    def vectorize(self):
        """Return a copy of the tensor collapsed into one dimension.

        :return: A copy of the tensor, vectorized to one dimension.
        :rtype: tensor object
        """
        size_factors = [reduce(operator.mul, self.shape[i:])
                        for i in range(1, self.ndim)]
        v_indices = np.zeros(self.nnz)
        for i, (ind, _) in enumerate(self):
            v_indices[i] = sum(ind[n] * size_factors[n]
                               for n in range(self.ndim))
        return CooTensor(v_indices, self._vals.copy(), self.shape,
                         dtype=self.dtype, issorted=self._issorted)

    def transpose(self, modes=None):
        """Returns the tensor with permuted modes.

        :param modes: By default, reverse the mode order, otherwise permute the
            modes according to the values given.
        :type modes: list of ints, optional
        :return: tensor with its modes permuted. A view is returned whenever
            possible.
        :rtype: tensor object
        """
        if modes is None:
            modes = list(reversed(range(self.ndim)))
        else:
            check_type("modes", modes, list)
        new_shape = []
        for i in range(len(self._shape)):
            new_shape.append(self._shape[modes[i]])
        new_idx = np.empty_like(self._idx)
        for i in range(len(self._idx)):
            for j in range(len(self._shape)):
                new_idx[i][j] = self._idx[i][modes[j]]

        return CooTensor(new_idx, self._vals, tuple(new_shape), self.dtype)

    def assign(self, func):
        """Assigns the result of a function to each element of the tensor T:
            T[i] = func(T[i]).

        Example:
        # tensor = [[0 1] [2 3]]
        tensor.assign(lambda t: t+1)
        --> [[1 2] [3 4]]

        :param func: a function object taking as argument the current
            element's value.
        :type func: function
        """
        self._vals[:] = [func(x) for x in self._vals]

    def unfold(self, mode, transpose=False):
        """Unfolds the tensor along specified modes.

        :param mode: Mode (or list of modes) along  which the tensor is
            unfolded
        :type mode: int or list of ints
        :return: Tensor unfolding along specified modes
        :rtype: unfolding object
        """
        if isinstance(mode, (int, np.integer)):
            mode = [mode]
        if transpose:
            row_modes = np.setdiff1d(range(self.ndim), mode)[::-1]
            col_modes = mode
        else:
            row_modes = mode
            col_modes = np.setdiff1d(range(self.ndim), mode)[::-1]
        unfolding_shape = (np.prod([self.shape[r] for r in row_modes],
                                   dtype=np.int64),
                           np.prod([self.shape[c] for c in col_modes],
                                   dtype=np.int64))
        row_idx = _build_idx(self._idx, row_modes, self.shape)
        col_idx = _build_idx(self._idx, col_modes, self.shape)
        return CooUnfolding(unfolding_shape, self._vals, row_idx, col_idx,
                            row_modes, col_modes, self.shape)

    def to_dense(self, copy=False):
        dense_t = tc.dense.DenseTensor(np.zeros(self.shape))
        for k, v in self:
            dense_t[k] = v
        return dense_t

    def to_dok(self):
        dok_t = DokTensor(self._shape, self.dtype)
        for k, v in self:
            dok_t[k] = v
        return dok_t

    def __str__(self):
        maxprint = MAXPRINT

        # helper function, outputs "(index)  v"
        def tostr(indices, values):
            triples = zip(indices, values)
            return '\n'.join([('  %s\t%s' % (tuple(ind), v))
                              if isinstance(ind, collections.Iterable)
                              else ('  %s\t%s' % ((ind,), v))
                              for ind, v in triples])

        if self.nnz > maxprint:
            half = maxprint // 2
            out = tostr(self._idx[:half], self._vals[:half])
            out += "\n  :\t:\n"
            half = maxprint - maxprint // 2
            out += tostr(self._idx[-half:], self._vals[-half:])
        else:
            out = tostr(self._idx, self._vals)

        return out


class CooUnfolding(coo_matrix, AbstractUnfolding):
    """Unfolded sparse tensor in COOrdinate format class (CooTensor)."""

    def __init__(self, shape, values, row_indices, col_indices, row_modes,
                 col_modes, tensor_shape, dtype=None, copy=False):
        self.tensor_shape = np.array(tensor_shape)
        if col_modes is None:
            col_modes = np.setdiff1d(range(len(self.tensor_shape)),
                                     row_modes)[::-1]
        self.row_modes = row_modes
        self.col_modes = col_modes
        super(CooUnfolding, self).__init__(
            (values, (row_indices, col_indices)), shape=shape, dtype=dtype,
            copy=copy)

    def fold(self):
        nsubs = np.zeros((len(self.data), len(self.tensor_shape)),
                         dtype=np.int)
        if len(self.row_modes) > 0:
            nidx = np.unravel_index(self.row,
                                    self.tensor_shape[self.row_modes])
            for i in range(len(self.row_modes)):
                nsubs[:, self.row_modes[i]] = nidx[i]
        if len(self.col_modes) > 0:
            nidx = np.unravel_index(self.col,
                                    self.tensor_shape[self.col_modes])
            for i in range(len(self.col_modes)):
                nsubs[:, self.col_modes[i]] = nidx[i]
        return CooTensor(nsubs, self.data, self.tensor_shape, self.dtype)


class DokTensor(AbstractTensor):
    """Dictionary Of Keys based sparse tensor."""

    _dok = None
    _shape = None
    _dtype = None

    def __init__(self, shape, dtype=None, dok=None):
        """Create a DokTensor object

        :param shape: tensor shape
        :type shape: tuple of ints or list of ints
        """
        self._shape = tc.base._check_shape(shape)
        self._dtype = dtype
        self._dok = {} if dok is None else dok

    @property
    def shape(self):
        """Returns the tensor shape.

        :return: tensor shape
        :rtype: tuple of ints
        """
        return self._shape

    def resize(self, new_shape):
        """Gives a new shape to a sparse matrix without changing its data.

        :param new_shape: The new shape should be compatible with the maximum
            indices on corresponding modes.
        :type new_shape: tuple of ints
        :return: `self` with the new dimensions of `shape`
        """
        new_shape = tc.base._check_shape(new_shape)
        if len(new_shape) != self.ndim:
            raise ValueError("Invalid shape length (%d)." % len(new_shape))
        data_shape = [1 for _ in range(self.ndim)]
        for idx in self._dok:
            for m, i in enumerate(idx):
                if data_shape[m] <= i:
                    data_shape[m] = i + 1
        for m in range(self.ndim):
            if new_shape[m] < data_shape[m]:
                raise ValueError("Data indices on mode {} exceed the new "
                                 "shape.".format(m))
        self._shape = new_shape

    @property
    def dtype(self):
        """Returns the type of data stored in the tensor.

        :return: data type
        :rtype: class
        """
        if self._dtype is None and self.nnz > 0:
            self._dtype = type(next(iter(self._dok.values())))
        return self._dtype

    @property
    def nnz(self):
        """Returns the number of non-zero values.

        :return: the number of non-zero values
        :rtype: int
        """
        return len(self._dok)

    def copy(self):
        """Return a copy of the tensor."""
        return DokTensor(self.shape, self.dtype, self._dok.copy())

    def __iter__(self):
        return iter(self._dok.items())

    def __eq__(self, other):
        if not isinstance(other, AbstractTensor):
            return False
        if self.shape != other.shape:
            return False

        if isinstance(other, DokTensor):
            return self._dok == other._dok
        if isinstance(other, CooTensor):
            if self.nnz != other.nnz:
                return False
            return all(self[ind] == v for ind, v in other)
        if isinstance(other, tc.dense.DenseTensor):
            return np.array_equal(self.to_dense(), other)

        raise NotImplementedError("Type %s is unsupported for "
                                  "DokTensor.__eq__()." % type(other))

    def __getitem__(self, idx):
        if isinstance(idx, (int, np.integer)):
            idx = (idx,)
        assert isinstance(idx, tuple), "idx must be a tuple or an integer."
        assert self.ndim == len(idx), "Number of modes in idx does not " \
                                      "match the shape of the tensor."
        assert all(0 <= idx[m] < self.shape[m] for m in range(self.ndim)), \
            "One of the indices ({}) exceeds the tensor shape ({}).".format(
                idx, self.shape)
        if idx in self._dok:
            return self._dok[idx]
        return 0.0

    def __setitem__(self, idx, val):
        if isinstance(idx, (int, np.integer)):
            idx = (idx,)
        assert isinstance(idx, tuple), "idx must be a tuple or an integer."
        assert self.ndim == len(idx), "Number of modes in idx does not " \
                                      "match the shape of the tensor."
        assert all(0 <= idx[m] < self.shape[m] for m in range(self.ndim)), \
            "One of the indices ({}) exceeds the tensor shape ({}).".format(
                idx, self.shape)
        assert (self.dtype is None or type(val) == self.dtype or
                self.dtype.type(val)), "val argument must be compatible " \
                                       "with tensor dtype."
        self._dok[idx] = val

    def __add__(self, other):  # self + other
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, tc.dense.DenseTensor):
            X = other.copy()
            for ind, val in self:
                X[ind] += val
            return X
        elif isinstance(other, (CooTensor, DokTensor)):
            X = self.copy()
            for ind, val in other:
                X[ind] += val
            return X
        else:
            raise NotImplementedError("Type %s is unsupported for "
                                      "DokTensor.__add__()." % type(other))

    def __iadd__(self, other):
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, (CooTensor, DokTensor, tc.dense.DenseTensor)):
            for ind, val in other:
                self[ind] += val
            return self

        raise NotImplementedError("Type %s is unsupported for "
                                  "DokTensor.__iadd__()." % type(other))

    def __sub__(self, other):  # self - other
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, (tc.dense.DenseTensor)):
            X = -other.copy()
            for ind, val in self:
                X[ind] += val
            return X
        elif isinstance(other, (DokTensor, CooTensor)):
            X = self.copy()
            for ind, val in other:
                X[ind] -= val
            return X
        else:
            raise NotImplementedError("Type %s is unsupported for "
                                      "DokTensor.__sub__()." % type(other))

    def __rsub__(self, other):  # other - self
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, (tc.dense.DenseTensor)):
            X = other.copy()
            for ind, val in self:
                X[ind] -= val
            return X
        elif isinstance(other, DokTensor):
            X = other.copy()
            for ind, val in self:
                X[ind] -= val
            return X
        elif isinstance(other, CooTensor):
            X = -self
            for ind, val in other:
                X[ind] += val
            return X.to_coo()
        else:
            raise NotImplementedError("Type %s is unsupported for "
                                      "DokTensor.__rsub__()." % type(other))

    def __isub__(self, other):
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, (CooTensor, DokTensor, tc.dense.DenseTensor)):
            for ind, val in other:
                self[ind] -= val
            return self

        raise NotImplementedError("Type %s is unsupported for "
                                  "DokTensor.__isub__()." % type(other))

    def __mul__(self, other):
        check_type("other", other, Number)
        if other == 0:
            return DokTensor(self.shape, self.dtype)
        X = self.copy()
        for ind in self._dok:
            X[ind] *= other
        return X

    def __imul__(self, other):
        check_type("other", other, Number)
        if other == 0:
            self._dok.clear()
        else:
            for ind in self._dok:
                self[ind] *= other
        return self

    def __truediv__(self, other):
        check_type("other", other, Number)
        X = self.copy()
        for ind in self._dok:
            X[ind] /= other
        return X

    def __itruediv__(self, other):
        check_type("other", other, Number)
        for ind in self._dok:
            self[ind] /= other
        return self

    def __neg__(self):
        X = self.copy()
        for ind, val in self:
            X[ind] = -val
        return X

    # right side operations
    __radd__ = __add__
    __rmul__ = __mul__

    def innerprod(self, other):
        """Returns the inner product with another tensor

        :return: the inner product with another tensor
        :rtype: dtype
        """
        check_type("other", other, AbstractTensor)
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, tc.dense.DenseTensor):
            return np.sum(v * other[ind] for ind, v in self)
        if isinstance(other, DokTensor):
            return np.sum(v * other[ind] for ind, v in self)
        if isinstance(other, CooTensor):
            return np.sum(v * self[ind] for ind, v in other)

        raise NotImplementedError("Type %s is unsupported for "
                                  "DokTensor.innerprod()." % type(other))

    def values(self):
        """Returns all values stored in the tensor.

        :return: tensor values
        :rtype: generator object
        """
        return (v for v in self._dok.values())

    def outerprod(self, vector):
        """Returns the outer product with the specified vector."""
        if not isinstance(vector, (np.ndarray, DokTensor, CooTensor)):
            raise TypeError("Given vector must be a numpy.ndarray or a sparse "
                            "tensor (CooTensor or DokTensor), not %s."
                            % type(vector))
        if len(vector.shape) != 1:
            raise ValueError("vector parameter must be a vector (1-mode "
                             "tensor), not {}-mode tensor.".format(
                len(vector.shape)))
        N = vector.shape[0]
        new_shape = self.shape + (N,)
        new_dok = {}
        if isinstance(vector, np.ndarray):
            for i in range(N):
                vi = vector[i]
                if vi == 0.0:
                    continue
                for ind, val in self:
                    new_dok[ind + (i,)] = val * vi
        else:
            for v_ind, v_val in vector:
                for t_ind, t_val in self:
                    new_dok[t_ind + v_ind] = t_val * v_val
        return DokTensor(new_shape, self.dtype, new_dok)

    def mult(self, V, mode=None, transpose=False):
        """Multiplies the tensor with matrix along specified mode.

        :param V: matrix or a list of matrices
        :type V: matrix object or list
        :param mode: modes along which the multiplication should be performed,
            by default the tensor is multiplied along mode 0 (if mode parameter
            is an int) or along all modes (if mode parameter is a list)
        :type mode: int or list of ints, optional
        :param transpose: indicates whether the matrices in V should be
            transposed before multiplication, by default False
        :type transpose: boolean, optional
        :return: tensor multiplied with matrices along specified modes
        :rtype: tensor object
        """
        if mode is not None:
            check_type("mode", mode, (int, np.integer, list, tuple))
        if not isinstance(V, (list, tuple)):
            V = [V]
        for v in V:
            if not isinstance(v, (np.ndarray, spmatrix)):
                raise TypeError("V parameter must be a matrix or a list of "
                                "matrices.")
        X = self
        if mode is None:
            if len(V) == 1:
                for i in range(self.ndim):
                    X = X._mult(V[0], i, transpose)
                return X
            elif len(V) == self.ndim:
                for i in range(self.ndim):
                    X = X._mult(V[i], i, transpose)
                return X
            else:
                raise ValueError("Invalid number of matrices given (%d)"
                                 % len(V))

        if isinstance(mode, (int, np.integer)):
            mode = [mode]
        if len(mode) != len(V):
            raise ValueError("Modes defined in mode parameter must correspond "
                             "to matrices in V.")
        X = self
        for i in range(len(mode)):
            X = X._mult(V[i], mode[i], transpose)
        return X

    def _mult(self, V, mode, transpose=False):
        shape = list(self.shape)
        shape[mode] = V.shape[1]

        # TODO: optimize and move to tc.matrix_operations.sparse_mult
        Z = self.unfold(mode, transpose=True)
        if transpose:
            V = V.T
        try:
            if self.nnz < 10 ** 4 or self.size > 5 * 10 ** 10:
                Z = sparse_mult(Z, V)
            elif self.nnz / self.size < 0.1 or self.size > 10 ** 8:
                Z = Z.tocsr().dot(csr_matrix(V))
            else:
                Z = Z.tocsr().dot(V)
        except MemoryError as e:
            raise Exception(
                "Failed to multiply sparse matrix(size: %d and nnz: %d) with "
                "another matrix(size: %d)" % (
                self.size, self.nnz, V.size)) from e
        if issparse(Z):
            Z = Z.tocoo().T
            return CooUnfolding(Z.shape, Z.data, Z.row, Z.col, [mode],
                                None, tuple(shape)).fold().to_dok()
        else:
            return tc.dense.DenseUnfolding(Z.T, mode, tuple(shape)).fold()

    def norm(self):
        """Returns the Frobenius norm of the tensor.

        :return: the Frobenius norm of the tensor.
        :rtype: float
        """
        return math.sqrt(np.sum(x * x for x in self.values()))

    def sum(self, mode=None, to_dense=False):
        """Returns a flattened tensor along the specified modes.

        :param mode: Mode (or list of modes) along  which the tensor is
            flattened
        :type mode: int or list of ints, by default 0
        :param to_dense: if true, a dense tensor is returned
        :type to_dense: boolean
        :return: Tensor flattened along specified modes
        :rtype: tensor object
        """
        if mode is None or (isinstance(mode, tuple) and
                                    sorted(mode) == list(range(self.ndim))):
            return sum(self.values())
        if isinstance(mode, (int, np.integer)):
            mode = (mode,)
        elif len(mode) == 0:
            return self.to_dense() if to_dense else self
        modes_left = np.setdiff1d(range(self.ndim), mode)

        new_shape = tuple(self.shape[m] for m in modes_left)
        if to_dense:
            ftensor = tc.dense.DenseTensor.zeros(new_shape)
            for ind, v in self:
                ind = tuple(ind[m] for m in modes_left)
                ftensor[ind] += v
            return ftensor
        else:
            ftensor = DokTensor(new_shape, self.dtype)
            for ind, v in self:
                ind = tuple(ind[m] for m in modes_left)
                ftensor[ind] += v
            return ftensor

    def vectorize(self):
        """Return a copy of the tensor collapsed into one dimension.

        :return: A copy of the tensor, vectorized to one dimension.
        :rtype: tensor object
        """
        size_factors = [reduce(operator.mul, self.shape[i:])
                        for i in range(1, self.ndim)]
        new_dok = {}
        for ind, val in self:
            new_dok[sum(ind[n] * size_factors[n]
                        for n in range(self.ndim))] = val
        return DokTensor((self.size,), dtype=self.dtype, dok=new_dok)

    def transpose(self, modes=None):
        """Returns the tensor with permuted modes.

        :param modes: By default, reverse the mode order, otherwise permute the
            modes according to the values given.
        :type modes: list of ints, optional
        :return: tensor with its modes permuted. A view is returned whenever
            possible.
        :rtype: tensor object
        """
        if modes is None:
            modes = list(reversed(range(self.ndim)))
        else:
            check_type("modes", modes, list)
        new_shape = []
        for i in range(len(self._shape)):
            new_shape.append(self._shape[modes[i]])
        new_dok = {}
        for ind, v in self:
            new_ind = tuple(ind[modes[i]] for i in range(len(self._shape)))
            new_dok[new_ind] = v

        return DokTensor(tuple(new_shape), self.dtype, new_dok)

    def assign(self, func):
        """Assigns the result of a function to each element of the tensor T:
            T[i] = func(T[i]).

        Example:
        # tensor = [[0 1] [2 3]]
        tensor.assign(lambda t: t+1)
        --> [[1 2] [3 4]]

        :param func: a function object taking as argument the current
            element's value.
        :type func: Callable
        """
        for key, value in self:
            self._dok[key] = func(value)

    def unfold(self, mode, transpose=False):
        """Unfolds the tensor along specified modes.

        :param mode: Mode (or list of modes) along  which the tensor is
            unfolded
        :type mode: int or list of ints
        :return: Tensor unfolding along specified modes
        :rtype: unfolding object
        """
        return self.to_coo().unfold(mode, transpose)

    def to_dense(self, copy=False):
        dense_t = tc.dense.DenseTensor(np.zeros(self.shape))
        for k, v in self:
            dense_t[tuple(k)] = v
        return dense_t

    def to_coo(self):
        return CooTensor(list(self._dok.keys()), list(self._dok.values()),
                         self.shape, self.dtype)

    def __str__(self):
        maxprint = MAXPRINT

        # helper function, outputs "(index)  v"
        def tostr(indices, values):
            triples = zip(indices, values)
            return '\n'.join([('  %s\t%s' % (tuple(ind), v))
                              for ind, v in triples])

        if self.nnz > maxprint:
            ind_vals = list(zip(*islice(self, maxprint)))
            out = tostr(ind_vals[0], ind_vals[1])
            out += "\n  ...\t...\n"
        else:
            out = tostr(list(self._dok.keys()), list(self._dok.values()))

        return out


def is_sparse(tensor_object):
    return isinstance(tensor_object, (CooTensor, DokTensor))


def _build_idx(idx, modes, tshape):
    if len(idx) == 0:
        return np.array(tuple())
    else:
        multi_index = tuple([idx[:, i] for i in modes])
        shape = tuple([tshape[d] for d in modes])
        size = np.prod(shape, dtype=np.int64)
        if size > 2 ** 31:
            return _ravel_multi_index(multi_index, shape)
        else:
            return np.ravel_multi_index(multi_index, shape)


def _ravel_multi_index(multi_index, dims):
    mdims = np.ones((len(dims)), dtype=np.int64)
    for i in range(len(dims) - 1, 0, -1):
        mdims[i - 1] = mdims[i] * dims[i]
    size = len(multi_index[0])
    ndim = len(multi_index)
    return [sum(mdims[d] * multi_index[d][i]
                for d in range(ndim)) for i in range(size)]
