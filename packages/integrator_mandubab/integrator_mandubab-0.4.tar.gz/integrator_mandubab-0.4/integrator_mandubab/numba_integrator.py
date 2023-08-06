#!/usr/bin/env python3
from numba import jit

def numba_integrate(f, a, b, N):
    f_jit = jit("f8(f8)", nopython=True)(f)

    @jit("f8(f8)", nopython=True)
    def f_call(x):
        return f_jit(x)
    
    @jit("f8(f8, f8, u8)", nopython=True)
    def numba_integrate_call(a, b, N):
        width = float((b-a)/N)
        result=0.0
        i = 1
        while(i < N):
            xi = float(a + (i * width))
            result += float(f_call(xi))
            i += 1
        result = width * (result + float(f_call(b)))
        return result
    return numba_integrate_call(a, b, N)

def numba_midpoint_integrate(f, a, b, N):
    f_jit = jit("f8(f8)", nopython=True)(f)

    @jit("f8(f8)", nopython=True)
    def f_call(x):
        return f_jit(x)

    @jit("f8(f8, f8, u8)", nopython=True)
    def numba_integrate_call(a, b, N):
        width = float((b-a)/N)
        result=0.0
        i = 1
        while(i < N):
            xi = float((2*a + ((2*i - 1) * width))/2.0)
            result += float(f_call(xi))
            i += 1
        result = width * (result + float(f_call((((a+((N-1) * width)) + b))/2.0)))
        return result
    return numba_integrate_call(a, b, N)
