"""game.py

This file stands for the main entry point
of the whole algorithm.
"""

from instantiation import Adversities
from genetic_programming import GeneticProgrammer
import numpy as np
from matplotlib import pyplot as plt
import random

if __name__ == "__main__":
	random.seed(2)
	np.random.seed(2)

	n_individuals = 10
	max_iter = 100
	level = ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'P', 'H', 'P', 'P', 'E', 'E', 'P', 'P']

	gp = GeneticProgrammer(n_individuals=n_individuals)  # , crossover_prob=1., mutation_prob=1., mutation_rate=0.5)
	fittest = gp.find_solution(max_iter=max_iter, level=level)
	print fittest.fitness
	fittest.plot()
	plt.show()

