import copy

__author__ = 'Henry'

from enum import Enum
import networkx as nx
from matplotlib import pyplot as plt
import itertools
import numpy as np


class Adversities(Enum):
	"""
	Possible adversities that the player may find in the level.
	"""
	plain = 'P'
	hole = 'H'
	enemy = 'E'


class Actions(Enum):
	"""
	Possible actions the player may take upon the adversities.
	"""
	move_right = 'R'
	jump = 'J'
	fire = 'F'

	@staticmethod
	def run(action, tile):
		"""
		Given an action, verifies if it is an adequate behaviour
		to perform upon encountering the given tile.

		:param action: An member of the Actions class.
		:param tile: The tile to behaviour upon.
		:return: True if the action is adequate to attack the tile,
			False otherwise.
		"""
		if action == Actions.move_right:
			return Actions.__move_right__(tile)
		elif action == Actions.jump:
			return Actions.__jump__(tile)
		elif Actions.fire:
			return Actions.__fire__(tile)
		return False

	@staticmethod
	def __move_right__(tile):
		"""
		Performs the action to move right.
		:param tile: A given tile to behave upon.
		:return: True if moving right is an appropriate action
			upon encountering the given tile.
		"""
		if Tests.is_enemy_func(tile) or Tests.is_hole_func(tile):
			return False
		return True

	@staticmethod
	def __jump__(tile):
		"""
		Jumps.
		:param tile: A given tile to behave upon.
		:return: True, because Mario's nickname is Jumpman
			and you don't mess with someone like him.
		"""
		return True

	@staticmethod
	def __fire__(tile):
		"""
		Fires a fireball.
		:param tile: A given tile to behave upon.
		:return: True if firing is an appropriate action
			upon encountering the given tile.
		"""
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
		"""
		Given a test, performs a test given a tile.

		:param test: An member of the Tests class.
		:param tile: The tile to test upon.
		:return: The result of the test over the given tile.
		"""
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
		"""
		Initializes a Node object.

		:param value: Value of the node. May be a test or an action.
		:param father: The father of this node, if any. Otherwise is a root.
		:param positive: Only test nodes have branches. This branch corresponds
			to the positive outcome of the test of this node, if it is a Test).
		:param negative: Only test nodes have branches. This branch corresponds
			to the negative outcome of the test of this node, if it is a Test).
		:return:
		"""
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

	@property
	def positive(self):
		return self._positive

	@positive.setter
	def positive(self, value):
		self._positive = value

	@property
	def negative(self):
		return self._negative

	@negative.setter
	def negative(self, value):
		self._negative = value

	@property
	def is_action(self):
		return self._test in Actions

	@property
	def is_test(self):
		return self._test in Tests

	@property
	def next_free(self):
		"""
		:return: Next free branch of this node. Raises an exception
			if none.
		"""
		if self.positive is None:
			return self._positive
		elif self.negative is None:
			return self.negative
		else:
			raise NameError('No free children!')

	@next_free.setter
	def next_free(self, value):
		"""
		:return: Sets the next free branch of this node. Raises an exception
			if none.
		"""
		if self._positive is None:
			self._positive = value
		elif self._negative is None:
			self._negative = value
		else:
			raise NameError('No free children!')

		value.father = self

	def __str__(self):
		return str(self.test)

	def behave(self, tile):
		"""
		Behaves upon a given tile.
		:param tile: Any tile described in the Adversities class.
		:return: Positive if this node and all of its
			dependent nodes respond adequately to the
			given tile. False otherwise.
		"""
		if self.is_action:
			return Actions.run(self._test, tile)
		else:
			if Tests.run(self._test, tile):
				return self.positive.behave(tile)
			else:
				return self.negative.behave(tile)

	def depth_below(self):
		"""
		:return: Depth of the tree below this node.
		"""
		depth_positive = self._positive.depth_below() if self._positive is not None else 0
		depth_negative = self._negative.depth_below() if self._negative is not None else 0
		return 1 + max(depth_positive, depth_negative)

	def nodes_below(self):
		"""
		:return: All nodes (including itself) below this node.
		"""
		nodes_positive = self._positive.nodes_below() if self._positive is not None else []
		nodes_negative = self._negative.nodes_below() if self._negative is not None else []
		return [self] + nodes_negative + nodes_positive

	def terminals_below(self):
		"""
		:return: All terminals below this node, or itself if this node is a Terminal.
		"""
		terminals_positive = self._positive.terminals_below() if self._positive is not None else []
		terminals_negative = self._negative.terminals_below() if self._negative is not None else []
		return [self] if self.is_action else [] + terminals_negative + terminals_positive

	def internals_below(self):
		"""
		:return: All internals (including itself, if a Test) below this node.
		"""
		internals_positive = self._positive.internals_below() if self._positive is not None else []
		internals_negative = self._negative.internals_below() if self._negative is not None else []
		return [self] if self.is_test else [] + internals_negative + internals_positive


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

		self.calculate_fitness()

	def __str__(self):
		return str(self.fitness)

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

	def calculate_fitness(self):
		"""
		Calculates the fitness of this individual, setting its attribute.
		"""
		summation = 0
		for tile in self._level:
			result = self._root.behave(tile)
			if not result:
				break  # fails to solve the problem
			else:
				summation += result
		self._fitness = float(summation) / len(self._level)
		# z = 0

	def mutate(self):
		"""
		Mutates this tree.
		"""
		all_nodes_of_tree = self._root.nodes_below()
		random_node = np.random.choice(all_nodes_of_tree)
		node_type = Actions if random_node.test in Actions else Tests
		new_value = np.random.choice(node_type.__members__.values())
		random_node._test = new_value

		self.calculate_fitness()

	@staticmethod
	def crossover(a, b):
		"""
		Performs crossover between two trees a and b.
		"""
		node_a = np.random.choice(a._root.nodes_below())  # randomly gets a node in the A tree
		node_b = np.random.choice(b._root.nodes_below())  # randomly gets a node in the B tree

		# prevents the root from being selected
		while node_a.father is None:
			node_a = np.random.choice(a._root.nodes_below())  # randomly gets a node in the A tree

		while node_b.father is None:
			node_b = np.random.choice(b._root.nodes_below())  # randomly gets a node in the B tree

		node_a_father = node_a._father  # father of A node
		node_b_father = node_b._father  # father of B node

		# if node A has a father, and node A is
		# allocated in the positive pointer in its father
		if node_a_father._positive is node_a:
			node_a_father._positive = node_b
		else:
			node_a_father._negative = node_b

		if node_b_father._positive is node_b:
			node_b_father._positive = node_a
		else:
			node_b_father._negative = node_a

		node_b._father = node_a_father
		node_a._father = node_b_father

		# recalculates fitness
		a.calculate_fitness()
		b.calculate_fitness()

	def plot(self):
		"""
		Plots this tree using matplotlib and networkx.
		:return:
		"""
		plt.figure()

		all_nodes = self._root.nodes_below()
		aliases = [str(x) for i, x in enumerate(all_nodes)]

		G = nx.DiGraph()

		edges = []
		for i, (alias, node) in enumerate(itertools.izip(aliases, all_nodes)):
			G.add_node(i)
			if node.is_test:
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
