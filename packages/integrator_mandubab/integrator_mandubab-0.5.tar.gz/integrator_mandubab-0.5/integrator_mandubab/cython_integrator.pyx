#!/usr/bin/env python3
import numpy
cimport numpy

cpdef double cython_integrate(f, a, b, N):
    cdef double width = (b-a)/N
    cdef numpy.ndarray[numpy.double_t, ndim=1] points = numpy.linspace(a+width, b, N, dtype=numpy.double)
    f = numpy.vectorize(f)
    cdef double result = numpy.sum(f(points), dtype=numpy.double) * width
    return result

cpdef double cython_midpoint_integrate(f, a, b, N):
    cdef double width = (b-a)/N
    cdef numpy.ndarray[numpy.double_t, ndim=1] points = numpy.linspace((2*a+width)/2.0, (((a+((N-1) * width)) + b)/2.0), N, dtype=numpy.double)
    f = numpy.vectorize(f)
    cdef double result = numpy.sum(f(points), dtype=numpy.double) * width
    return result