#! /usr/bin/env python

import numpy as np
import cv2
import math
import os

class imageSlice():

	def __init__(self, path):
		self.path = path		
		self.img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
		self.yMax, self.xMax = self.img.shape


	def getVoronoiTest(self, centroids):
		sliceNum = np.shape(centroids)[0]

		self.slice = 255 * np.ones(self.img.shape, dtype = self.img.dtype)
		self.slice = np.array([255 * np.ones(self.img.shape, dtype = self.img.dtype) for i in range(sliceNum)])

		for x, y in [(x, y) for x in range(self.xMax) for y in range(self.yMax)]:
			dist = [(math.sqrt((x - i[0])**2 + (y - i[1])**2), i)[0] for i in centroids]
			indexMin = dist.index(min(dist))

			self.slice[indexMin][y][x] = self.img[y][x]

		for i in range(sliceNum):
			cv2.imshow('Slice'+str(i), self.slice[i])
		cv2.waitKey(0)


	def saveBMP(self):
		num = np.shape(self.slice)[0]
		pathList = [] 

		for i in range(num):
			writepath = './Slices/' + os.path.splitext(os.path.basename(self.path))[0] +'-slice-' + str(i) + '.bmp'
			pathList.append(writepath)
			# print(writepath)
			cv2.imwrite(writepath, self.slice[i])

		return pathList


if __name__ == '__main__':
	test = imageSlice('./BMP/test4.bmp')
	test.getVoronoiTest([(100,250), (300,250), (250,100), (250,300)])
	test.saveBMP()