
from queue import Queue, LifoQueue, PriorityQueue
from search import Search
from state import State


class Maze:
	"""
	Maze class to store input maze, start position and dot positions
	"""

	def __init__(self, filename):
		# maze is a list of list of chars
		self.graph = list()
		# dots positions is a list of tuples of (i, j)
		self.dots = list()
		# start point
		self.start = (0, 0)
		# dimension of maze
		self.n = 0
		self.m = 0

		# read the maze graph from file
		with open(filename, "r") as file:
			for i, line in enumerate(file.readlines()):
				self.graph.append(list(line))
				for j, c in enumerate(list(line)):
					if c == 'P':
						self.start = (i, j)
					elif c == '.':
						self.dots.append((i, j))

		# update dimension of the maze
		self.n = len(self.graph)
		self.m = len(self.graph[0]) if self.n > 0 else 0

	def display_maze(self):
		"""
		Display function to show the current maze status
		:return: None
		:rtype: None
		"""
		for line in self.graph:
			print(''.join(line))


def build_search(name, maze):
	# create the start state
	x, y = maze.start
	bits = tuple(1 for _ in range(len(maze.dots)))
	start_state = State(x, y, bits)
	# enumerate the goal states
	goal_states = set()
	end = tuple(0 for _ in range(len(maze.dots)))
	for x, y in maze.dots:
		goal_states.add(State(x, y, end))
	# construct the search object
	print("============Working on Maze %s ===============\n" % name)
	search = Search(start_state, goal_states, maze)
	print("====Running BFS======")
	frontier = Queue()
	print(search.bfs(frontier))

	print("====Running DFS======")
	frontier = LifoQueue()
	print(search.dfs(frontier))

	print("====Running Greedy======")
	frontier = PriorityQueue()
	print(search.greedy(frontier))

	print("====Running A*======")
	frontier = PriorityQueue()
	print(search.astar(frontier))

if __name__ == "__main__":
	path = "input/"
	maze_files = ["mediumMaze.txt", "bigMaze.txt", "openMaze.txt"]
	for maze_file in maze_files:
		maze = Maze(path+maze_file)
		build_search(maze_file, maze)
		break
