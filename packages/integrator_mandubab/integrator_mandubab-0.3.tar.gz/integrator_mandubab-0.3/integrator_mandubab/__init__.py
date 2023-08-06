#!/usr/bin/env python3
from integrator import python_integrate, python_midpoint_integrate
from numpy_integrator import numpy_integrate, numpy_midpoint_integrate
from numba_integrator import numba_integrate, numba_midpoint_integrate
from cython_integrator import cython_integrate, cython_midpoint_integrate

# f --> function to integrate
# a --> lower limit
# b --> upper limit
# N --> number of intermediate points
# method --> "endpoint" or "midpoint"
# implementation --> "python" or "numpy" or "numba" or "cython" 
def integrate(f, a, b, N, method = "endpoint", implementation = "python"):
    if(implementation == "numpy"):
        if(method == "midpoint"):
            return numpy_midpoint_integrate(f, a, b, N)
        else: # endpoint
            return numpy_integrate(f, a, b, N)

    elif(implementation == "numba"):
        if(method == "midpoint"):
            return numba_midpoint_integrate(f, a, b, N)
        else: # endpoint
            return numba_integrate(f, a, b, N)

    elif(implementation == "cython"):
        if(method == "midpoint"):
            return cython_midpoint_integrate(f, a, b, N)
        else: # endpoint
            return cython_integrate(f, a, b, N)

    else: #python
        if(method == "midpoint"):
            return python_midpoint_integrate(f, a, b, N)
        else: # endpoint
            return python_integrate(f, a, b, N)