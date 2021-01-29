import math
# availabe function set to form the individuo
#binary operations

INFINITY = 1e18

def sumB(a, b):
    return a + b

# absolute minus
def subB(a, b):
    return math.fabs(a - b)

def multB(a, b):
    return a * b

def divB(a, b):
    if b == 0:
        return INFINITY
    return a/(1.0*b)

#array of available functions
functionSet = [sumB, subB, multB, divB]
functionType = [0, 0, 0, 0] #0 is binary, 1 is unary