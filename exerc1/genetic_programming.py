# coding=utf-8

"""
This file stands for the genetic programming class
that is used to execute the algorithm itself. It
contains genetic operators (such as crossover and
mutation).
"""

from instantiation import *


class GeneticProgrammer:

	_n_individuals = None
	_elitism_rate = None
	_crossover_prob = None
	_tournament_size = None
	_mutation_rate = None
	_mutation_prob = None
	_max_initial_height = None

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

		:param max_initial_height: Maximum size of initial trees in the population. Defaults to 5.

		:type level: list
		:param level: The problem to be optimized.

		"""
		self._n_individuals = max(6, kwargs['n_individuals'])
		self._elitism_rate = 0.1 if 'elitism_rate' not in kwargs else max(0., kwargs['elitism_rate'])
		self._crossover_prob = 0.5 if 'crossover_prob' not in kwargs else max(0., kwargs['crossover_prob'])
		self._tournament_size = 5 if 'tournament_size' not in kwargs else max(2, kwargs['tournament_size'])
		self._mutation_rate = 0.05 if 'mutation_rate' not in kwargs else max(0., kwargs['mutation_rate'])
		self._mutation_prob = 0.03 if 'mutation_prob' not in kwargs else max(0., kwargs['mutation_prob'])
		self._max_initial_height = 5 if 'max_initial_height' not in kwargs else max(2, kwargs['max_initial_height'])

	def __sample__(self, level):
		"""
		Generates the initial population of the Genetic Programmer.
		"""
		population = np.empty(self._n_individuals, dtype=np.object)

		tests = Tests.__members__.values()
		actions = Actions.__members__.values()

		for i, individual in enumerate(population):
			root = Node(value=np.random.choice(tests))

			tree_tests = [root]
			while len(tree_tests) > 0:  # while there are any non-terminal nodes without children
				if root.depth_below() + 1 < self._max_initial_height:
					draw = Node(np.random.choice(tests + actions))
				else:
					draw = Node(np.random.choice(actions))
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

		max_iter = kwargs['max_iter']
		population = self.__sample__(kwargs['level'])

		while iteration < max_iter:
			population = sorted(population, key=lambda x: x.fitness, reverse=True)  # sorts population
			n_elite = int(round(self._elitism_rate * self._n_individuals))  # number of elite individuals

			elite = population[:n_elite] if n_elite > 0 else []
			not_elite = population[n_elite:] if n_elite > 0 else population

			do_crossover = np.random.choice([True, False], p=[self._crossover_prob, 1. - self._crossover_prob])
			do_mutation = np.random.choice([True, False], p=[self._mutation_prob, 1. - self._mutation_prob])

			if do_crossover:
				GeneticProgrammer.tournament(population, self._tournament_size)

			if do_mutation:
				GeneticProgrammer.mutation(self._mutation_rate, not_elite)

			population = elite + not_elite
			iteration += 1

		return sorted(population, key=lambda x: x.fitness, reverse=True)[0]  # returns the fittest individual

	@staticmethod
	def tournament(population, tournament_size):
		taken = []
		while len(taken) < len(population):
			fathers = []
			for i in range(2):  # two parents for each crossover
				tournament = np.random.choice(population, size=tournament_size)
				father = sorted(tournament, key=lambda x: x.fitness, reverse=True)[0]  # fittest individual is the parent
				taken += [father]
				fathers += [father]
			Tree.crossover(*fathers)

	@staticmethod
	def mutation(mutation_rate, sample):
		"""
		Performs mutation in the not-elite population.
		:param mutation_rate: The rate of the sample to mutate.
		:param sample: The not-elite subpopulation.
		"""

		n_to_mutate = int(round(mutation_rate * len(sample)))
		to_mutate = np.random.choice(sample, size=n_to_mutate)
		for individual in to_mutate:
			individual.mutate()
