#!/usr/bin/env python3
import numpy

def numpy_integrate(f, a, b, N):
    width = float((b-a)/N)
    points = numpy.linspace(a+width, b, N)
    f = numpy.vectorize(f)
    result = numpy.sum(f(points)) * width
    return result

def numpy_midpoint_integrate(f, a, b, N):
    width = float((b-a)/N)
    points = numpy.linspace((2*a+width)/2.0, (((a+((N-1) * width)) + b)/2.0), N)
    f = numpy.vectorize(f)
    result = numpy.sum(f(points)) * width
    return result