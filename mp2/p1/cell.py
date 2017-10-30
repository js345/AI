

class Cell:

	def __init__(self, x, y, value):
		self.x = x
		self.y = y
		self.value = value
		self.source = False
		# placeholder for list of available colors
		self.available = list()

	def __str__(self):
		return '(' + str(self.x) + ',' + str(self.y) + ',' + str(self.value) + ')'
