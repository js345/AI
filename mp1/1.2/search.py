
from copy import deepcopy
from state import State


class Search:
	"""
	Top level search routine for BFS, DFS, Greedy, A*
	"""

	dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

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

	@staticmethod
	def manhattan(state, dot):
		x, y = state.x, state.y
		return abs(dot[0] - x) + abs(dot[1] - y)

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
		dot = '0'
		for state in states:
			x, y = state.x, state.y
			if state.capture:
				graph[x][y] = dot
				if dot == '9':
					dot = 'a'
				elif dot == 'z':
					dot = 'A'
				else:
					dot = chr(ord(dot) + 1)
		res = ""
		for line in graph:
			res += ''.join(line)
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

	def astar(self, frontier):
		self.reset()
		frontier.put((0, self.start_state))
		self.visited.add(self.start_state)
		# start search, unreachable if return None
		while not frontier.empty():
			h, state = frontier.get()
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
				# compute heuristic and add current cost
				expand.heuristic = self.nearest_heuristic(expand) + expand.cost
				expand.parent = state
				if expand not in self.visited:
					frontier.put((expand.heuristic, expand))
					self.visited.add(expand)

	def sum_heuristic(self, state):
		"""
		Heuristic of adding up all manhattan distance from current state to all
		remaining dots not collected.
		:param state: 
		:type state: 
		:return: 
		:rtype: 
		"""
		dots = self.maze.dots
		heuristic = 0
		for idx, dot in enumerate(dots):
			if state.bits[idx] == 1:
				heuristic += Search.manhattan(state, dot)
		return heuristic

	def nearest_heuristic(self, state):
		"""
		Heuristic of finding manhattan distance from current state to the
		closest dot not collected.
		:param state: 
		:type state: 
		:return: 
		:rtype: 
		"""
		dots = self.maze.dots
		heuristic = 9999999999
		for idx, dot in enumerate(dots):
			if state.bits[idx] == 1 and heuristic >= Search.manhattan(state, dot):
				heuristic = Search.manhattan(state, dot)
		return heuristic
