#! /usr/bin/env python

import numpy as np

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle
from matplotlib.collections import CircleCollection


class vizualize():
	def __init__(self, numBots, initPose, figSize):
		self.numBots = numBots
		self.initPose = initPose

		self.grid = plt.figure()
		self.ax = self.grid.add_subplot(111)
		self.ax = plt.axes(xlim=(0, figSize[0]), ylim=(figSize[1], 0))
		plt.axis('scaled')

		self.path = [self.ax.plot([], [], lw = 1, color = 
			list(np.random.choice(range(256), size=3)), linestyle = '--',
			zorder=1) for i in range(self.numBots)]

		self.pointer = [Circle((self.initPose[i][0], self.initPose[i][1]), 
			radius=5, color='r', zorder=3) for i in range(self.numBots)]

		print('test')

if __name__ == '__main__':
	test = vizualize(2, [[0,0], [2,2]], [100, 100])