
from copy import deepcopy
from state import State


class Search:
	"""
	Top level search routine for BFS, DFS, Greedy, A*
	"""

	dirs = [(0, -1), (-1, 0), (1, 0), (0, 1)]

	def __init__(self, start_state, goal_states, maze):
		"""
		Constructor for uniformed search routine
		:param start_state: start state of search
		:type start_state: 
		:param goal_states: set of goal states
		:type goal_states: set
		:param maze: maze with current configuration
		:type maze: Maze
		"""
		self.start_state = start_state
		self.goal_states = goal_states
		self.maze = maze
		# explored set keeps visited states
		self.visited = set()
		# path & path cost & #ofnodes expanded
		self.path = list()
		self.path_cost = 0
		self.node_number = 0

	def reset(self):
		# explored set keeps visited states
		self.visited = set()
		# path & path cost & #ofnodes expanded
		self.path = list()
		self.path_cost = 0
		self.node_number = 0

	def manhattan(self, state):
		x, y = state.x, state.y
		return abs(self.maze.dots[0][0] - x) + abs(self.maze.dots[0][1] - y)

	def display(self, state):
		"""
		Display the path of solving the maze
		:param state: 
		:type state: 
		:return: 
		:rtype: 
		"""
		states = list()
		while state is not None:
			states.append(state)
			state = state.parent
		states.reverse()
		graph = deepcopy(self.maze.graph)
		for state in states:
			x, y = state.x, state.y
			graph[x][y] = '.'
		res = ""
		for line in graph:
			res += ''.join(line) + "\n"
		return res

	def bfs(self, frontier):
		self.reset()
		frontier.put(self.start_state)
		self.visited.add(self.start_state)
		# start search, unreachable if return None
		while not frontier.empty():
			state = frontier.get()
			self.node_number += 1
			if state in self.goal_states:
				print("Expanded %r nodes" % self.node_number)
				print("The path cost is %r" % state.cost)
				return self.display(state)
			for di in Search.dirs:
				x, y = state.x + di[0], state.y + di[1]
				# not a wall
				if x < 0 or y < 0 or x >= self.maze.n or y >= self.maze.m or self.maze.graph[x][y] == '%':
					continue
				# deepcopy bits from the current state
				next_bits = list(deepcopy(state.bits))
				# if it's a dot and not eaten yet, change the bit to zero
				capture = False
				if self.maze.graph[x][y] == '.' and state.bits[self.maze.dots.index((x, y))] == 1:
					capture = True
					next_bits[self.maze.dots.index((x, y))] = 0
				# convert back to tuple so we can hash it
				next_bits = tuple(next_bits)
				expand = State(x, y, next_bits, capture)
				expand.cost = state.cost + 1
				expand.parent = state
				if expand not in self.visited:
					frontier.put(expand)
					self.visited.add(expand)

	def dfs(self, frontier):
		self.reset()
		return self.bfs(frontier)

	def greedy(self, frontier):
		self.reset()
		frontier.put(self.start_state)
		self.visited.add(self.start_state)
		# start search, unreachable if return None
		while not frontier.empty():
			state = frontier.get()
			self.node_number += 1
			if state in self.goal_states:
				print("Expanded %r nodes" % self.node_number)
				print("The path cost is %r" % state.cost)
				return self.display(state)
			for di in Search.dirs:
				x, y = state.x + di[0], state.y + di[1]
				# not a wall
				if x < 0 or y < 0 or x >= self.maze.n or y >= self.maze.m or self.maze.graph[x][y] == '%':
					continue
				# deepcopy bits from the current state
				next_bits = list(deepcopy(state.bits))
				# if it's a dot and not eaten yet, change the bit to zero
				capture = False
				if self.maze.graph[x][y] == '.' and state.bits[self.maze.dots.index((x, y))] == 1:
					capture = True
					next_bits[self.maze.dots.index((x, y))] = 0
				# convert back to tuple so we can hash it
				next_bits = tuple(next_bits)
				expand = State(x, y, next_bits, capture)
				expand.cost = state.cost + 1
				# compute heuristic for manhattan distance
				expand.heuristic = self.manhattan(expand)
				expand.parent = state
				if expand not in self.visited:
					frontier.put(expand)
					self.visited.add(expand)

	def astar(self, frontier):
		self.reset()
		frontier.put(self.start_state)
		self.visited.add(self.start_state)
		# start search, unreachable if return None
		while not frontier.empty():
			state = frontier.get()
			self.node_number += 1
			if state in self.goal_states:
				print("Expanded %r nodes" % self.node_number)
				print("The path cost is %r" % state.cost)
				return self.display(state)
			for di in Search.dirs:
				x, y = state.x + di[0], state.y + di[1]
				# not a wall
				if x < 0 or y < 0 or x >= self.maze.n or y >= self.maze.m or self.maze.graph[x][y] == '%':
					continue
				# deepcopy bits from the current state
				next_bits = list(deepcopy(state.bits))
				# if it's a dot and not eaten yet, change the bit to zero
				capture = False
				if self.maze.graph[x][y] == '.' and state.bits[self.maze.dots.index((x, y))] == 1:
					capture = True
					next_bits[self.maze.dots.index((x, y))] = 0
				# convert back to tuple so we can hash it
				next_bits = tuple(next_bits)
				expand = State(x, y, next_bits, capture)
				expand.cost = state.cost + 1
				# compute heuristic for manhattan distance and current cost
				expand.heuristic = self.manhattan(expand) + expand.cost
				expand.parent = state
				if expand not in self.visited:
					frontier.put(expand)
					self.visited.add(expand)
