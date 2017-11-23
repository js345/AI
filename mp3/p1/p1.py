
from mp3.p1.nb import NB
from itertools import islice

import numpy as np


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


def cmatrix(ypred, ytest):
	matrix = np.zeros((10, 10))
	for i in range(ypred.shape[0]):
		matrix[int(ypred[i]), int(ytest[i])] += 1
	return matrix


def show_prototypical(testY, maps, test_digits):
	print("============Showing prototypical digits==============")
	for i in range(10):
		ids = np.where(testY == i)[0]
		ps = maps[ids, i]
		ds = [test_digits[x] for x in ids]
		print("====Showing for digit " + str(i) + "======")
		print("Max posterior")
		print(ds[np.argmax(ps)])
		print("Min posterior")
		print(ds[np.argmin(ps)])


if __name__ == "__main__":
	path = "digitdata/"
	testfile = ["testimages", "testlabels"]
	trainfile = ["trainingimages", "traininglabels"]
	trainX, train_digits = read_features(path + trainfile[0])
	trainY = read_labels(path + trainfile[1])
	nb = NB()
	nb.train(trainX, trainY)
	testX, test_digits = read_features(path + testfile[0])
	testY = read_labels(path + testfile[1])
	predY, maps = nb.test(testX)
	# nb.acc(predY, testY)
	# print("====Showing confusion matrix")
	# print(cmatrix(testY, predY))
	# show_prototypical(testY, maps, test_digits)
