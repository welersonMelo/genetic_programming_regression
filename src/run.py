#!/bin/python
import os
import argparse
import sys

import input_reader as ir
import genotype
import k_means
import numpy as np
import statistics
import math
import plots
import copy

from random import randint

# global variables
KNOWN_CLUSTERS = 7
# for plots
meanByGeneration = []
medianByGeneration = []
minByGeneration = []
maxByGeneration = []
repeatedIndividuals = []
generatedFunctionList = []
maxEqualIndividuals = []
# global variables


def calEuclidianToCompare(testData, completeData, columnToExclude):
    def euclidianDistance(point1, point2):
        dimension = len(point1)
        sum = 0.0
        for i in range(dimension):
            sum += (point1[i] - point2[i])**2

        return math.sqrt(sum)
    
    function = euclidianDistance

    clustersNumber = KNOWN_CLUSTERS
    clusters = k_means.modelTrain(function, clustersNumber, testData)
    fitness = k_means.modelEvaluation(clusters, completeData, columnToExclude)
    return fitness

def full(populationSize, maxDeep, terminalSetSize):
    populationGenotype = []
    for i in range(populationSize):
        tree = genotype.generateOne(2, maxDeep, terminalSetSize)
        populationGenotype.append(tree)
    return populationGenotype

def grow(populationSize, maxDeep, terminalSetSize):
    populationGenotype = []
    for i in range(populationSize):
        tree = genotype.generateOne(1, maxDeep, terminalSetSize)
        populationGenotype.append(tree)
    return populationGenotype

def generatePopulation(populationSize, initType, terminalSetSize):
    if initType == 1:
        return grow(populationSize, 7, terminalSetSize)
    elif initType == 2:
        return full(populationSize, 7, terminalSetSize)
    elif initType == 3:
        subSize = populationSize//6 # population size should be a multiple of 6
        firsHalf = subSize//2
        secondHalf = subSize - firsHalf
        populationGenotype = []
        for i in range(2, 8): # for 7 levels fixed
            populationGenotype += full(firsHalf, i, terminalSetSize)
            populationGenotype += grow(secondHalf, i, terminalSetSize)
                
        return populationGenotype

def isFunction(f):
    return type(f) == type(dfs)
    
def dfs(u, tree, point1, point2, fromLeft):
    f = u[0]
    adjList = u[1]

    if isFunction(f):
        return f(dfs(tree[adjList[0]], tree, point1, point2, 1), dfs(tree[adjList[1]], tree, point1, point2, 0))
    else: #f is terminal
        if fromLeft:
            return point1[f[0]]
        else:
            return point2[f[0]]

import time
def getFitness(gene, testData, completeData, columnToExclude):
    global KNOWN_CLUSTERS
    gene = np.array(gene, dtype=object)
    # Calculando Fitness
    root = gene[0]
    #print(gene)
    def distanceFunction(point1, point2):
        r = dfs(root, gene, point1, point2, 0)
        return r
        
    function = distanceFunction

    clustersNumber = KNOWN_CLUSTERS
    clusters = k_means.modelTrain(function, clustersNumber, testData)
    fitness = k_means.modelEvaluation(clusters, completeData, columnToExclude)
    #print("my func v-meausure:", fitness)
    
    return fitness

def selectionTournament(populationFitness, k):
    maxIndividual = randint(0, len(populationFitness)-1)
    for i in range(k - 1):
        individual = randint(0, len(populationFitness)-1)
        if populationFitness[individual] > populationFitness[maxIndividual]:
            maxIndividual = individual
    return maxIndividual
    
def createNode(tree, n):
    for i in range(len(tree), n):
        tree.append(None)
    return tree

def bfsCrossover (tree1, tree2, u):
    if len(tree1) < len(tree2):
        tree1 = createNode(tree1, len(tree2))
    else:
        tree2 = createNode(tree2, len(tree1))
    
    treesLen = len(tree1)

    queue = [u]
    while len(queue) != 0:
        u = queue.pop()
        aux = None if tree1[u] == None else tree1[u].copy()
        tree1[u] = None if tree2[u] == None else tree2[u].copy()
        tree2[u] = aux
        v1, v2 = 2*u+1, 2*u+2
        if v1 < treesLen:
            if tree1[v1] != None or tree2[v1] != None:
                queue.append(v1)
        if v2 < treesLen:
            if tree1[v2] != None or tree2[v2] != None:
                queue.append(v2)
        
    return tree1, tree2

def crossover(parent1, parent2, crossoverProb):
    minParent = min(len(parent1), len(parent2))
    probability = randint(0, 100)

    if parent1 == parent2:
        print('iguais')
        return parent1, parent2

    child1 = parent1.copy()
    child2 = parent2.copy()

    if probability <= crossoverProb * 100.0:
        while True: # review this approach
            u = randint(1, minParent-1)
            if parent1[u] != None and parent2[u] != None:
                break

        child1, child2 = bfsCrossover(parent1, parent2, u)

    return child1, child2

def mutation(population, mutationProb):
    popSize = len(population)
    for i in range(popSize):
        probability = randint(0, 100)
        if probability <= mutationProb*100:
            population[i] = genotype.mutateGene(population[i])
    return population

def updateStatisticalData(populationFitness):
    meanFitness = sum(populationFitness) / (1.0 * len(populationFitness))
    medianFitness = statistics.median(populationFitness)
    meanByGeneration.append(meanFitness)
    medianByGeneration.append(medianFitness)
    maxByGeneration.append(max(populationFitness))
    minByGeneration.append(min(populationFitness))
    
    # count repeated
    totalRepeated = 0
    n = len(generatedFunctionList)
    i = 0
    maxCount = 0
    while i < n:
        curr = generatedFunctionList[i]
        count = 0
        k = len(generatedFunctionList)
        j = 0
        while j < k:
            if curr == generatedFunctionList[j]:
                generatedFunctionList.pop(j)
                count += 1
                k -= 1
            j += 1
        n = k
        maxCount = max(maxCount, count)
        if count > 1:
            totalRepeated += 1
        i += 1
        
    #print('repeated:', totalRepeated)
    maxEqualIndividuals.append(maxCount)
    repeatedIndividuals.append(totalRepeated)

import datetime
def geneticProgramming(populationSize, generations, initType, testData, completeData, columnToExclude, k, crossoverProb, mutationProb, elitismNumber):
    global generatedFunctionList
    terminalSetSize = len(testData.columns.values)
    populationGenotype = generatePopulation(populationSize, initType, terminalSetSize)

    #print('Population Generated!')

    maxIndividualLastGeneration = []

    for seculum in range(generations):
        print(seculum, 'th generation')
        populationFitness = []
        generatedFunctionList = populationGenotype.copy()

        #print('Init:', datetime.datetime.now().time())
        
        for gene in populationGenotype:
            populationFitness.append(getFitness(gene, testData, completeData, columnToExclude))
        
        #print('end - getFiness:', datetime.datetime.now().time())

        updateStatisticalData(populationFitness)

        # selection
        newPopulation = []
        for i in range(int(populationSize/2) - elitismNumber//2):
            parent1 = populationGenotype[selectionTournament(populationFitness, k)]
            parent2 = populationGenotype[selectionTournament(populationFitness, k)]
            child1, child2 = crossover(parent1, parent2, crossoverProb)
            #print('parent1:', parent1, '\nparent2:', parent2)
            #print('child1:', child1, '\nchild2:', child2)
            newPopulation.append(child1)
            newPopulation.append(child2)
        #print('end - crossover:', datetime.datetime.now().time())
        # elitism
        maxId = populationFitness.index(max(populationFitness))
        maxIndividualLastGeneration = [populationGenotype[maxId], max(populationFitness)]
        for i in range(elitismNumber):
            maxId = populationFitness.index(max(populationFitness))
            newPopulation.append(populationGenotype[maxId])
            populationFitness[maxId] = -1

        #print('end - elitism:', datetime.datetime.now().time())
        #mutation on new offspring
        populationGenotype = []
        populationGenotype = mutation(newPopulation, mutationProb)
        #print('end - mutation:', datetime.datetime.now().time())

    #end of Genetic Programming
    #print(f"Finishing last generation! Max individual found with fitness {maxIndividualLastGeneration[1]}: {maxIndividualLastGeneration[0]}")
    # return fitness of the best individual of the last generation
    return maxIndividualLastGeneration[0]
    
def handlePlots():
    plots.plotOneLine(meanByGeneration, "Generation", "Mean")
    plots.plotOneLine(repeatedIndividuals, "Generation", "Repeated individuals")
    plots.plotOneLine(medianByGeneration, "Generation", "Median")
    plots.plotOneLine(maxByGeneration, "Generation", "Max")
    plots.plotOneLine(minByGeneration, "Generation", "Min")


def initiatePoints(csvPath, columnToExclude):
    completeData = ir.readCsv(csvPath)
    testData = completeData.drop([columnToExclude], axis=1)

    return completeData, testData

#in e.g.: python run.py --csvPath ../data/glass_train.csv --columnToExclude glass_type --populationSize 30 --generations 30 --initPopulationType 3 --tournamentK 2 --crossoverProb 0.9 --mutationProb 0.05 --elitismNumber 2
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csvPath", required=True, help="Path to csv of dataset.", type=str)
    ap.add_argument("--columnToExclude", required=True, help="The label column to be excluded from the tests.", type=str)
    ap.add_argument("--populationSize", required=True, help="Number of individuals of a population.", type=int)
    ap.add_argument("--generations", required=True, help="Number of generations to be produced.", type=int)
    ap.add_argument("--initPopulationType", required=True, help="Type of initialization, 1: grow; 2: full: 3: ramped half-and-half", type=int)
    ap.add_argument("--tournamentK", required=True, help="The size of K used for tournaments", type=int)
    ap.add_argument("--crossoverProb", required=True, help="Crossover probability in range [0, 1]", type=float)
    ap.add_argument("--mutationProb", required=True, help="Mutation probability in range [0, 1]", type=float)
    ap.add_argument("--elitismNumber", required=True, help="Number of individuals to elitism. Use 0 for no use elitism; must be an even number", type=int)
    args = vars(ap.parse_args())

    popSize = args["populationSize"]
    generations = args["generations"]
    initPopType = args["initPopulationType"]
    csvPath = args["csvPath"]
    columnToExclude = args["columnToExclude"]
    k = args["tournamentK"]
    crossoverProb = args["crossoverProb"]
    mutationProb = args["mutationProb"]
    elitismNumber = args["elitismNumber"]

    completeData, testData = initiatePoints(csvPath, columnToExclude)

    bestFitness = geneticProgramming(popSize, generations, initPopType, testData, completeData, columnToExclude, k, crossoverProb, mutationProb, elitismNumber)

    testDataComplete, testDataTest = initiatePoints('../data/glass_test.csv', columnToExclude)
    fitnessTest = 0
    for _ in range(10):
        fitnessTest += getFitness(bestFitness, testDataTest, testDataComplete, columnToExclude)

    fitnessTest = fitnessTest / 10.0

    fitnessOnEuclidian = [calEuclidianToCompare(testDataTest, testDataComplete, columnToExclude) for _ in range(10)]
    fitnessOnEuclidian = sum(fitnessOnEuclidian) / (1.0 * len(fitnessOnEuclidian))

    print("Euclidian result mean: ", fitnessOnEuclidian)
    print("Our individual mean: ", fitnessTest)
    
    popSiz = args["populationSize"]
    # name is composed by: population size + number of generations + crossover prob + mutation prob + K of tourname + elitism number of inidivdual
    f = open(f"result_{popSiz}_{generations}_{crossoverProb}_{mutationProb}_k-{k}_{elitismNumber}.txt", "w")
    f.write('mean:' + str(meanByGeneration) + "\n")
    f.write('repeated:' + str(repeatedIndividuals) + "\n")
    f.write('maxEqual:' + str(maxEqualIndividuals) + "\n")
    f.write('median:' + str(medianByGeneration) + "\n")
    f.write('max:' + str(maxByGeneration) + "\n")
    f.write('min:' + str(minByGeneration) + "\n")
    f.write('best final fitness =' + str(bestFitness))
    f.write('Final on test dataset =' + str(fitnessTest))
    f.close()

    # ploting data
    #handlePlots()
                            
if __name__ == "__main__":
    main()



