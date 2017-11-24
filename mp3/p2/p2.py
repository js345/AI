
from mp3.p2.nb import NB

from itertools import islice, product

import numpy as np
import matplotlib.pyplot as plt


def load_data(filename):
	# modify data files to allow 3 blank lines at beginning
	features = list()
	with open(filename, 'r') as f:
		while True:
			feature = np.zeros(25 * 10)
			lines = list(islice(f, 3, 28))
			if not lines:
				break
			for i, line in enumerate(lines):
				for j, c in enumerate(list(line)[:-1]):
					if c == '%':
						feature[i * 10 + j] = 1
			# skip 3 blank lines
			features.append(feature)
	return np.array(features)


def cmatrix(ytest, ypred):
	matrix = np.zeros((2, 2))
	for i in range(ypred.shape[0]):
		matrix[int(ytest[i]), int(ypred[i])] += 1
	return matrix


def plot_confusion_matrix(cm, classes,
						  normalize=False,
						  title='Confusion matrix',
						  cmap=plt.cm.Blues):
	"""
	This function prints and plots the confusion matrix.
	Normalization can be applied by setting `normalize=True`.
	"""
	if normalize:
		cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	print(cm)

	plt.imshow(cm, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalize else 'd'
	thresh = cm.max() / 2.
	for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
		plt.text(j, i, format(cm[i, j], fmt),
				 horizontalalignment="center",
				 color="white" if cm[i, j] > thresh else "black")

	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')


if __name__ == "__main__":
	path = "yesno/"
	yes_train = load_data(path+"yes_train.txt")
	yes_test = load_data(path+"yes_test.txt")
	no_train = load_data(path+"no_train.txt")
	no_test = load_data(path+"no_test.txt")
	xTrain = np.append(yes_train, no_train, axis=0)
	yTrain = np.append(np.ones(yes_train.shape[0]), np.zeros(no_train.shape[0]))
	xTest = np.append(yes_test, no_test, axis=0)
	yTest = np.append(np.ones(yes_test.shape[0]), np.zeros(no_test.shape[0]))
	nb = NB()
	nb.train(xTrain, yTrain)
	ypred = nb.test(xTest)
	print(cmatrix(yTest, ypred))
	# Plot normalized confusion matrix
	plt.figure()
	plot_confusion_matrix(cmatrix(yTest, ypred), classes=["No", "Yes"], normalize=True, title='Normalized confusion matrix')

	plt.show()
