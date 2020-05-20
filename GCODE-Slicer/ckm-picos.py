#! /usr/bin/env python
import cv2
import numpy as np
from matplotlib import pyplot as plt
import picos
import itertools

class ckMeans():
	def __init__(self, path, clusters):
		self.img  = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
		self.yMax, self.xMax = np.shape(self.img)

		self.clusters = clusters
		self.pixels = 0


	def getData(self):
		data = []

		for x, y in [(x, y) for x in range(self.xMax) for y in range(self.yMax)]:
			if self.img[y][x] == 0:
				data.append([x,y])

		self.pixels = len(data)
		return np.array(data)


	def euclDist(self, a, b, axis=1):
		return np.linalg.norm(a - b, axis=axis)


	def kmPP(self, data):
		centres = []
		centres.append(data[np.random.randint(0, np.shape(data)[0])].tolist())

		while len(centres) < self.clusters:
			d2 = np.array([min([np.square(self.euclDist(i,c, None)) for c in centres]) for i in data])
			prob = d2/d2.sum()
			cumlProb = prob.cumsum()
			r = np.random.random()
			ind = np.where(cumlProb >= r)[0][0]
			centres.append(data[ind].tolist())
		return np.array(centres)


	def plot(self, data, centres):
		plt.scatter(data[:, 0], data[:, 1])
		plt.scatter(centres[:,0], centres[:,1])
		plt.show()


	def picos(self, data, mu):
		P = picos.Problem()
		print(self.pixels, self.clusters)
		self.W = picos.BinaryVariable("W", (self.pixels, self.clusters))


		e = picos.sum([self.W[i,j]*(1/2) for i,j in itertools.product(range(self.pixels), range(self.clusters))])
		
		print(e)
		self.mu = picos.BinaryVariable("mu", self.clusters)
		P.set_objective("min", (self.W-5)*2-self.mu[i])
		print(P)


if __name__ == '__main__':
	test = ckMeans('./BMP/test4.bmp', 5)
	data = test.getData()
	centres=test.kmPP(data)
	test.picos(data, centres)
	# test.plot(centres, data)
	print(centres)
		