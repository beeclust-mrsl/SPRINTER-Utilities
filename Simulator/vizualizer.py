#! /usr/bin/env python

import numpy as np

from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle
from matplotlib.collections import CircleCollection


class vizualize():

	def __init__(self, xSize = 100, ySize = 100, xInit = 0, yInit = 0):
		self.indexX = 0
		self.indexY = 10

		self.xPath = np.array([xInit])
		self.yPath = np.array([yInit])

		self.xFeed = np.array([None])
		self.yFeed = np.array([None])

		self.mask = np.array([0])
		self.grid = plt.figure()

		self.ax = self.grid.add_subplot(111)
		self.ax = plt.axes(xlim=(0, xSize), ylim=(ySize, 0))
		plt.axis('scaled')

		self.path, = self.ax.plot([], [], lw = 1, color = 'b', linestyle = '--',zorder=1)
		self.feed, = self.ax.plot([], [], lw = 0, color = 'k', marker='o')
	
		self.circle = Circle((0, 0), radius=5, color='r',zorder=3)
		self.ax.add_patch(self.circle)

		# Writer = animation.writers['ffmpeg']
		# self.writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)


	def appendPath(self, x, y):
		self.xPath = np.append(self.xPath, x)
		self.yPath = np.append(self.yPath, y)
		self.path.set_data(self.xPath, self.yPath)

		self.circle.center = (x, y)


	def appendFeed(self, x, y):
		self.ax.add_patch(Circle((x,y),radius=1, color='k', zorder=2))

		
	def getArtists(self):
		return self.path, self.feed,


	def animate(self, callback, steps, freq):
		anim = animation.FuncAnimation(self.grid, func=callback, frames=steps, interval=freq, repeat=False, blit=False)
		#anim.save('lines.mp4', writer=self.writer)
		plt.show()