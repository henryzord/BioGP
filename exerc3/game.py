"""game.py

This file stands for the main entry point
of the whole algorithm.
"""

from genetic_programming import GeneticProgramming
import utils

if __name__ == "__main__":

    populationSize = 1000;
    maxGenerations = 100;

    gp = GeneticProgramming(populationSize, maxGenerations);
    bestIndividual = gp.run();

    print("Return Individual");
    print( "Fitness %i" % bestIndividual.fitness);
    print("Depth %i" % bestIndividual.depth());
    print(bestIndividual);
