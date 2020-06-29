#! /usr/bin/env python

#------------------------------------------------------------------------------#
#   This code slices a bitmap file into voronoi components based 			   #
#	on given input seed points.        						 				   #
#                                                                              #
#   Usage:              python ROISlicer.py 						           #
#                                                                              #
#------------------------------------------------------------------------------#
#   Author: Kedar Karpe (https://github.com/karpenet)                          #
#   Copyright Beeclust - Multi Robot Systems Lab, 2020                         #
#------------------------------------------------------------------------------#

import numpy as np
import cv2
import math
import os

class imageSlice():

	def __init__(self, image, path):		
		self.img = image
		self.yMax, self.xMax = self.img.shape
		self.path = path


	def getVoronoi(self, centroids):
		sliceNum = np.shape(centroids)[0]
		roi = 255 * np.ones(self.img.shape, dtype = self.img.dtype)
		self.slice = 255 * np.ones(self.img.shape, dtype = self.img.dtype)
		self.slice = np.array([255 * np.ones(self.img.shape, dtype = self.img.dtype) for i in range(sliceNum)])

		for x, y in [(x, y) for x in range(self.xMax) for y in range(self.yMax)]:
			dist = [(math.sqrt((x - i[0])**2 + (y - i[1])**2), i)[0] for i in centroids]
			indexMin = dist.index(min(dist))
			roi[y][x] = indexMin*10
			self.slice[indexMin][y][x] = self.img[y][x]

		roi = cv2.applyColorMap(roi, cv2.COLORMAP_HSV)
		cv2.imshow('nice' ,roi)
		cv2.imshow('orig', self.img)
		cv2.waitKey(0)

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
	path = './BMP/test4.bmp'
	img  = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

	test = imageSlice(image = img, path = path)
	test.getVoronoi([(319.03,348.03), (212.21,116.42), (153.56,225.40), (299.30,187.57), (169.99,352.92)])
	test.saveBMP()
	