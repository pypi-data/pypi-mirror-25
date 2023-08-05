# Author: Michal Ciesielczyk
# Licence: MIT
from scipy.sparse.base import spmatrix
import numpy as np
import tensorcore as tc
from ._pyutils import range_without, check_type
from .base import AbstractTensor, AbstractUnfolding


class DenseTensor(np.ndarray, AbstractTensor):
    """Dense tensor class based on a numpy array implementation.

    Example:
    t = DenseTensor(input_array=[0, 1, 2, 3] dtype=int)
    """

    """Creates a new DenseTensor object.

    :param input_array: Input data, in any form that can be converted to a
        tensor.  This includes lists, lists of tuples, tuples, tuples of
        tuples, tuples of lists and ndarrays.
    :type input_array: array_like
    :param dtype: By default, the data-type is inferred from the input data.
    :type dtype: data-type, optional
    """

    def __new__(cls, input_array, dtype=None):
        obj = np.asarray(input_array, dtype=dtype).view(cls)
        return obj

    def __eq__(self, other):
        if not isinstance(other, AbstractTensor):
            return False
        if self.shape != other.shape:
            return False

        if isinstance(other, DenseTensor):
            return np.array_equal(self, other)
        if isinstance(other, tc.sparse.CooTensor):
            return np.array_equal(self, other.to_dense())
        if isinstance(other, tc.sparse.DokTensor):
            return np.array_equal(self, other.to_dense())

        raise NotImplementedError("Type %s is unsupported for "
                                  "DenseTensor.__eq__()." % type(other))

    @property
    def nnz(self):
        """Returns the number of non-zero values.

        :return: the number of non-zero values
        :rtype: int
        """
        nnz = 0
        for v in np.nditer(self):
            if v != 0:
                nnz += 1
        return nnz

    class DenseTensorIter:

        def __init__(self, multi_index_nditer):
            self.__it = multi_index_nditer

        def __iter__(self):
            return self

        def __next__(self):
            while not self.__it.finished:
                result = self.__it.multi_index, self.__it[0].item()
                self.__it.iternext()
                return result
            raise StopIteration

    def __iter__(self):
        return self.DenseTensorIter(np.nditer(self, flags=['multi_index']))

    def values(self):
        """Returns all values stored in the tensor.

        :return: tensor values
        :rtype: generator object
        """
        for x in np.nditer(self):
            yield x.item()

    def innerprod(self, other):
        """Returns the inner product with another tensor

        :param other: tensor
        :type other: AbstractTensor
        :return: the inner product with another tensor
        :rtype: dtype
        """
        if not isinstance(other, AbstractTensor):
            raise TypeError("other (%s given) must implement the "
                            "AbstractTensor class." % type(other))
        if self.shape != other.shape:
            raise ValueError("Tensor shapes does not match (%s != %s)."
                             % (self.shape, other.shape))

        if isinstance(other, DenseTensor):
            return (self * other).sum()
        if tc.sparse.is_sparse(other):
            return np.sum(v * self[ind] for ind, v in other)

        raise NotImplementedError("Type %s is unsupported for "
                                  "DenseTensor.innerprod()." % type(other))

    def outerprod(self, vector):
        """Returns the outer product with a vector.

        :param vector: vector
        :type vector: numpy.ndarray
        :return: tensor object
        :rtype: DenseTensor
        """
        check_type("vector", vector, np.ndarray)
        if len(vector.shape) == 1:
            # tensor vector outer product
            return self[..., np.newaxis] * vector[np.newaxis, ...]
        raise ValueError("vector parameter must be a vector.")

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
        if not (mode is None or
                    isinstance(mode, (int, np.integer, list, tuple))):
            raise TypeError("mode parameter must be an int, list, tuple or "
                            "None, not %s" % type(mode))
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
        shape[mode] = V.shape[0]
        if transpose:
            shape[mode] = V.shape[0]
            return DenseUnfolding(V.dot(self.unfold(mode)), mode,
                                  tuple(shape)).fold()
        else:
            shape[mode] = V.shape[1]
            return DenseUnfolding(V.T.dot(self.unfold(mode)), mode,
                                  tuple(shape)).fold()

    def norm(self):
        """Returns the Frobenius norm of the tensor.

        :return: the Frobenius norm of the tensor.
        :rtype: float
        """
        return np.linalg.norm(self)

    def sum(self, mode=None, *args, **kwargs):
        """Returns a flattened tensor along the specified modes.

        :param mode: Mode (or tuple of modes) along  which the tensor is
            flattened
        :type mode: int or tuple of ints, by default 0
        :return: Tensor flattened along specified modes
        :rtype: DenseTensor
        """
        if mode is None and 'axis' in kwargs:
            mode = kwargs['axis']
        if mode is None or (isinstance(mode, tuple) and
                                    sorted(mode) == list(range(self.ndim))):
            return np.ndarray.sum(self, axis=mode).item()
        return np.ndarray.sum(self, axis=mode)

    def vectorize(self):
        """Return a copy of the tensor collapsed into one dimension.

        :return: A copy of the tensor, vectorized to one dimension.
        :rtype: tensor object
        """
        return np.ndarray.flatten(self)

    def transpose(self, modes=None):
        """Returns the tensor with permuted modes.

        :param modes: By default, reverse the mode order, otherwise permute the
            modes according to the values given.
        :type modes: list of ints, optional
        :return: tensor with its modes permuted. A view is returned whenever
            possible.
        :rtype: DenseTensor
        """
        return DenseTensor(np.transpose(np.array(self), axes=modes))

    def assign(self, func):
        """Assigns the result of a function to each element of the tensor T;
            T[i] = function(T[i]).

        Example:
        # tensor = [[0 1] [2 3]]
        tensor.assign(lambda t: t+1)
        --> [[1 2] [3 4]]

        :param func: a function object taking as argument the current
            element's value.
        :type func: Callable
        :return: self (for convenience only)
        :rtype: DenseTensor
        """
        for x in np.nditer(self, op_flags=['readwrite']):
            x[...] = func(x)

    def center(self, mode=None):
        """Centers this tensor by removing the global or mode specific average.

        :param mode: Mode along  which the tensor is centered or None for
            removing the global average from each tensor cell.
        :type mode: int
        """
        if mode is None:
            avg = self.sum() / self.size
            self -= avg
        else:
            size = self.shape[mode]
            for i in range(size):
                avg = self.swapaxes(0, mode)[i].sum() / (self.size / size)
                self.swapaxes(0, mode)[i] -= avg

    def to_dense(self, copy=False):
        if copy:
            return self.copy()
        else:
            return self

    def unfold(self, mode):
        """Unfolds the tensor along specified modes.

        :param mode: Mode (or list of modes) along  which the tensor is
            unfolded
        :type mode: int or list of ints
        :return: Tensor unfolding along specified modes
        :rtype: DenseUnfolding
        """
        shape = np.array(self.shape)
        if isinstance(mode, (int, np.integer)):
            mode = [mode]
        if not isinstance(mode, list):
            raise TypeError("mode parameter must be an in or list of ints, "
                            "not %s." % type(mode))
        order = (mode, list(range_without(0, self.ndim, mode, reverse=True)))
        shape = (np.prod(shape[order[0]], dtype=np.int64),
                 np.prod(shape[order[1]], dtype=np.int64))
        arr = self.transpose(modes=(order[0] + order[1]))
        arr = arr.reshape(shape)
        return DenseUnfolding(arr, mode, self.shape)

    @staticmethod
    def zeros(shape, dtype=None):
        """Return a new dense tensor of given shape and type, filled with zeros.

        :param shape: shape of the returned tensor
        :type shape: tuple
        :return: tensor object
        :rtype: DenseTensor
        """
        if not isinstance(shape, tuple):
            raise TypeError("shape parameter has to be a tuple, not a %s."
                            % type(shape))
        if dtype is None:
            return DenseTensor(np.zeros(shape))
        return DenseTensor(np.zeros(shape, dtype))

    @staticmethod
    def random(shape):
        """Return a new Tensor of given shape and type, filled with random samples
        from a uniform distribution over ``[0, 1)``.

        :param shape: shape of the returned tensor
        :type shape: tuple
        """
        shape = tc.base._check_shape(shape)
        return DenseTensor(np.random.rand(*shape))


class DenseUnfolding(np.ndarray, AbstractUnfolding):
    """Unfolded tensor class

    :param input_array: 2-dimensional ndarrays, representing the unfolded
        tensor data
    :type input_array: array_like
    :param mode: Mode (or list of modes) along  which the tensor was unfolded
    :type mode: int or list of ints
    :param tensor_shape: original tensor shape
    :type tensor_shape: int
    """

    def __new__(cls, input_array, mode, tensor_shape):
        obj = np.asarray(input_array).view(cls)
        obj.tensor_shape = tensor_shape
        if isinstance(mode, (int, np.integer)):
            mode = [mode]
        obj.mode = mode
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.tensor_shape = getattr(obj, 'tensor_shape', None)
        self.mode = getattr(obj, 'mode', None)

    def fold(self):
        """Restore a matrix into a tensor"""
        shape = np.array(self.tensor_shape)
        order = (self.mode, list(range_without(0, len(shape), self.mode,
                                               reverse=True)))
        arr = self.reshape(tuple(shape[order[0]], ) + tuple(shape[order[1]]))
        arr = np.transpose(arr, np.argsort(order[0] + order[1]))
        return DenseTensor(arr)
