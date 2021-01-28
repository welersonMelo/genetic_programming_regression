#!/bin/python
import os
import argparse
import sys

import input_reader as ir
import genotype
import k_means
import numpy as np

import copy

from random import randint

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
    # Calculando Fitness
    root = gene[0]
    #print(gene)
    #time.sleep(2)
    def distanceFunction(point1, point2):
        r = dfs(root, gene, point1, point2, 0)
        return r
        
    function = distanceFunction

    clustersNumber = 7 # passar esse valor como parametro
    clusters = k_means.modelTrain(function, clustersNumber, testData)
    fitness = k_means.modelEvaluation(clusters, completeData, columnToExclude)
    
    #print("my func v-meausure:", fitness)
    
    return fitness

def selectionTournament(populationFitness, k):
    individual1 = randint(0, len(populationFitness)-1)
    individual2 = randint(0, len(populationFitness)-1)

    if populationFitness[individual1] >= populationFitness[individual2]:
        return individual1
    else:
        return individual2

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

    child1 = parent1
    child2 = parent2

    if probability <= crossoverProb * 100:
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

def geneticProgramming(populationSize, initType, testData, completeData, columnToExclude, k, crossoverProb, mutationProb, elitismNumber):
    terminalSetSize = len(testData.columns.values)
    populationGenotype = generatePopulation(populationSize, initType, terminalSetSize)

    print('Population Generated!')

    for generation in range(populationSize):
        print(generation, 'th generation')
        populationFitness = []

        for gene in populationGenotype:
            populationFitness.append(getFitness(gene, testData, completeData, columnToExclude))



        # selection
        newPopulation = []
        for i in range(int(populationSize/2) - elitismNumber):
            parent1 = populationGenotype[selectionTournament(populationFitness, k)]
            parent2 = populationGenotype[selectionTournament(populationFitness, k)]
            child1, child2 = crossover(parent1, parent2, crossoverProb)
            newPopulation.append(child1)
            newPopulation.append(child2)
        # elitism
        for i in range(elitismNumber):
            maxId = populationFitness.index(max(populationFitness))
            newPopulation.append(populationGenotype[maxId])
            populationFitness[maxId] = -1

        # mutation on new offspring
        populationGenotype = mutation(newPopulation, mutationProb)

        print("fim forçado aqui")
        exit(1)


def initiatePoints(csvPath, columnToExclude):
    completeData = ir.readCsv(csvPath)
    testData = completeData.drop([columnToExclude], axis=1)

    return completeData, testData

#in e.g.: python run.py --csvPath ../data/glass_train.csv --columnToExclude glass_type --populationSize 5 --initPopulationType 1 --tournamentK 2 --crossoverProb 0.8 --mutationProb 0.2 --elitismNumber 2
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csvPath", required=True, help="Path to csv of dataset.", type=str)
    ap.add_argument("--columnToExclude", required=True, help="The label column to be excluded from the tests.", type=str)
    ap.add_argument("--populationSize", required=True, help="Number of individuals of a population.", type=int)
    ap.add_argument("--initPopulationType", required=True, help="Type of initialization, 1: grow; 2: full: 3: ramped half-and-half", type=int)
    ap.add_argument("--tournamentK", required=True, help="The size of K used for tournaments", type=int)
    ap.add_argument("--crossoverProb", required=True, help="Crossover probability in range [0, 1]", type=float)
    ap.add_argument("--mutationProb", required=True, help="Mutation probability in range [0, 1]", type=float)
    ap.add_argument("--elitismNumber", required=True, help="Number of individuals to elitism. Use 0 for no use elitism; must be an even number", type=int)
    args = vars(ap.parse_args())

    csvPath = args["csvPath"]
    columnToExclude = args["columnToExclude"]
    k = args["tournamentK"]
    crossoverProb = args["crossoverProb"]
    mutationProb = args["mutationProb"]
    elitismNumber = args["elitismNumber"]

    completeData, testData = initiatePoints(csvPath, columnToExclude)

    geneticProgramming(args["populationSize"], args["initPopulationType"], testData, completeData, columnToExclude, k, crossoverProb, mutationProb, elitismNumber)

    
                            

if __name__ == "__main__":
    main()