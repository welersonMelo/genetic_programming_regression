#!/bin/python
import os
import argparse
import sys

import matplotlib.pyplot as plt

def plotOneLine(array, xLabel, yLabel):
    plt.plot(array)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.show()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pathToFile", required=True, help="Path to result file.", type=str)
    args = vars(ap.parse_args())

    path = args["pathToFile"]

    f = open(path, "r")
    lines = f.readlines()
    arrayType = []
    for line in lines:
        line = line.split(':')
        if len(line) > 1:
            array = line[1].replace("'","").replace(']','').replace('[','').replace('\n','').split(', ')
            array = [float(a) for a in array]
            #print(array)
            plotOneLine(array, "Generation", line[0])
        else:
            print(line[0])

## main ##
if __name__ == "__main__":
    main()
