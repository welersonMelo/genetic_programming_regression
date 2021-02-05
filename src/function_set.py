import math
import numpy as np
# availabe function set to form the individuo
#binary operations

INFINITY = 1e18

def sumB(a, b):
    return np.add(a, b)

# absolute minus
def subB(a, b):
    return np.fabs(np.subtract(a, b))

def multB(a, b):
    return np.multiply(a, b)

def divB(a, b):
    if b == 0:
        return INFINITY
    return np.divide(a, b)

#array of available functions
functionSet = [sumB, subB, multB, divB]
functionType = [0, 0, 0, 0] #0 is binary, 1 is unary