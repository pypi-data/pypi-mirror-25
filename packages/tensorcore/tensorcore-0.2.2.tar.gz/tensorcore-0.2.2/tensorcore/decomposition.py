# Author: Michal Ciesielczyk
# Licence: MIT
import numpy as np
from scipy.sparse.base import spmatrix
from .base import is_tensor, AbstractTensor
from .vector_operations import to_tensor
from ._pyutils import is_sequence, check_type


class DecomposedTensor(object):

    def __init__(self, U, core):
        if not is_sequence(U, (np.ndarray, spmatrix)):
            raise TypeError("U parameter must be a sequence of dense or "
                            "sparse arrays.")
        check_type("core", core, AbstractTensor)
        self._U = U
        self._shape = tuple(u.shape[0] for u in U)
        self._core = core

    @property
    def ndim(self):
        """Returns the number of dimensions (tensor modes).

        :return: the number of dimensions
        :rtype: int
        """
        return len(self.shape)

    @property
    def shape(self):
        """Returns the tensor shape.

        :return: tensor shape
        :rtype: tuple of ints
        """
        return self._shape

    @property
    def size(self):
        """Returns the number of elements.

        :return: the number of elements
        :rtype: int
        """
        return np.prod(self.shape, dtype=np.int64)

    def add(self, data):
        self._core += self.encode(data)

    def encode(self, data):
        if is_sequence(data, (np.ndarray, spmatrix)):
            if len(data) != self.ndim:
                raise ValueError("Number of vectors must correspond to the "
                                 "number of tensor modes")
            return self._encode_vectors(data)
        elif isinstance(data, tuple) and all(
                        isinstance(i, (np.integer, int)) for i in data):
            if len(data) != self.ndim:
                raise ValueError("Number of indices must correspond to the "
                                 "number of tensor modes")
            return self._encode_indices(data)
        elif is_tensor(data):
            return self._encode_tensor(data)
        else:
            raise TypeError("data parameter must be a list of vectors, tuple "
                            "of integers or a tensor, not a {}".
                            format(type(data)))

    def _encode_vectors(self, vectors):
        t = to_tensor(vectors[0].dot(self._U[0]))
        for m in range(1, self.ndim):
            t = t.outerprod(to_tensor(vectors[m].dot(self._U[m])))
        if self._core.shape == t.shape:
            return t
        else:
            raise ValueError("Invalid shape of one of the vectors (shape{} "
                             "instead of expected shape{}).".format(
                                 t.shape, self._core.shape))

    def _encode_indices(self, indices):
        t = to_tensor(self._U[indices[0]])
        for m in range(1, self.ndim):
            t = t.outerprod(to_tensor(self._U[indices[m]]))
        return t

    def _encode_tensor(self, tensor):
        return tensor.mult(self._U)

    def reconstruct(self):
        return self._core.mult(self._U, transpose=True)

    def decode(self, data):
        return self._core.innerprod(self.encode(data))
