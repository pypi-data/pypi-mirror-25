
This package implements simple integration function with following signature:

def integrate(f, a, b, N, method = "endpoint", implementation = "python")
where
f --> function to integrate (python function)
a --> lower limit (float)
b --> upper limit (float)
N --> number of intermediate points (integer)
method --> "endpoint" or "midpoint" (string)
implementation --> "python" or "numpy" or "numba" or "cython" (string) 