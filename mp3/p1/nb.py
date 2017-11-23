
import numpy as np


class NB:

	def __init__(self):
		# P(class) placeholders
		self.pys = np.zeros(10)
		# P(f_i = 1 | class) placeholders
		self.pfs = np.zeros((10, 28*28))
		# P(f_i = 0 | class)
		self.pfzs = np.zeros((10, 28*28))
		# smoothing constant
		self.k = 0.1

	def train(self, trainX, trainY):
		"""
		Train NB with given data
		:param trainX: 2d np array
		:type trainX: 
		:param trainY: 1d np array
		:type trainY: 
		:return: 
		:rtype: 
		"""
		# reinitialize all vals
		self.__init__()
		# total number of examples
		n, m = trainX.shape
		# calculate frequencies of class labels and features
		for i in range(n):
			y = trainY[i]
			self.pys[y] += 1
			self.pfs[y] += trainX[i]
			self.pfzs[y] += (1 - trainX[i])
		# calculate P(f | class) with laplace smoothing with k = 0.1
		for i in range(10):
			self.pfs[i] = (self.pfs[i] + self.k) / (self.pys[i] + 2 * self.k)
			self.pfzs[i] = (self.pfzs[i] + self.k) / (self.pys[i] + 2 * self.k)
		self.pys /= n

	def test(self, testX):
		"""
		Classifiy the given test data
		:param testX: 
		:type testX: 
		:return: 
		:rtype: 
		"""
		# take log of all values of ps
		pfs = np.log(self.pfs)
		pfzs = np.log(self.pfzs)
		pys = np.log(self.pys)
		# total number of test data
		n, m = testX.shape
		predY = np.zeros(n)
		maps = np.zeros((n, 10))
		for i in range(n):
			x = testX[i]
			for j in range(10):
				maps[i][j] += pys[j]
				for k in range(m):
					if x[k] == 0:
						maps[i][j] += pfzs[j][k]
					elif x[k] == 1:
						maps[i][j] += pfs[j][k]
			predY[i] = np.argmax(maps[i])
		return predY

	def acc(self, predY, testY):
		"""
		Calculate accuracy for all different classes
		:param predY: 
		:type predY: 
		:param testY: 
		:type testY: 
		:return: 
		:rtype: 
		"""
		total = np.zeros(10)
		correct = np.zeros(10)
		for i in range(predY.shape[0]):
			total[int(testY[i])] += 1
			if predY[i] == testY[i]:
				correct[int(predY[i])] += 1
		print(np.divide(correct, total))
