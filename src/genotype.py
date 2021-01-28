import numpy as np
import function_set
from random import randint

MAX_DEEP = 7

terminalLen = 0
functions = []
functionsLen = 0
functionType = 0

def initGlobalVariables(terminalSetSize):
    global terminalLen, functions, functionsLen, functionType
    terminalLen = terminalSetSize
    functions = function_set.functionSet
    functionsLen = len(functions)
    functionType = function_set.functionType

def initArray(tree, n):
    for i in range(len(tree), n+1):
        tree.append(None)
    return tree

def full():
    n = np.power(2, MAX_DEEP-1) - 1
    totalNodes = np.power(2, MAX_DEEP) - 1

    tree = [[None,[]] for _ in range(totalNodes)]
    
    for i in range(n):    
        functionId = randint(0, functionsLen-1)
        f = functions[functionId]
        tree[i][0] = f
        tree[i][1].append(2*i+1)
        tree[i][1].append(2*i+2)
    
    for i in range(n, totalNodes):
        terminalId = randint(0, terminalLen-1)
        tree[i][0] = [terminalId, randint(0, 1)] # if 0 - get point1, else, get from point2
    return tree

def handleFunctionGrow(tree, u, functionId, deep):
    if functionType[functionId] == 0: #binary function +, - , *
        tree[u][1].append(2*u+1)
        tree[u][1].append(2*u+2)
        tree = initArray(tree, 2*u+2)
        grow(deep+1, tree, 2*u+1)
        grow(deep+1, tree, 2*u+2)

def grow(deep, tree, u):
    tree[u] = [None,[]]
    r = randint(0, 1)
    if (deep == 0) or (r == 0 and deep < MAX_DEEP): #functions
        functionId = randint(0, functionsLen-1)
        f = functions[functionId]
        tree[u][0] = f
        handleFunctionGrow(tree, u, functionId, deep)
    else: #terminal
        terminalId = randint(0, terminalLen-1)
        tree[u][0] = [terminalId, randint(0, 1)] # if 0 - get point1, else, get from point2
        return

def generateOne(initType, maxDeep, terminalSetSize):
    global MAX_DEEP
    MAX_DEEP = maxDeep
    tree = [None]
    initGlobalVariables(terminalSetSize)
    if initType == 1:
        grow(0, tree, 0)
    elif initType == 2:
        tree = full()

    return tree
        
def mutateGene(gene):
    #one point mutation
    n = len(gene)

    while True:
        u = randint(1, n-1)
        if gene[u] != None:
            f = gene[u]
            if f in functions:
                gene[u] = functions[randint(0, functionsLen-1)]
            else:
                gene[u] = [randint(0, terminalLen-1), randint(0, 1)]
            return gene