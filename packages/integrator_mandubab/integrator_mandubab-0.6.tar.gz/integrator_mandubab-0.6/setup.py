#!/usr/bin/env python3
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    raise ImportError("could not import cython")


class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""
    def run(self):

        # Import numpy here, only when headers are needed
        import numpy

        # Add numpy headers to include_dirs
        self.include_dirs.append(numpy.get_include())

        # Call original build_ext command
        build_ext.run(self)

cmdclass = {}
ext_modules = []

ext_modules += [
        Extension("integrator_mandubab.cython_integrator", [ "integrator_mandubab/cython_integrator.pyx" ]),
    ]
cmdclass.update({ 'build_ext': CustomBuildExtCommand })

setup(
    name='integrator_mandubab',
    version='0.6',
    description='Simple Integrator for INF4331 assignment4 in UiO',
    url='https://github.com/UiO-INF3331/INF3331-mandubab/tree/master/assignment4',
    author='Manduba Annka Bari',
    author_email='m.a.bari@sfe.uio.no',
    packages=[ 'integrator_mandubab'],
    cmdclass = cmdclass,
    install_requires=['numpy'],
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