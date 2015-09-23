"""genetic_programming.py

This file stands for the genetic programming class
that is used to execute the algorithm itself. It
contains genetic operators (such as crossover and
mutation).
"""

import random;
import genetic_operators;
from tree import Tree;
import utils;

class GeneticProgramming:

    def __init__(self,populationSize,maxGenerations,elitismPercentage=0.1,crossoverProbability=0.5,tournamentSize=5,mutationPercentage=0.05,mutationProbability=0.03):
        """
        "Constructor" of the class. Initializes the main components and parameters
        of the Genetic Program.

        :param populationSize:       population size of each generation.
        :param maxGenerations:       max number of generations in the execution.
        :param elitismPercentage:    percentage of the population that will be considered elite, which will be
                                     added directly to the next population. Default value is 0.1 (10%).
        :param crossoverProbability: probability of occurring crossover. Default value is 0.5 (50%).
        :param tournamentSize:       the size of the tournament, which is responsible for choosing the parents
                                     that will be used in the crossover. Default value is 5 (5 participants).
        :param mutationPercentage:   related to the percentage of the population that will be mutated in each
                                     generation. Default value is 0.05 (5%).
        :param mutationProbability:  probability of occurring mutation in a given individual. Default value is
                                     0.03 (3%).
        """
        self.functions = [utils.isHole1StepsLeft,utils.isPlain1StepsLeft,utils.isEnemy1StepsLeft, 
                        utils.isHole2StepsLeft,utils.isPlain2StepsLeft,utils.isEnemy2StepsLeft,
                        utils.isHole1StepsRight,utils.isPlain1StepsRight,utils.isEnemy1StepsRight,
                        utils.isHole2StepsRight,utils.isPlain2StepsRight,utils.isEnemy2StepsRight];
        self.terminals = [n.value for n in utils.Moves];

        self.population = [];

        # Tamanho da populacao
        self.populationSize =  populationSize

        # Numero maximo de geracoes
        self.maxGenerations = maxGenerations;

        # Percentual de Elitismo
        self.elitismPercentage = elitismPercentage;

        # Probabilidade de Ocorrencia de  Croosover
        self.crossoverProbability = crossoverProbability;

        # Tamanho do torneio
        self.tournamentSize = tournamentSize;

               # Probabilidade de Ocorrencia de Mutacao 
        self.mutationPercentage = mutationPercentage;

               # Probabilidade de Mutacao dos nodos
        self.mutationProbability = mutationProbability;


    def generateInitialPopulation(self):
        """
        Generates the initial population of the evolution
        """
        # Código para geração da população inicial
        pass

    def run(self):
        """
        Executes the genetic program.
        :return: the best individual (solution) found to the problem.
        """

        numGenerations = 0;

        while(numGenerations < self.maxGenerations):
            newGeneration = [];

            #Coloque aqui o seu código para execução de GP

            numGenerations = numGenerations + 1;

        return self.population[0];


