#! usr/bin/env python

import cv2
from ckMeans import ckMeans
from ROISlicer import imageSlice

imagePath = './BMP/test4.bmp'
numRobots = 5
iterations = 10
img  = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

ckm = ckMeans(img, numRobots, iterations)
vor = imageSlice(img, imagePath)

means = ckm.ckmMain()



