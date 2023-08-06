import setuptools

# main project configurations is loaded from setup.cfg by setuptools
assert setuptools.__version__ > '30.3', "setuptools > 30.3 is required"

setuptools.setup()
