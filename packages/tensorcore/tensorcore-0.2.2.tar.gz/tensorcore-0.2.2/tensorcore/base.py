"""Provides abstract base classes for arbitrary-dimensional tensors."""
# Author: Michal Ciesielczyk
# Licence: MIT
import functools
import collections
import numpy as np
from abc import ABC, abstractmethod
from ._pyutils import check_type


class AbstractTensor(ABC, collections.Iterable):
    """Abstract base class for arbitrary-dimensional tensors.

    This class is non-instantiable.
    """

    @property
    def ndim(self):
        """Returns the number of dimensions (tensor modes).

        :return: the number of dimensions
        :rtype: int
        """
        return len(self.shape)

    @property
    @abstractmethod
    def shape(self):
        """Returns the tensor shape.

        :return: tensor shape
        :rtype: tuple of ints
        """

    @property
    @abstractmethod
    def dtype(self):
        """Returns the type of data stored in the tensor.

        :return: data type
        :rtype: class
        """

    @property
    def size(self):
        """Returns the number of elements.

        :return: the number of elements
        :rtype: int
        """
        return np.prod(self.shape, dtype=np.int64)

    @property
    @abstractmethod
    def nnz(self):
        """Returns the number of non-zero values.

        :return: the number of non-zero values
        :rtype: int
        """

    @abstractmethod
    def copy(self):
        """Return a copy of the tensor."""

    @abstractmethod
    def innerprod(self, other):
        """Returns the inner product with another tensor

        :return: the inner product with another tensor
        :rtype: dtype
        """

    @abstractmethod
    def values(self):
        """Returns all values stored in the tensor.

        :return: tensor values
        :rtype: generator object
        """

    @abstractmethod
    def outerprod(self, vector):
        """Returns the outer product with the specified vector."""

    @abstractmethod
    def mult(self, V, mode=None, transpose=False):
        """Multiplies the tensor with matrix along specified mode.

        :param V: matrix or a list of matrices
        :type V: matrix object or list
        :param mode: modes along which the multiplication should be performed,
            by default the tensor is multiplied along mode 0 (if mode parameter
            is an int) or all modes (if mode parameter is a list)
        :type mode: int or list of ints, optional
        :param transpose: indicates whether the matrices in V should be
            transposed before multiplication, by default False
        :type transpose: boolean, optional
        :return: tensor multiplied with matrices along specified modes
        :rtype: tensor object
        """

    @abstractmethod
    def norm(self):
        """Returns the Frobenius norm of the tensor.

        :return: the Frobenius norm of the tensor.
        :rtype: float
        """

    @abstractmethod
    def sum(self, mode=None):
        """Returns a 'flattened' tensor along the specified modes (i.e. sum of
        tensor elements over a given mode).

        :param mode: Mode (or tuple of modes) along  which the tensor is
            flattened
        :type mode: int or tuple of ints, by default 0
        :return: Tensor flattened along specified modes
        :rtype: tensor object or scalar if mode is None
        """

    @abstractmethod
    def vectorize(self):
        """Return a copy of the tensor collapsed into one dimension.

        :return: A copy of the tensor, vectorized to one dimension.
        :rtype: tensor object
        """

    @abstractmethod
    def transpose(self, modes=None):
        """Returns the tensor with permuted modes.

        :param modes: By default, reverse the mode order, otherwise permute the
            modes according to the values given.
        :type modes: list of ints, optional
        :return: tensor with its modes permuted. A view is returned whenever
            possible.
        :rtype: tensor object
        """

    def aggregate(self, aggr, f=None, initializer=None):
        """Applies a function f to each element of the tensor T and aggregates
        the results. Returns a value v such that v==a(N) where N is the size of
        T, T[i] is the i-th element of T, and a(i) == aggr( a(i-1), f(T[i]) ).

        Example:

        >>> T = DenseTensor([[0, 1], [2, 3]])
        >>> T.aggregate(lambda x,y: x+y)
        6

        :param aggr: an aggregation function taking as first argument the
            current aggregation and as second argument the transformed current
            element value
        :type aggr: Callable
        :param f: a function transforming the current element value, by default
            no transformation is performed
        :type f: Callable
        :param initializer: placed before the items of the sequence in the
            calculation, and serves as a default when the sequence is empty. By
            default equals to None.
        :return: the aggregated measure.
        :rtype: dtype
        """
        if f is None:
            if initializer is None:
                return functools.reduce(aggr, self.values())
            else:
                return functools.reduce(aggr, self.values(), initializer)
        elif initializer is None:
            return functools.reduce(aggr, (f(x) for x in self.values()))
        else:
            return functools.reduce(aggr, (f(x) for x in self.values()),
                                    initializer)

    @abstractmethod
    def assign(self, func):
        """Assigns the result of a function to each element of the tensor T::

            T[i] = func(T[i]).

        Example:

        >>> T = DenseTensor([[0, 1], [2, 3]])
        >>> T.assign(lambda t: t+1)
        [[1 2] [3 4]]

        :param func: a function object taking as argument the current
            element's value.
        :type func: function
        """

    @abstractmethod
    def unfold(self, mode):
        """Unfolds the tensor along specified modes.

        :param mode: Mode (or list of modes) along  which the tensor is
            unfolded
        :type mode: int or list of ints
        :return: Tensor unfolding along specified modes
        :rtype: unfolding object
        """

    @abstractmethod
    def to_dense(self, copy=False):
        """Returns a dense tensor representation of this tensor.

        :param copy: if False the data may be shared between this tensor and
            the resultant DenseTensor
        :type copy: bool
        :return: a dense tensor
        :rtype: DenseTensor
        """


class AbstractUnfolding(ABC):
    """Abstract base class for a tensor unfolding, providing a fold method to
    the source tensor.

    This class is non instantiable.
    """

    @abstractmethod
    def fold(self):
        """Restore a matrix into a tensor.

        :return: tensor
        :rtype: tensor object
        """


def _check_shape(shape):
    if isinstance(shape, (list, np.ndarray)):
        shape = tuple(shape)
    else:
        check_type("shape", shape, tuple)
    if len(shape) == 0:
        raise ValueError("Invalid shape parameter, number of dimensions must "
                         "be > 0.")
    for dim in shape:
        if not isinstance(dim, (int, np.integer)):
            raise TypeError("shape parameter must be a tuple or list of "
                            "integers (not {}).".format(type(dim)))
    return tuple(shape)


def is_tensor(x):
    return isinstance(x, AbstractTensor)
