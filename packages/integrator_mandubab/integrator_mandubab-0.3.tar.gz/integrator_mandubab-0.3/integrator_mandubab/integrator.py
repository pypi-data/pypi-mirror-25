#!/usr/bin/env python3

def integrate(f, a, b, N):
    width = float((b-a)/N)
    result=0.0
    i = 1
    while(i < N):
        xi = float(a + (i * width))
        result += float(f(xi))
        i += 1
    result = width * (result + float(f(b)))
    return result

def midpoint_integrate(f, a, b, N):
    width = float((b-a)/N)
    result=0.0
    i = 1
    while(i < N):
        xi = float((2*a + ((2*i - 1) * width))/2.0)
        result += float(f(xi))
        i += 1
    result = width * (result + float(f((((a+((N-1) * width)) + b))/2.0)))
    return result