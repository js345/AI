
from mp3.p1.nb import NB
from itertools import islice

import numpy as np
import matplotlib.pyplot as plt


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


def cmatrix(ytest, ypred):
	matrix = np.zeros((10, 10))
	for i in range(ypred.shape[0]):
		matrix[int(ytest[i]), int(ypred[i])] += 1
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


def show_odds_ratio(pfs, cls1, cls2):
	odd1, odd2 = np.log(pfs[cls1]), np.log(pfs[cls2])
	ratio = odd1 - odd2
	odd1, odd2, ratio = np.reshape(odd1, (28, 28)), np.reshape(odd2, (28, 28)), np.reshape(ratio, (28, 28))
	fig = plt.figure(1)
	fig.suptitle("Odds ratio plot with " + str(cls1) + " and " + str(cls2))
	cmap = 'jet'
	plt.subplot(131)
	plt.imshow(odd1, cmap=cmap)
	plt.axis('off')
	plt.colorbar()
	plt.subplot(132)
	plt.imshow(odd2, cmap=cmap)
	plt.axis('off')
	plt.colorbar()
	plt.subplot(133)
	plt.imshow(ratio, cmap=cmap)
	plt.axis('off')
	plt.colorbar()
	plt.show()


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

	show_odds_ratio(nb.pfs, 5, 3)
	show_odds_ratio(nb.pfs, 8, 3)
	show_odds_ratio(nb.pfs, 4, 9)
	show_odds_ratio(nb.pfs, 7, 9)
