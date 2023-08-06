import numpy as np

def standartize(X):
	"""Get numpy array and return standartized array"""
	return (X - np.mean(X)) / np.std(X)

def normalization(X):
	"""Get numpy array and return normalized array"""
	return (X - np.amin(X)) / (np.amax(X) - np.amin(X))
