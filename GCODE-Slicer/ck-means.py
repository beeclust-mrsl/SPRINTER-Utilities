#! /usr/bin/env python

import numpy as np
import networkx as nx
import cv2
import time

import ROISlicer

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

		return data, numPoints

	def constrained_kmeans(self, data, demand, maxiter=None, fixedprec=1e9):
		data = np.array(data)
		
		min_ = np.min(data, axis = 0)
		max_ = np.max(data, axis = 0)

		C = min_ + np.random.random((len(demand), data.shape[1])) * (max_ - min_)
		M = np.array([-1] * len(data), dtype=np.int)
		
		itercnt = 0
		while True:
			itercnt += 1
			print('in loop')
			# memberships
			g = nx.DiGraph()
			g.add_nodes_from(range(0, data.shape[0]), demand=-1) # points
			for i in range(0, len(C)):
				g.add_node(len(data) + i, demand=demand[i])
			
			# Calculating cost...
			cost = np.array([np.linalg.norm(np.tile(data.T, len(C)).T - 
				np.tile(C, len(data)).reshape(len(C) * len(data), C.shape[1]), 
				axis=1)])

			print('cost')

			# Preparing data_to_C_edges...
			data_to_C_edges = np.concatenate((np.tile([range(0, data.shape[0])], 
				len(C)).T, np.tile(np.array([range(data.shape[0], data.shape[0] + 
					C.shape[0])]).T, len(data)).reshape(len(C) * 
				len(data), 1), cost.T * fixedprec), axis=1).astype(np.uint64)
	
			# Adding to graph
			g.add_weighted_edges_from(data_to_C_edges)
			
	
			a = len(data) + len(C)
			g.add_node(a, demand=len(data)-np.sum(demand))
			C_to_a_edges = np.concatenate((np.array([range(len(data), len(data) + 
				len(C))]).T, np.tile([[a]], len(C)).T), axis=1)
			g.add_edges_from(C_to_a_edges)
			
			print('before min flow')
			# Calculating min cost flow...
			f = nx.min_cost_flow(g, weight=0)
			print('after min flow')
			# assign
			M_new = np.ones(len(data), dtype=np.int) * -1
			for i in range(len(data)):
				p = sorted(f[i].items(), key=lambda x: x[1])[-1][0]
				M_new[i] = p - len(data)
			
			print('Iteration: ', itercnt)

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


if __name__ == '__main__':
	test = cKMeans('./BMP/test4.bmp')
	# roi = ROISlicer.imageSlice('./BMP/test4.bmp')

	data, numPoints = test.kMeans()
	print(np.shape(data))
	numBots = 5
	print(numPoints)

	demand = (numPoints - (numPoints%numBots))/numBots
	demand = [demand for i in range(numBots)]

	t = time.time()
	(C, M, f) = test.constrained_kmeans(data, demand)
	print('Elapsed:', (time.time() - t) * 1000, 'ms')
	print('C:', C)

	# roi.getVoronoi(C)
	# roi.saveBMP()

