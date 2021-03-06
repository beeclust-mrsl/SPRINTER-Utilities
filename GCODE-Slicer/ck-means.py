#! /usr/bin/env python

import numpy as np
import networkx as nx
import cv2
import time

import ROISlicer

from matplotlib import pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

class cKMeans():

	def __init__(self, path):
		self.img  = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
		self.yMax, self.xMax = np.shape(self.img)

	def kMeans(self):
		data = np.empty((0, 2), int)
		numPoints = 0

		for x, y in [(x, y) for x in range(self.xMax) for y in range(self.yMax)]:
			if self.img[y][x] == 0:
				data = np.append(data, np.array([[x,y]]), axis=0)
				numPoints += 1

		return data, numPoints, np.shape(self.img)

	def constrained_kmeans(self, data, demand, maxiter=None, fixedprec=1e9):
		data = np.array(data)
		
		min_ = np.min(data, axis = 0)
		max_ = np.max(data, axis = 0)
		
		C = min_ + np.random.random((len(demand), data.shape[1])) * (max_ - min_)
		M = np.array([-1] * len(data), dtype=np.int)
		
		itercnt = 0
		while True:
			itercnt += 1
			
			# memberships
			print('Evaluating memberships...')
			g = nx.DiGraph()
			g.add_nodes_from(range(0, data.shape[0]), demand=-1) # points
			for i in range(0, len(C)):
				g.add_node(len(data) + i, demand=demand[i])
			
			# Calculating cost...
			print('Calculating cost...')
			cost = np.array([np.linalg.norm(np.tile(data.T, len(C)).T - 
				np.tile(C, len(data)).reshape(len(C) * len(data), C.shape[1]), 
				axis=1)])
			
			# Preparing data_to_C_edges...
			print('Preparing data_to_C_edges...')
			data_to_C_edges = np.concatenate((np.tile([range(0, data.shape[0])], 
				len(C)).T, np.tile(np.array([range(data.shape[0], data.shape[0] + 
					C.shape[0])]).T, len(data)).reshape(len(C) * 
				len(data), 1), cost.T * fixedprec), axis=1).astype(np.uint64)

			# Adding to graph
			print('Adding to graph')
			g.add_weighted_edges_from(data_to_C_edges)
			

			a = len(data) + len(C)
			g.add_node(a, demand=len(data)-np.sum(demand))
			C_to_a_edges = np.concatenate((np.array([range(len(data), len(data) + 
				len(C))]).T, np.tile([[a]], len(C)).T), axis=1)
			g.add_edges_from(C_to_a_edges)
			
			print('Iteration: ', itercnt)
			# Calculating min cost flow...
			f = nx.min_cost_flow(g)
			
			# assign
			M_new = np.ones(len(data), dtype=np.int) * -1
			for i in range(len(data)):
				p = sorted(f[i].items(), key=lambda x: x[1])[-1][0]
				M_new[i] = p - len(data)
				
			# stop condition
			if np.all(M_new == M):
				# Stop
				return (C, M, f)
				
			M = M_new
				
			# compute new centers
			for i in range(len(C)):
				C[i, :] = np.mean(data[M==i, :], axis=0)
				
			if maxiter is not None and itercnt >= maxiter:
				# Max iterations reached
				return (C, M, f)

		def ckTest(self):
			temp = np.array([i for i in range(10)])
			temp = temp * constrained_kmeans([100,200])


if __name__ == '__main__':
	test = cKMeans('./BMP/test4.bmp')
	roi = ROISlicer.imageSlice('./BMP/test4.bmp')

	data, numPoints, matDim = test.kMeans()
	# data = np.random.random((100, 2))
	# numPoints = 100
	print(np.shape(data))
	numBots = 3
	print(numPoints)

	demand = (numPoints - (numPoints%numBots))/numBots
	demand = [demand for i in range(numBots)]

	t = time.time()
	(C, M, f) = test.constrained_kmeans(data, demand)
	print('Elapsed:', (time.time() - t) * 1000, 'ms')
	print('C:', C)

	unique, counts = np.unique(M, return_counts=True)
	a = dict(zip(unique, counts))
	print(a)


	vor = Voronoi(C)
	voronoi_plot_2d(vor)
	plt.scatter(C[:,0], C[:,1])
	plt.scatter(data[:, 0], data[:, 1])
	plt.xlim ((0, matDim[0]))
	plt.ylim ((0, matDim[1]))
	plt.show()


	# roi.getVoronoi(C)
	# roi.saveBMP()

