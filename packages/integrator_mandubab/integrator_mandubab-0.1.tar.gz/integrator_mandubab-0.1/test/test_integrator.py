#!/usr/bin/env python3
from integrator import integrate, midpoint_integrate
from numpy_integrator import numpy_integrate, numpy_midpoint_integrate
from numba_integrator import numba_integrate, numba_midpoint_integrate
from cython_integrator import cython_integrate, cython_midpoint_integrate

def test_integral_of_constant_function(f, N):
    print("TESTING: integration of constant function using ", f.__name__, " and N=", N)
    assert abs(f(lambda x: 2, 0, 1, N) - 2) < 10**-10 
    print("integration of constant function using ", f.__name__, " and N=", N, "test: PASSED")

def test_integral_of_linear_function(f, N):
    print("TESTING: integration of linear function using ", f.__name__, " and N=", N)
    assert abs(f(lambda x: 2*x, 0, 1, N) - 1) <= (1.0/N + 10**-10)
    print("integration of linear function using ", f.__name__, " and N=", N, "test: PASSED")
    
#for N in range(1, 100002, 100):
#    test_integral_of_constant_function(integrate, N)
#    test_integral_of_constant_function(numpy_integrate, N)
#    test_integral_of_constant_function(numba_integrate, N)
#    test_integral_of_constant_function(cython_integrate, N)

#    test_integral_of_constant_function(midpoint_integrate, N)
#    test_integral_of_constant_function(numpy_midpoint_integrate, N)
#    test_integral_of_constant_function(numba_midpoint_integrate, N)
#    test_integral_of_constant_function(cython_midpoint_integrate, N)



