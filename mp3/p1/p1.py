
from mp3.p1.nb import NB
from itertools import islice
from sklearn.metrics import confusion_matrix

import numpy as np


def read_features(filename):
	digits_features = list()
	with open(filename, 'r') as f:
		while True:
			feature = np.zeros(28*28)
			lines = list(islice(f, 28))
			if not lines:
				break
			for i, line in enumerate(lines):
				for j, c in enumerate(list(line)[:-1]):
					if c != ' ':
						feature[i*28+j] = 1
			digits_features.append(feature)
	return np.array(digits_features)


def read_labels(filename):
	labels = list()
	with open(filename, 'r') as f:
		for line in f.readlines():
			labels.append(int(line[0]))
	return np.array(labels)


if __name__ == "__main__":
	path = "digitdata/"
	testfile = ["testimages", "testlabels"]
	trainfile = ["trainingimages", "traininglabels"]
	trainX = read_features(path+trainfile[0])
	trainY = read_labels(path+trainfile[1])
	nb = NB()
	nb.train(trainX, trainY)
	testX = read_features(path+testfile[0])
	testY = read_labels(path+testfile[1])
	predY = nb.test(testX)
	nb.acc(predY, testY)
	print(confusion_matrix(testY, predY, labels=np.arange(0, 10)))
