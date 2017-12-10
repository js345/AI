
from itertools import islice, product
from sklearn.utils import shuffle

import numpy as np
import matplotlib.pyplot as plt


def f1(alpha, epoch):
	"""
	Decay function #1
	:param alpha: 
	:type alpha: 
	:param epoch: 
	:type epoch: 
	:return: 
	:rtype: 
	"""
	return alpha * 1000 / (1000 + epoch)


class Perceptron:

	def __init__(self, rand=True):
		# 10 weight vectors for 10 digit classes
		self.ws = np.zeros((10, 28 * 28))
		# bias term
		self.bs = np.zeros(10)
		if rand:
			self.ws = np.random.rand(10, 28*28)
			self.bs = np.random.rand(10)

	def train(self, trainX, trainY, epochs=1, rand=True, shuff=False, bias=False, decay=f1, alpha=0.1):
		n, m = trainX.shape
		accs = np.zeros(epochs)
		self.__init__(rand)
		for epoch in range(epochs):
			alpha = decay(alpha, epoch)
			if shuff:
				trainX, trainY = shuffle(trainX, trainY)
			# iterating through all training examples
			for i in range(n):
				# find out the c
				cs = np.zeros(10)
				for j in range(10):
					cs[j] = np.dot(trainX[i], self.ws[j])
					if bias:
						cs[j] += self.bs[j]
				c = np.argmax(cs)
				# update weights
				for j in range(10):
					y = 1 if trainY[i] == j else 0
					yp = 1 if c == j else 0
					self.ws[j] += alpha * (y - yp) * trainX[i]
					if bias:
						self.bs[j] += alpha * (y - yp)
			# generating training accuracy per epoch
			accs[epoch] = self.acc(self.test(trainX, bias), trainY)
		return accs

	def test(self, testX, bias=False):
		n, m = testX.shape
		predY = np.zeros(n)
		for i in range(n):
			cs = np.zeros(10)
			for j in range(10):
				cs[j] = np.dot(testX[i], self.ws[j])
				if bias:
					cs[j] += self.bs[j]
			predY[i] = np.argmax(cs)
		return predY

	def acc(self, predY, testY):
		correct = 0.0
		for i in range(predY.shape[0]):
			if predY[i] == testY[i]:
				correct += 1
		return correct / predY.shape[0]


def read_features(filename):
	digits_features = list()
	digits = list()
	with open(filename, 'r') as f:
		while True:
			feature = np.zeros(28 * 28)
			lines = list(islice(f, 28))
			if not lines:
				break
			digits.append(''.join(lines))
			for i, line in enumerate(lines):
				for j, c in enumerate(list(line)[:-1]):
					if c != ' ':
						feature[i * 28 + j] = 1
			digits_features.append(feature)
	return np.array(digits_features), digits


def read_labels(filename):
	labels = list()
	with open(filename, 'r') as f:
		for line in f.readlines():
			labels.append(int(line[0]))
	return np.array(labels)


def plot_accuracy(accs):
	plt.plot(accs)
	plt.ylabel("Training Accuracy")
	plt.xlabel("Epochs")
	plt.show()


def cmatrix(ytest, ypred):
	matrix = np.zeros((10, 10))
	for i in range(ypred.shape[0]):
		matrix[int(ytest[i]), int(ypred[i])] += 1
	return matrix


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalize else 'd'
	thresh = cm.max() / 2.
	for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')

if __name__ == "__main__":
	path = "digitdata/"
	testfile = ["testimages", "testlabels"]
	trainfile = ["trainingimages", "traininglabels"]
	trainX, train_digits = read_features(path + trainfile[0])
	trainY = read_labels(path + trainfile[1])
	testX, test_digits = read_features(path + testfile[0])
	testY = read_labels(path + testfile[1])

	clf = Perceptron()
	bias = True
	accs = clf.train(trainX, trainY, epochs=50, rand=True, shuff=True, bias=bias, decay=f1, alpha=0.2)
	plot_accuracy(accs)
	predY = clf.test(testX, bias=bias)
	print(clf.acc(predY, testY))
	print("====Showing confusion matrix")
	cnf_matrix = cmatrix(testY, predY)
	print(cnf_matrix)
	plt.figure()
	plot_confusion_matrix(cnf_matrix, classes=np.arange(0, 10), normalize=True, title='Normalized confusion matrix')
	plt.show()
