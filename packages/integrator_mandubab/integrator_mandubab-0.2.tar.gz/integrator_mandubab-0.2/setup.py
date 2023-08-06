#!/usr/bin/env python3
from distutils.core import setup
from distutils.extension import Extension
import numpy

try:
    from Cython.Distutils import build_ext
except ImportError:
    raise ImportError("could not import cython")

cmdclass = {}
ext_modules = []

ext_modules += [
        Extension("integrator_mandubab.cython_integrator", [ "integrator_mandubab/cython_integrator.pyx" ],
        include_dirs=[numpy.get_include()]),
    ]
cmdclass.update({ 'build_ext': build_ext })

setup(
    name='integrator_mandubab',
    version='0.2',
    description='Simple Integrator for INF4331 assignment4 in UiO',
    url='https://github.com/UiO-INF3331/INF3331-mandubab/tree/master/assignment4',
    author='Manduba Annka Bari',
    author_email='m.a.bari@sfe.uio.no',
    packages=[ 'integrator_mandubab'],
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    long_description=open('README.txt').read(),
    license="MIT",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Cython',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='simple integrator UiO INF4331 assignment4',
)