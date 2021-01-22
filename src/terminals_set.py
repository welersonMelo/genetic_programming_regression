import numpy as np

terminalSet = []

def initSet(labelCsvList):
    global terminalSet
    terminalSet = np.array(labelCsvList)

def getTerminalSet():
    global terminalSet
    return terminalSet