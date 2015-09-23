# coding=utf-8
"""genetic_programming.py

This file stands for the genetic programming class
that is used to execute the algorithm itself. It
contains genetic operators (such as crossover and
mutation).
"""

import numpy as np
from instantiation import *


class GeneticProgrammer:

	_n_individuals = None
	_elitism_rate = None
	_crossover_prob = None
	_tournament_size = None
	_mutation_rate = None
	_mutation_prob = None

	def __init__(self, **kwargs):
		"""
		:param n_individuals: population size for each generation. Minimum size is 6.

		:param elitism_rate: percentage of the population that will be considered elite, which will be
			added directly to the next population. Default value is 0.1 (10%).

		:param crossover_prob: probability of occurring crossover. Default value is 0.5 (50%).

		:param tournament_size:  the size of the tournament, which is responsible for choosing the parents
			that will be used in the crossover. Default value is 5 (5 participants).

		:param mutation_rate: related to the percentage of the population that will be mutated in each
			generation. Default value is 0.05 (5%).

		:param mutation_prob: probability of occurring mutation in a given individual. Default value is
			0.03 (3%).

		:type level: list
		:param level: The problem to be optimized.

		"""
		self._n_individuals = max(6, kwargs['n_individuals'])
		self._elitism_rate = 0.1 if 'elitism_rate' not in kwargs else kwargs['elitism_rate']
		self._crossover_prob = 0.5 if 'crossover_prob' not in kwargs else kwargs['crossover_prob']
		self._tournament_size = 5 if 'tournament_size' not in kwargs else kwargs['tournament_size']
		self._mutation_rate = 0.05 if 'mutation_rate' not in kwargs else kwargs['mutation_rate']
		self._mutation_prob = 0.03 if 'mutation_prob' not in kwargs else kwargs['mutation_prob']

	def __sample__(self, level):
		"""
		Generates the initial population of the evolution
		"""
		population = np.empty(self._n_individuals, dtype=np.object)

		tests = Tests.__members__.values()
		actions = Actions.__members__.values()

		for i, individual in enumerate(population):
			root = Node(value=np.random.choice(tests))

			tree_tests = [root]
			while len(tree_tests) > 0:  # while there are any non-terminal nodes without children
				draw = Node(np.random.choice(tests + actions))
				try:
					tree_tests[0].next_free = draw
					if draw.is_internal:
						tree_tests.append(draw)
				except NameError:
					tree_tests.remove(tree_tests[0])  # tree_tests[0] has no free branches

			population[i] = Tree(root=root, level=level)

		return population

	def find_solution(self, **kwargs):
		"""
		Executes the genetic program.

		:param max_iter: max number of generations in the execution.
		:param level: The level to be tested in the fitness function.
		:return: the best individual (solution) found to the problem.
		"""
		iteration = 0

		best = None
		max_iter = kwargs['max_iter']
		population = self.__sample__(kwargs['level'])

		while iteration < max_iter:
			population = sorted(population, key=lambda x: x.fitness, reverse=True)
			elite_factor = int(round(self._elitism_rate * self._n_individuals))
			elite = population[:elite_factor] if elite_factor > 0 else np.ndarray([])
			not_elite = population[elite_factor:] if elite_factor > 0 else population
			do_crossover = np.random.choice([True, False], p=[self._crossover_prob, 1. - self._crossover_prob])
			do_mutation = np.random.choice([True, False], p=[self._mutation_prob, 1. - self._mutation_prob])
			if do_crossover:
				taken = []
				while len(taken) < len(population):
					fathers = []
					for i in range(2):  # two parents for each crossover
						tournament = np.random.choice(population, size=self._tournament_size)
						father = sorted(tournament, key=lambda x: x.fitness, reverse=True)[0]  # fittest individual is the parent
						taken += [father]
						fathers += [father]
					Tree.crossover(*fathers)

			if do_mutation:
				n_to_mutate = int(round(self._mutation_rate * len(not_elite)))
				to_mutate = np.random.choice(not_elite, size=n_to_mutate)
				for individual in to_mutate:
					individual.mutate()

			population = elite + not_elite
			iteration += 1

		return best

	@staticmethod
	def calculate_fitness(population, level):
		"""
		:param population: A list of Tree objects.

		:type level: list
		:param level: A list of tiles of a given level.

		:rtype: list
		:return: List of fitness of individuals in the population.
		"""
		return map(lambda x: x.__calculate_fitness__(level), population)
