
from functools import total_ordering


@total_ordering
class State:
	"""
	General class for states used in search
	"""

	def __init__(self, x, y, bits, capture=False, cost=0, heuristic=0, parent=None):
		"""
		Constructor for search state
		:param x: x position
		:type x: 
		:param y: y position
		:type y: 
		:param bits: tuple bit vector indicate existence of dots
		:type bits:
		:param capture: see comments below
		:type capture: boolean
		:param cost: path cost
		:type cost:
		:param heuristic: heuristic value of the state
		:type heuristic:
		:param parent: parent state
		:type parent:
		"""
		self.x = x
		self.y = y
		self.bits = bits
		self.cost = cost
		# add path cost to heuristic if using A*
		self.heuristic = heuristic
		self.parent = parent
		# whether this state captured a dot
		self.capture = capture

	def __eq__(self, other):
		return isinstance(other, State) and self.x == other.x and self.y == other.y and self.bits == other.bits

	def __ne__(self, other):
		return not self.__eq__(other)

	def __lt__(self, other):
		return self.heuristic < other.heuristic

	def __hash__(self):
		return hash((self.x, self.y, self.bits))

	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + str(self.bits) + ')'
