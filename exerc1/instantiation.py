import copy

__author__ = 'Henry'

from enum import Enum
import networkx as nx
from matplotlib import pyplot as plt
import itertools
import numpy as np

class Adversities(Enum):
	plain = 'P'
	hole = 'H'
	enemy = 'E'


class Actions(Enum):
	move_right = 'R'
	jump = 'J'
	fire = 'F'

	@staticmethod
	def run(action, tile):
		if action == Actions.move_right:
			return Actions.__move_right__(tile)
		elif action == Actions.jump:
			return Actions.__jump__(tile)
		elif Actions.fire:
			return Actions.__fire__(tile)
		return False

	@staticmethod
	def __move_right__(tile):
		if Tests.is_enemy_func(tile) or Tests.is_hole_func(tile):
			return False
		return True

	@staticmethod
	def __jump__(tile):
		return True

	@staticmethod
	def __fire__(tile):
		if Tests.is_hole_func(tile):
			return False
		return True


# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


class Tests(Enum):
	is_enemy = 'IE'
	is_hole = 'IH'
	is_plain = 'IP'

	@staticmethod
	def run(test, tile):
		if test == Tests.is_enemy:
			return Tests.is_enemy_func(tile)
		elif test == Tests.is_hole:
			return Tests.is_hole_func(tile)
		elif test == Tests.is_plain:
			return Tests.is_plain_func(tile)
		return False

	@staticmethod
	def is_plain_func(tile):
		"""
		Verifies if the given position is a plain.
		:param tile: the level vector position
		:return: True if it's a plain. False otherwise.
		"""
		return tile == Adversities.plain.value

	@staticmethod
	def is_hole_func(tile):
		"""
		Verifies if the given position is a hole.
		:param tile: the level vector position
		:return: True if it's a hole. False otherwise.
		"""
		return tile == Adversities.hole.value

	@staticmethod
	def is_enemy_func(tile):
		"""
		Verifies if the given position is a enemy.
		:param tile: the level vector position
		:return: True if it's a enemy. False otherwise.
		"""
		return tile == Adversities.enemy.value


# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


class Node(object):
	_test = None
	_positive = None
	_negative = None
	_father = None

	def __init__(self, value, father=None, positive=None, negative=None):
		self._test = value
		self._father = father
		self._positive = positive
		self._negative = negative

		if positive is not None:
			self._positive.father = self

		if negative is not None:
			self._negative.father = self

	@property
	def test(self):
		return self._test

	@test.setter
	def test(self, value):
		self._test = value

	@property
	def father(self):
		return self._father

	@father.setter
	def father(self, value):
		self._father = value

	def __str__(self):
		return str(self.test)

	def behave(self, tile):
		if self.is_terminal:
			return Actions.run(self._test, tile)
		else:
			if Tests.run(self._test, tile):
				return self.positive.behave(tile)
			else:
				return self.negative.behave(tile)

	@property
	def is_terminal(self):
		return self._test in Actions

	@property
	def is_internal(self):
		return self._test in Tests

	def depth_below(self):
		"""
		:return: Depth of the tree below this node.
		"""
		depth_positive = self._positive.depth_below() if self._positive is not None else 0
		depth_negative = self._negative.depth_below() if self._negative is not None else 0
		return 1 + max(depth_positive, depth_negative)

	def nodes_below(self):
		nodes_positive = self._positive.nodes_below() if self._positive is not None else []
		nodes_negative = self._negative.nodes_below() if self._negative is not None else []
		return [self] + nodes_negative + nodes_positive

	def terminals_below(self):
		terminals_positive = self._positive.terminals_below() if self._positive is not None else []
		terminals_negative = self._negative.terminals_below() if self._negative is not None else []
		return [self] if self.is_terminal else [] + terminals_negative + terminals_positive

	def internals_below(self):
		internals_positive = self._positive.internals_below() if self._positive is not None else []
		internals_negative = self._negative.internals_below() if self._negative is not None else []
		return [self] if self.is_internal else [] + internals_negative + internals_positive

	@property
	def next_free(self):
		if self.positive is None:
			return self._positive
		elif self.negative is None:
			return self.negative
		else:
			raise NameError('No free children!')

	@next_free.setter
	def next_free(self, value):
		if self._positive is None:
			self._positive = value
		elif self._negative is None:
			self._negative = value
		else:
			raise NameError('No free children!')

		value.father = self

	@property
	def test(self):
		return self._test

	@property
	def positive(self):
		return self._positive

	@property
	def negative(self):
		return self._negative

	@positive.setter
	def positive(self, value):
		self._positive = value

	@negative.setter
	def negative(self, value):
		self._negative = value


class Tree(object):
	_root = None
	_fitness = -1.
	_level = None

	def __init__(self, root, level):
		"""
		:param root: Root node.
		:param level: Level to evaluate.
		"""
		self._root = root
		self._level = level

		self.__calculate_fitness__()

	def __calculate_fitness__(self):
		"""
		Calculates the fitness of this individual, setting its attribute
		and also returning the value.
		"""
		summation = 0
		for tile in self._level:
			result = self._root.behave(tile)
			if not result:
				break  # fails to solve the problem
			else:
				summation += result

		self.fitness = float(summation) / len(self._level)
		return self.fitness

	def mutate(self):
		random_node = np.random.choice(self.nodes)
		node_type = Actions if random_node.test in Actions else Tests
		new_value = np.random.choice(node_type.__members__.values())
		random_node._test = new_value

	@staticmethod
	def crossover(a, b):
		"""
		Performs crossover between two trees a and b.
		"""
		node_a = np.random.choice(a.nodes)  # randomly gets a node in the A tree
		node_b = np.random.choice(b.nodes)  # randomly gets a node in the B tree

		node_a_father = node_a.father  # father of A node
		node_b_father = node_b.father  # father of B node

		# if node A has a father, and node A is
		# allocated in the positive pointer in its father
		if node_a_father is not None and node_a_father.positive is node_a:
			node_a_father.positive = node_b
		elif node_a.father is not None:
			node_a_father.negative = node_b

		node_b.father = node_a_father

		# if node B has a father, and node B is
		# allocated in the positive pointer in its father
		if node_b_father is not None and node_b_father.positive is node_b:
			node_b_father.positive = node_a
		elif node_b.father is not None:
			node_b_father.negative = node_a

		node_a.father = node_b_father

	@property
	def nodes(self):
		return self._root.nodes_below()

	@property
	def depth(self):
		return self._root.depth_below()

	@property
	def fitness(self):
		return self._fitness

	@fitness.setter
	def fitness(self, value):
		self._fitness = value

	def __str__(self):
		return str(self.fitness)

	def plot(self):
		plt.figure()

		all_nodes = self._root.nodes_below()
		aliases = [str(x) for i, x in enumerate(all_nodes)]

		G = nx.DiGraph()

		edges = []
		for i, (alias, node) in enumerate(itertools.izip(aliases, all_nodes)):
			G.add_node(i)
			if node.is_internal:
				positive_pair = (i, all_nodes.index(node.positive))
				negative_pair = (i, all_nodes.index(node.negative))
				edges += [(positive_pair, 'yes'), (negative_pair, 'no')]
				G.add_edge(*positive_pair)
				G.add_edge(*negative_pair)

		pos = nx.spring_layout(G)
		node_labels = dict(itertools.izip(xrange(len(aliases)), aliases))
		edge_labels = dict(edges)

		nx_edge_labels = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=16)
		nx.draw(G, pos, labels=node_labels, edge_labels=nx_edge_labels)
		plt.draw()
		# plt.show()
