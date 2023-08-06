#!/usr/bin/env python3
from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name = "Integration",
    ext_modules = cythonize("*.pyx"),
    include_dirs=[numpy.get_include()]
)