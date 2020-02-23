#! /usr/bin/env python

import numpy as np
import cv2
import random

class imageSlice():

	def __init__(self, path):		
		self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
		self.rows, self.cols = self.img.shape

		imageBound = (0, 0, 500, 500)
		self.subdiv = cv2.Subdiv2D(imageBound)
		self.ifacet = np.empty((0,2))

		self.getVoronoi([(100,250), (300,250), (250,100), (250,300)])

		# x = self.clipVoronoi(np.array([[200,200], [600,600]]))
		# print(x)


	def getVoronoi(self, centroids):
		img = np.zeros(self.img.shape, dtype = self.img.dtype)
		#cv2.imshow('bullshit', img)
		for c in centroids:
			self.subdiv.insert(c)

		(facets, centers) = self.subdiv.getVoronoiFacetList([])

		for i in range(0,len(facets)) :
			ifacet_arr = []
			for f in facets[i] :
				ifacet_arr.append(f)

			# ifacet_arr = self.clipVoronoi(np.array(ifacet_arr))
			# print(ifacet_arr)

			ifacet = np.array(ifacet_arr, np.int)
			print(ifacet)
			ifacet = self.clipVoronoi(ifacet)
			# print(ifacet)
			# print('yolo')
			color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

			cv2.fillConvexPoly(img, ifacet, color);
			ifacets = np.array([ifacet])

			if i == 2:
				# print(ifacets)
				cv2.polylines(img, ifacets, True, (0, 0, 0), 1)

				for x in range(ifacets.shape[1]):
					#print(ifacets[0][x])
					cv2.circle(img,(ifacets[0][x][0], ifacets[0][x][1]), 3, (0, 0, 0), -1)

			#cv2.circle(img, (centers[i][0], centers[i][1]), 3, (0, 0, 0), -1)

		cv2.imshow('bullshit', img)
		cv2.waitKey(0)
		
	def getLine(self, u, v):
		# m = 1
		# # print(u,v)
		# if np.array_equal((u % v), np.array([0, 0])):
		# 	print(u, v)
		m = (u[1] - v[1])/(u[0] - v[0])
		if (u[0] - v[0])==0:
			print(u,v)
		c = u[1] - (m * u[0])

		return m, c


	def clipVoronoi(self, vertices):
		length = np.shape(vertices)[0]

		for i in range (0, length):
			x, y = vertices[i][0], vertices[i][1]

			if i == (length - 1):
				m, c = self.getLine(vertices[i],vertices[0])
			else:
				m, c = self.getLine(vertices[i],vertices[i+1])

			if x>self.rows:
				x = self.rows
				y = m*x + c

			if y>self.cols:
				y = self.cols
				x = (y - c)/m	

			if x<0:
				x = 0
				y = m*x + c
			if y<0:
				y = 0
				x = (y - c)/m

			vertices[i][0], vertices[i][1] = x, y

		return vertices
				







if __name__ == '__main__':
	test = imageSlice('./BMP/test4.bmp')