import os

# Downloads setuptools if not find it before try to import
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

packages = ['comments']

setup(
    name='London comments',
    version=0.1,
    author="Eugen Perepelkov",
    license="BSD License",
    packages=packages,
    )

