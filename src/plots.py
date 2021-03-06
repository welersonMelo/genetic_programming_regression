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

def plotTreeLines(arr1, arr2, arr3, xLabel, label1, label2, label3, title):
    plt.plot(arr1, label = label1)
    plt.plot(arr2, label = label2)
    plt.plot(arr3, label = label3)
    plt.title(title)
    plt.legend()
    plt.show()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pathToFile", required=True, help="Path to result file.", type=str)
    args = vars(ap.parse_args())

    path = args["pathToFile"]

    f = open(path, "r")
    lines = f.readlines()
    arrayType = []
    allPlots = []
    for line in lines:
        line = line.split(':')
        if len(line) > 1:
            array = line[1].replace("'","").replace(']','').replace('[','').replace('\n','').split(', ')
            array = [float(a) for a in array]
            #print(array)
            allPlots.append(array)
            plotOneLine(array, "Generation", line[0])
        else:
            print(line[0])
    
    meanP = allPlots[0]
    maxP = allPlots[4]
    minP = allPlots[5]
    plotTreeLines(maxP, meanP, minP, "Generation", "max", "mean", "min", "Fitness vs Generation plot.")

# python plots.py --pathToFile results/result_30_5_0.9_0.05_k-2_2.txt
## main ##
if __name__ == "__main__":
    main()
