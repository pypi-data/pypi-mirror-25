from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .version import __version__

# data structures
from .base import AbstractTensor, AbstractUnfolding
from .dense import DenseTensor, DenseUnfolding
from .sparse import CooTensor, CooUnfolding, DokTensor
