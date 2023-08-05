# Author: Michal Ciesielczyk
# Licence: MIT
import math
import operator
import numpy as np
from collections import defaultdict
from functools import reduce
from scipy.sparse import dok_matrix, coo_matrix, csr_matrix, csc_matrix, \
                        issparse


def spmatrix_nbytes(sparse_matrix):
    """Returns the estimated number of bytes a sparse takes in memory."""
    if isinstance(sparse_matrix, coo_matrix):
        return (sparse_matrix.data.nbytes + sparse_matrix.row.nbytes
                + sparse_matrix.col.nbytes)
    if isinstance(sparse_matrix, (csr_matrix, csc_matrix)):
        return (sparse_matrix.data.nbytes + sparse_matrix.indptr.nbytes
                + sparse_matrix.indices.nbytes)
    raise TypeError("Unsupported sparse matrix type. Can't estimate nbytes.")


def is_nan(matrix):
    return np.isnan(matrix.sum())


def is_finite(matrix):
    return not is_nan(matrix)


def generate_i_matrix(size, dtype=None, sparse=False):
    if sparse:
        m = dok_matrix((size, size), dtype=dtype)
    else:
        m = np.zeros((size, size), dtype=dtype)
    for i in range(size):
        m[i, i] = 1
    return m


def sparse_mult(A, B, transpose_A=False, transpose_B=False,
                returned_type=None):
    """Performs a multiplication of two matrices A and B. At least one of the
    given matrices must be sparse. This procedure is memory efficient at the
    expense of CPU time - useful for large matrices.
    """
    if issparse(A) and issparse(B):
        if transpose_A and transpose_B:
            C = A.T * B.T if A.shape[1] < B.shape[0] else (B * A).T
        elif transpose_A:
            C = A.T * B if A.shape[1] < B.shape[1] else (B.T * A).T
        elif transpose_B:
            C = A * B.T if A.shape[0] < B.shape[0] else (B * A.T).T
        else:
            C = A * B if A.shape[0] < B.shape[1] else (B.T * A.T).T
    elif issparse(A):
        if not isinstance(B, np.ndarray):
            raise TypeError("Unknown matrix type (%s)." % type(B))
        if transpose_B:
            B = B.T
        if transpose_A:
            A = A.tocoo()
            shape = (A.shape[1], B.shape[1])
            md = defaultdict(float)  # faster than scipy.dok_matrix
            for row, col, val in zip(A.row, A.col, A.data):
                for k in range(shape[1]):
                    md[(col, k)] += val * B[row, k]
            C = dok_matrix(shape)
            C.update(md)
        else:
            shape = (A.shape[0], B.shape[1])
            md = defaultdict(float)  # faster than scipy.dok_matrix
            for row, col, val in zip(A.row, A.col, A.data):
                for k in range(shape[1]):
                    md[(row, k)] += val * B[col, k]
            C = dok_matrix(shape)
            C.update(md)
    elif issparse(B):
        if not isinstance(B, np.ndarray):
            raise TypeError("Unknown matrix type (%s)." % type(A))
        if transpose_A:
            A = A.T
        if transpose_B:
            B = B.tocoo()
            shape = (A.shape[0], B.shape[0])
            md = defaultdict(float)  # faster than scipy.dok_matrix
            for row, col, val in zip(B.row, B.col, B.data):
                for k in range(shape[0]):
                    md[(k, row)] += val * A[k, col]
            C = dok_matrix(shape)
            C.update(md)
        else:
            B = B.tocoo()
            shape = (A.shape[0], B.shape[1])
            md = defaultdict(float)  # faster than scipy.dok_matrix
            for row, col, val in zip(B.row, B.col, B.data):
                for k in range(shape[0]):
                    md[(k, col)] += val * A[k, row]
            C = dok_matrix(shape)
            C.update(md)
    else:
        raise TypeError("At least one of the specified matrices must be "
                        "sparse. A is a %s and B is a %s" % (type(A), type(B)))
    if returned_type is None:
        return C
    if returned_type == "dok":
        return C.todok()
    if returned_type == "coo":
        return C.tocoo()
    if returned_type == "csr":
        return C.tocsr()
    if returned_type == "csc":
        return C.tocsc()


def normalize(matrix, axis=None):
    if axis is None:
        # Frobenius norm
        norm = 0.0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                norm += matrix[i, j] * matrix[i, j]
        norm = math.sqrt(norm)
        return matrix / norm
    if axis == 0:
        # euclidean norm on rows
        if isinstance(matrix, np.ndarray):
            norms = np.apply_along_axis(np.linalg.norm, 1, matrix)
        else:
            norms = []
            for i in range(matrix.shape[axis]):
                norm = 0
                for j in range(matrix.shape[1]):
                    norm += matrix[i, j] * matrix[i, j]
                norms.append(math.sqrt(norm))
        for i in range(matrix.shape[axis]):
            if norms[i] > 0.0:
                matrix[i, :] = matrix[i, :] / norms[i]
        return matrix
    elif axis == 1:
        # euclidean norm on columns
        if isinstance(matrix, np.ndarray):
            norms = np.apply_along_axis(np.linalg.norm, 0, matrix)
        else:
            norms = []
            for i in range(matrix.shape[axis]):
                norm = 0
                for j in range(matrix.shape[0]):
                    norm += matrix[j, i] * matrix[j, i]
                norms.append(math.sqrt(norm))
        for i in range(matrix.shape[axis]):
            if norms[i] > 0.0:
                matrix[:, i] = matrix[:, i] / norms[i]
        return matrix
    raise ValueError('Invalid matrix axis!')


def flipsign(U):
    """Flip sign of a factor matrix such that largest magnitude element will be
    positive
    """
    midx = np.asarray(abs(U).argmax(axis=0))
    if midx.ndim > 1:
        midx = midx.flatten()
    for i in range(U.shape[1]):
        if U[midx[i], i] < 0:
            U[:, i] = -U[:, i]
    return U


def svd(A, k_components, compute_U=True, compute_V=True, algorithm='arpack'):
    if not (isinstance(A, np.ndarray) or issparse(A)):
        raise TypeError("Parameter A must be of matrix type, not %s."
                        % type(A))
    if A.ndim != 2:
        raise ValueError("Parameter A must be a 2-dimensional array, while "
                         "%d-dimensional array was given." % A.ndim)
    if isinstance(k_components, float):
        if k_components <= 0.0 or k_components > 1.0:
            raise ValueError("Parameter k_components must be in (0.0,1.0>, "
                             "while %d given." % k_components)
        k_components = max(int(round(k_components * min(A.shape))), 1)
    elif isinstance(k_components, (int, np.integer)):
        if k_components < 1:
            raise ValueError("Parameter k_components must be greater than 0.")
    else:
        raise TypeError("Parameter k_components must be an int or float, not "
                        "%s." % type(k_components))
    if algorithm not in {'lapack', 'arpack', 'randomized'}:
        raise ValueError("Parameter algorithm must be equal to one of "
                         "['lapack', 'arpack', 'randomized'].")

    if k_components > max(A.shape):
        raise ValueError("Parameter k_components must be less or equal to "
                         "max(A.shape). %d > max %s."
                         % (k_components, A.shape))
    if is_nan(A):
        raise ValueError("NaN or infinity values in specified the matrix A.")

    # TODO: check if converting sparse matrices to CSR format is needed
    # if issparse(A):
    #     A = csr_matrix(A)

    if k_components >= min(A.shape) or algorithm == 'lapack':
        # http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.svd.html
        from numpy.linalg import svd as lsvd
        # FIXME: numpy.linalg.svd requires a dense matrix?
        if issparse(A):
            A = A.todense()

        full_matrices = k_components > min(A.shape)
        if compute_U and compute_V:
            U, S, Vt = lsvd(A, full_matrices=full_matrices, compute_uv=True)
            return trunc(U, k_components, 1), trunc(S, k_components), trunc(
                Vt, k_components)
        elif compute_U:
            U, S, _ = lsvd(A, full_matrices=full_matrices, compute_uv=True)
            return trunc(U, k_components, 1), trunc(S, k_components)
        elif compute_V:
            _, S, Vt = lsvd(A, full_matrices=full_matrices, compute_uv=True)
            return trunc(S, k_components), trunc(Vt, k_components)
        else:
            S = lsvd(A, full_matrices=full_matrices, compute_uv=False)
            return trunc(S, k_components)
    elif algorithm == 'arpack':
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.svds.html
        from scipy.sparse.linalg import svds

        if compute_U and compute_V:
            U, S, Vt = svds(A, k_components, return_singular_vectors=True)
            U[:, :k_components] = U[:, k_components - 1::-1]  # reverse the n first columns of u
            S = S[::-1]  # reverse s
            Vt[:k_components, :] = Vt[k_components - 1::-1, :]  # reverse the n first rows of vt
            return U, S, Vt
        elif compute_U:
            U, S, _ = svds(A, k_components, return_singular_vectors='u')
            U[:, :k_components] = U[:, k_components - 1::-1]  # reverse the n first columns of u
            S = S[::-1]  # reverse s
            return U, S
        elif compute_V:
            _, S, Vt = svds(A, k_components, return_singular_vectors='vh')
            S = S[::-1]  # reverse s
            Vt[:k_components, :] = Vt[k_components - 1::-1, :]  # reverse the n first rows of vt
            return S, Vt
        else:
            S = svds(A, k_components, return_singular_vectors=False)
            S = S[::-1]  # reverse s
            return S
    else:
        # https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/extmath.py
        from sklearn.utils.extmath import randomized_svd as rsvd

        if compute_U and compute_V:
            U, S, Vt = rsvd(A, k_components)
            return U, S, Vt
        elif compute_U:
            U, S, _ = rsvd(A, k_components)
            return U, S
        elif compute_V:
            _, S, Vt = rsvd(A, k_components)
            return S, Vt
        else:
            _, S, _ = rsvd(A, k_components)
            return S


def trunc(matrix, n, axis=0):
    if not n > 0:
        return matrix
    dim = matrix.shape[axis]
    if n > dim:
        return matrix
    return np.delete(matrix, np.s_[n:dim], axis)


def khatri_rao(A):
    """Returns a column-wise Khatri-Rao product of matrices A.

    :param A: list of matrices for which the column-wise Khatri-Rao product
        should be computed
    :type A: list or tuple of matrices
    """
    if not isinstance(A, (list, tuple)):
        raise ValueError("A parameter must be a list or tuple of matrices, "
                         "not %s." % type(A))
    N = len(A)
    for i in range(N):
        if A[i].ndim != 2:
            raise ValueError("A parameter must be a tuple of matrices (while "
                             "A[%d].ndim = %d)." % (i, A[i].ndim))
    R = A[0].shape[1]
    C = reduce(operator.mul, (A[i].shape[0] for i in range(len(A))))
    for i in range(N):
        if C != A[i].shape[1]:
            raise ValueError("All matrices in A must have same number of "
                             "columns (ie. A[%d].shape[1] != %d." % (i, C))
    P = np.zeros((R, C), dtype=A[0].dtype)  # preallocate
    for col in range(C):
        ab = A[0][:, col]
        for i in range(1, N):
            ab = np.kron(ab, A[i][:, col])
        P[:, col] = ab
    return P
