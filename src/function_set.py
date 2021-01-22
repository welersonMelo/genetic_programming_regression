import numpy as np
import math
# availabe function set to form the individuo
#binary operations
def sumB(a, b):
    return a + b

# absolute minus
def subB(a, b):
    return math.fabs(a - b)

def multB(a, b):
    return a * b

#array of available functions
functionSet = np.array([sumB, subB, multB])
functionType = [0, 0, 0] #0 is binary, 1 is unary