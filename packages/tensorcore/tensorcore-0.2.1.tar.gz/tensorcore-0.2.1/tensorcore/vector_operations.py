# Author: Michal Ciesielczyk
# Licence: MIT
import numpy as np
from scipy.sparse.base import issparse, spmatrix
from ._pyutils import check_type
from .dense import DenseTensor
from .sparse import CooTensor


def hadamard_product(*vectors):
    N = vectors[0].shape
    prod = np.ones(N, dtype=vectors[0].dtype)
    for v in vectors:
        for i in range(N):
            prod[i] *= v[i]
    return prod.sum()


def to_tensor(vector):
    check_type("vector", vector, (np.ndarray, spmatrix))
    if issparse(vector):
        t = vector.tocoo()
        if t.shape[0] == 1:
            return CooTensor(indices=t.col, values=t.data,
                             shape=(t.shape[1],), dtype=t.dtype)
        elif t.shape[1] == 1:
            return CooTensor(indices=t.row, values=t.data,
                             shape=(t.shape[0],), dtype=t.dtype)
        else:
            raise ValueError("Parameter vector must be a row or column vector,"
                             " not a matrix with {} shape."
                             .format(to_tensor.shape))
    else:
        return DenseTensor(vector.ravel(), dtype=vector.dtype)
