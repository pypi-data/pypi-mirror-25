import setuptools
import tensorcore
from setuptools import setup, config

# main project configurations is loaded from setup.cfg by setuptools
# setuptools > 30.3 is required
assert setuptools.__version__ > '30.3'

# add more parameters to configuration
cfg = config.read_configuration("setup.cfg")
download_url = cfg["metadata"]["url"] + "/repository/v" + \
               tensorcore.__version__ + "/archive.tar.gz"

# setup() call
setup(download_url=download_url)
