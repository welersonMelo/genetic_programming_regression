#!/bin/python
import os
import argparse
import sys

import input_reader as ir
import terminals_set as terminal
import genotype
import k_means

from random import randint

def full(populationSize, maxDeep):
    populationGenotype = []
    for i in range(populationSize):
        tree = genotype.generateOne(2, maxDeep)
        populationGenotype.append(tree)
    return populationGenotype

def grow(populationSize. maxDeep):
    populationGenotype = []
    for i in range(populationSize):
        tree = genotype.generateOne(1, maxDeep)
        populationGenotype.append(tree)
    return populationGenotype

def generatePopulation(populationSize, initType):
    if initType == 1:
        return grow(populationSize, 7)
    elif initType == 2:
        return full(populationSize, 7)


def getFitness(gene, testData, completeData, columnToExclude):
    # Calculando Fitness

    function = genotype.mapToFenotype(gene)

    clustersNumber = 7 # passar esse valor como parametro
    clusters = k_means.modelTrain(function, clustersNumber, testData)
    fitness = k_means.modelEvaluation(clusters, completeData, columnToExclude)

    return fitness

def selectionTournament(populationFitness, k):
    individual1 = randint(0, len(populationFitness)-1)
    individual2 = randint(0, len(populationFitness)-1)

    if populationFitness[individual1] >= populationFitness[individual2]:
        return individual1
    else:
        return individual2

def crossover(parent1, parent2, crossoverProb):
    probability = randint(0, 100)/100.0
    if probability <= crossoverProb:
        #make crossover and return generated childs

    
    return parent1, parent2

def mutateGene(gene):
    # mutation ...

    return gene

def mutation(population, mutationProb):
    popSize = len(population)
    for i in range(popSize):
        probability = randint(0, 100)/100.0
        if probability <= mutationProb:
            population[i] = mutateteGene(population[i])
    return population

def geneticProgramming(populationSize, initType, testData, completeData, columnToExclude, k, crossoverProb, mutationProb, elitismNumber):
    populationGenotype = generatePopulation(populationSize, initType)

    for generation in range(populationSize):
        populationFitness = []

        for gene in populationGenotype:
            populationFitnesse.append(getFitness(gene, testData, completeData, columnToExclude))

        # selection
        newPopulation = []
        for i in range(int(populationSize/2) - elitismNumber):
            parent1 = selectionTournament(populationFitness, k)
            parent2 = selectionTournament(populationFitness, k)
            child1, child2 = crossover(parent1, parent2, crossoverProb)
            newPopulation.append(child1)
            newPopulation.append(child2)
        # elitism
        for i in range(elitismNumber):
            maxId = populationFitness.index(max(populationFitness))
            newPopulation.append(populationGenotype[maxId])
            populationFitness[maxId] = -1

        populationGenotype = mutation(newPopulation, mutationProb)


def initiatePoints(csvPath, columnToExclude):
    completeData = ir.readCsv(csvPath)
    testData = completeData.drop([columnToExclude], axis=1)
    terminal.initSet(list(testData.columns.values))
    return completeData, testData

#in e.g.: python run.py --csvPath ../data/glass_test.csv --columnToExclude glass_type --populationSize 5 --initPopulationType 1 --tournamentK 2 --crossoverProb 0.8 --mutationProb 0.2 --elitismNumber 2
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