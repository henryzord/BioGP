"""game.py

This file stands for the main entry point
of the whole algorithm.
"""

from instantiation import Adversities
from genetic_programming import GeneticProgrammer
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
	np.random.seed(2)

	n_individuals = 2
	max_iter = 100
	level = ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P', 'H', 'P', 'P', 'P', 'P', 'H', 'P', 'P', 'E', 'E', 'P', 'P']

	gp = GeneticProgrammer(n_individuals=n_individuals, crossover_prob=1.)
	fittest = gp.find_solution(max_iter=max_iter, level=level)
	fittest.plot()

	# self._elitism_rate = kwargs['elitism_rate']
	# self._crossover_prob = kwargs['crossover_rate']
	# self._tournament_size = kwargs['tournament_size']
	# self._mutation_rate = kwargs['mutation_rate']
	# self._mutation_prob = kwargs['mutation_prob']

	plt.show()

