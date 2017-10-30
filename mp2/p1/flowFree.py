
from mp2.p1.cell import Cell

from timeit import default_timer
from random import randint


class FlowFree:
	"""
	FlowFree game initialized from a file.
	Variables: cells on the board
	Domain: list of all possible colors given by source cells
	Constraints: Cells can only have exactly 1 color. No zigzag. Two cells
	must be the same color with non-source cell and one cell must be same 
	color with source cell.
	"""

	def __init__(self, filename):
		# board holding cells, row major
		self.board = list()
		# source nodes
		self.sources = set()
		# domain
		self.colors = list()
		# num of unassigned cells
		self.unassigned = 0

		with open(filename, 'r') as f:
			for x, line in enumerate(f.readlines()):
				row = list()
				for y, c in enumerate(list(line.strip())):
					cell = Cell(x, y, c)
					if c != '_':
						cell.source = True
						self.sources.add(cell)
						self.colors.append(c)
					else:
						self.unassigned += 1
					row.append(cell)
				self.board.append(row)

		# turn colors into a list for random shuffling
		self.colors = list(set(self.colors))
		# num of assignments made
		self.assignments = 0

	def dumb(self):
		"""
		Dumb backtracking CSP algorithm
		:return: 
		:rtype: 
		"""
		# check if it is solved
		if self.unassigned == 0:
			return True
		# get next unassigned cell
		cell = self.get_unassigned()

		# get colors in random order
		# shuffle(self.colors)
		for color in self.colors:
			cell.value = color
			self.assignments += 1
			self.unassigned -= 1
			if self.check_constraints():
				res = self.dumb()
				if res:
					return res
			cell.value = '_'
			self.unassigned += 1
		return False

	def smart(self):
		"""
		Smart algorithm which uses different heuristics
		:return: 
		:rtype: 
		"""
		if self.unassigned == 0:
			return True
		cell = self.get_most_constrained()
		if cell is None:
			return False
		self.lca(cell)
		for color in cell.colors:
			cell.value = color
			self.unassigned -= 1
			if self.check_constraints():
				self.assignments += 1
				res = self.smart()
				if res:
					return res
				self.unassigned += 1
			cell.value = '_'
		return False

	def lca(self, cell):
		"""
		Rank the possibility of colors to a cell
		:param cell: 
		:type cell: 
		:return: 
		:rtype: 
		"""
		neighbors = self.get_neighbor(cell)
		counts = dict()
		for color in self.colors:
			counts[color] = 0
		for neighbor in neighbors:
			if neighbor == '_' or neighbor.value not in counts:
				continue
			counts[neighbor.value] += 1
		cell.available = sorted(counts, key=lambda k: counts[k], reverse=True)

	def get_most_constrained(self):
		"""
		Find the most constrained variable to assign
		:return: 
		:rtype: 
		"""
		max_color = len(self.colors) + 1
		var = None
		for row in self.board:
			for cell in row:
				if cell.value != '_':
					continue
				cell.colors = list()
				for color in self.colors:
					if self.forward_check(cell, color):
						cell.colors.append(color)
				# update most constrained/minimum remaining values
				if len(cell.colors) == 0:
					return None
				if len(cell.colors) < max_color:
					max_color = len(cell.colors)
					var = cell
				elif len(cell.colors) == max_color:
					if self.count_constraints(cell) > self.count_constraints(var):
						max_color = len(cell.colors)
						var = cell
		return var

	def count_constraints(self, cell):
		"""
		Get number of constraints of current cell
		:param cell: 
		:type cell: 
		:return: 
		:rtype: 
		"""
		count = 0
		for neighbor in self.get_neighbor(cell):
			if neighbor.value != '_':
				count += 1
		return count

	def forward_check(self, cell, color):
		"""
		Run forward checking with the cell assigned with this color
		:param cell: 
		:type cell: 
		:param color: 
		:type color: 
		:return: 
		:rtype: 
		"""
		neighbors = self.get_neighbor(cell)
		cell.value = color
		if not self.check_constraint(cell):
			cell.value = '_'
			return False
		# check if current assignment violates constraints for neighbors
		for neighbor in neighbors:
			if neighbor.value == '_':
				continue
			if not self.check_constraint(neighbor):
				cell.value = '_'
				return False
		cell.value = '_'
		return True

	def get_neighbor(self, cell):
		"""
		Get the neighbors of current cell
		:param cell: 
		:type cell: 
		:return: 
		:rtype: 
		"""
		neighbors = list()
		x, y = cell.x, cell.y
		if x > 0:
			neighbors.append(self.board[x-1][y])
		if x < len(self.board) - 1:
			neighbors.append(self.board[x+1][y])
		if y > 0:
			neighbors.append(self.board[x][y-1])
		if y < len(self.board[0]) - 1:
			neighbors.append(self.board[x][y+1])
		return neighbors

	def check_constraints(self):
		"""
		Check constraint for every cell
		:return: 
		:rtype: 
		"""
		for row in self.board:
			for cell in row:
				if cell.value == '_':
					continue
				if not self.check_constraint(cell):
					return False
		return True

	def check_constraint(self, cell):
		"""
		Check constraint for given cell
		:param cell: 
		:type cell: 
		:return: 
		:rtype: 
		"""
		neighbors = self.get_neighbor(cell)
		same, empty = 0, 0
		for neighbor in neighbors:
			if neighbor.value == '_':
				empty += 1
			elif neighbor.value == cell.value:
				same += 1
		# test all constraints
		if cell.source:
			if same + empty < 1:
				return False
			if same > 1:
				return False
		else:
			if same + empty < 2:
				return False
			if same > 2:
				return False
		return True

	def get_unassigned(self):
		"""
		Get unassigned cell randomly
		:return: 
		:rtype: 
		"""
		cells = list()
		for row in self.board:
			for cell in row:
				if cell.value == '_':
					cells.append(cell)
		if len(cells) == 0:
			return None
		return cells[randint(0, len(cells)-1)]

	def print(self):
		out = ""
		for row in self.board:
			for cell in row:
				out += cell.value
			out += "\n"
		print(out)


if __name__ == "__main__":
	dire = "input/"
	filenames = ["input77.txt", "input88.txt", "input991.txt", "input10101.txt", "input10102.txt"]
	for filename in filenames:
		print("Now working on file " + filename + "================")
		ff = FlowFree(dire+filename)
		ff.print()
		start = default_timer()
		if ff.smart():
			ff.print()
		print("Num of Assignments is " + str(ff.assignments))
		print("Running Time is " + str(default_timer() - start) + "s")
		outfile = "output/out" + filename[5:]
		with open(outfile, 'w+') as f:
			f.write()
