import numpy as np
import terminals_set
import function_set
from random import randint

MAX_DEEP = 7

terminals = []
terminalLen = 0
functions = []
functionsLen = 0
functionType = 0

def initGlobalVariables():
    global terminals, terminalLen, functions, functionsLen, functionType
    terminals = terminals_set.getTerminalSet()
    terminalLen = len(terminals)
    functions = function_set.functionSet
    functionsLen = len(functions)
    functionType = function_set.functionType

def initArray(tree, n):
    for i in range(len(tree), n+1):
        tree.append(None)
    return tree

def full(tree, u):
    tree[u] = [None,[]]
    
    n = np.power(2, MAX_DEEP-1) - 1
    totalNodes = np.power(2, MAX_DEEP) - 1

    for i in range(n):
        functionId = randint(0, functionsLen-1)
        f = functions[functionId]
        tree[i][0] = f
        tree[u][1].append(2*u+1)
        tree[u][1].append(2*u+2)
    
    for i in range(n, totalNodes):
        print(i)
        terminalId = randint(0, terminalLen-1)
        terminal = terminals[terminalId]
        tree[i][0] = [terminal, randint(0, 1)] # if 0 - get point1, else, get from point2

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
    if r == 0 and deep < MAX_DEEP: #functions
        functionId = randint(0, functionsLen-1)
        f = functions[functionId]
        tree[u][0] = f
        handleFunctionGrow(tree, u, functionId, deep)
    else: #terminal
        terminalId = randint(0, terminalLen-1)
        terminal = terminals[terminalId]
        tree[u][0] = [terminal, randint(0, 1)] # if 0 - get point1, else, get from point2
        return

def generateOne(initType, maxDeep):
    global MAX_DEEP
    MAX_DEEP = maxDeep
    tree = [None]
    initGlobalVariables()
    if initType == 1:
        grow(0, tree, 0)
    elif initType == 2:
        tree = full(tree, 0)

    return tree

def isFunction(f):
    return type(f) == type(dfs)

def dfs(u, tree):
    f = u[0]
    adjList = u[1]
    if isFunction(f):
        return f(dfs(tree[adjList[0]], tree), dfs(tree[adjList[1]], tree))
    else:
        return 
    

def mapGenotype(tree, point1, point2):
    resultFunction = None
    root = tree[0]
    resultFunction = dfs(root, tree, point1, point2)
    print(tree)
    print(resultFunction)

    return resultFunction
        
            