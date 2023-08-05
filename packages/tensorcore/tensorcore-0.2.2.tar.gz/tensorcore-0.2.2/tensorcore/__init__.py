"""tensorcore is a Python package for multilinear algebra supporting basic
operations on dense and sparse tensors.

See https://gitlab.com/cmick/tensorcore for more information.
"""
from ._version import __version__

# data structures
from .base import AbstractTensor, AbstractUnfolding
from .dense import DenseTensor, DenseUnfolding
from .sparse import CooTensor, CooUnfolding, DokTensor
