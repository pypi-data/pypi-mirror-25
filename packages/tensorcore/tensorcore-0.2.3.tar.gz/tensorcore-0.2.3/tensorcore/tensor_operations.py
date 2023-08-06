# Author: Michal Ciesielczyk
# Licence: MIT
import sklearn.metrics as metrics
import numpy as np
import math
import operator
from sklearn.random_projection import sparse_random_matrix
from .matrix_operations import generate_i_matrix, svd
from .sparse import is_sparse
from .base import is_tensor


def mean_squared_error(A, B):
    if not (is_tensor(A) and is_tensor(B)):
        raise TypeError("A and B both must be tensors.")

    if is_sparse(A):
        A = A.to_dense()
    if is_sparse(B):
        B = B.to_dense()

    return metrics.regression.mean_squared_error(A.unfold(0), B.unfold(0))


def mean_absolute_error(A, B):
    if not (is_tensor(A) and is_tensor(B)):
        raise TypeError("A and B both must be tensors.")

    if is_sparse(A):
        A = A.to_dense()
    if is_sparse(B):
        B = B.to_dense()

    return metrics.mean_absolute_error(A.unfold(0), B.unfold(0))


def nri(X, core_shape, density='auto', modes=None, positive_only=False):
    if not is_tensor(X):
        raise TypeError("X has to be a tensor, not a %s." % type(X))
    if modes is None:
        modes = range(X.ndim)
    U = [sparse_random_matrix(X.shape[mode], core_shape[i], density)
         if X.shape[mode] > core_shape[i]
         else generate_i_matrix(X.shape[mode], sparse=True)
         for i, mode in enumerate(modes)]
    if positive_only:
        U = [abs(u) for u in U]
    return U, X.mult(U)


def hosvd(X, ranks, modes=None, compute_core=False):
    """
    High Order SVD (HOSVD) of a tensor. Based on:

    Lieven De Lathauwer, Bart De Moor, and Joos Vandewalle, "A multilinear
    singular value decomposition", 2000.

    :param X: tensor
    :type X: tensor object
    :param ranks:
    :type ranks: list of ints
    :param modes: tensor modes in which HOSVD is applied, default None
        indicates all
    :type modes: list of ints
    :param computeCore: indicates whether to compute the core tensor, by
        default False
    :type computeCore: bool, optional
    :return: list of U matrices for each mode and the core tensor (only if
        computeCore=True)
    :rtype: list or tuple(list, tensor)
    """
    if not is_tensor(X):
        raise TypeError("X has to be a tensor, not a %s." % type(X))
    if modes is None:
        modes = range(X.ndim)
    U = [svd(X.unfold(mode), ranks[mode], compute_U=True,
             compute_V=False)[0] for mode in modes]
    return U, X.mult(U) if compute_core else U


def hooi(X, core_shape, max_iter=100, ctol=1e-8):
    """Higher-Order Orthogonal Iteration (HOOI) of a tensor. Based on:

    Bernard N. Sheehan, Yousef Saad, "Higher Order Orthogonal Iteration of
        Tensors (HOOI) and its Relation to PCA and GLRAM", 2006.

    :param X: tensor
    :type X: tensor object
    :param core_shape: shape of the output core tensor, indicating the extent
        of dimensionality reduction
    :type core_shape: tuple of ints
    :param max_iter: maximum number of iterations taken for the solver to
        converge, by default 100
    :type max_iter: int
    :return: list of U matrices for each mode and the core tensor
    :rtype: list or tuple(list, tensor)
    """
    if not is_tensor(X):
        raise TypeError("X has to be a tensor, not a %s." % type(X))
    U = [np.random.rand(*(X.shape[mode], core_shape[mode]))
         for mode in range(X.ndim)]
    xnorm = X.norm()
    error = float('inf')
    for _ in range(max_iter):
        for mode in range(X.ndim):
            C = X
            sorted_modes = sorted(dict(zip(range(X.ndim), X.shape)).
                                  items(), key=operator.itemgetter(1),
                                  reverse=True)
            sorted_modes = [m for m, _ in sorted_modes if not m == mode]
            for m in sorted_modes:
                C = C.mult(U[m], m)
            if is_sparse(C):
                C = C.to_dense()
            U[mode] = svd(C.unfold(mode), core_shape[mode],
                          compute_U=True, compute_V=False)[0]
        # estimate error on core tensor
        C = C.mult(U[mode], mode)
        new_error = math.sqrt(abs(xnorm ** 2 - C.norm() ** 2)) / xnorm
        if abs(error - new_error) < ctol:
            break
        error = new_error
    return U, C
