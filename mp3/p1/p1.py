
from itertools import islice

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
						print(str(i) + ',' + str(j))
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
	testX = read_features(path+testfile[0])
	testY = read_labels(path+testfile[1])
	trainX = read_features(path+trainfile[0])
	trainY = read_features(path+trainfile[1])
