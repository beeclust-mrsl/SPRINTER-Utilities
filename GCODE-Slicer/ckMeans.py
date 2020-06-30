import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from mip import Model, xsum, minimize, BINARY
from itertools import product
from scipy.spatial import Voronoi, voronoi_plot_2d


class ckMeans():
	def __init__(self, image, clusters, iterations):
		self.img  = image
		self.yMax, self.xMax = np.shape(self.img)
		self.clusters = clusters
		self.iterations = iterations
		self.pixels = 0
		self.mu = []
		self.weight = []
		self.cost = []
		self.clusterLen =[]
		self.model = Model()

		fig = plt.figure()
		self.ax1 = fig.add_subplot(2, 2, 1)
		self.ax2 = fig.add_subplot(2, 2, 2)
		self.ax3 = fig.add_subplot(2, 2, 3)
		self.ax4 = fig.add_subplot(2, 2, 4)

		# self.ax1.set_xlim([0, self.xMax])
		# self.ax1.set_ylim([0, self.yMax])
		self.ax1.set_title('(a) Geodesic Cells')
		self.ax2.set_title('(b) Optimization Cost')
		self.ax2.set_xlabel('Iteration')
		self.ax2.set_ylabel('Objective Cost')
		self.ax4.set_xlim([0, self.xMax])
		self.ax4.set_ylim([0, self.yMax])
		self.ax4.set_title('(d) K-means Centroids')
		# plt.axis([0, 500, 0, 500])


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
		self.mu = np.array(centres)
		return(centres)


	def pymip(self, data):
		# Binary weight matrix
		self.w = [[self.model.add_var(var_type=BINARY) for j in range(self.clusters)] for i in range(self.pixels)]
		print(len(self.w),len(self.w[0]))
		# Objective Funtion
		self.model.objective = minimize(xsum(self.w[i][j]*(self.euclDist(data[i], self.mu[j], None)**2)/2  for j in range(self.clusters) for i in range(self.pixels)))
		#Constraints
		for i in range(self.pixels):
			self.model += xsum(self.w[i][j] for j in range(self.clusters)) == 1
		for j in range(self.clusters):
			self.model += xsum(self.w[i][j] for i in range(self.pixels)) >= math.floor(self.pixels/self.clusters)
		# for (i, j) in product(self.pixels, self.clusters):
		# 	model += w[i][j] >= 0


	def optimizer(self):
		status = self.model.optimize(max_seconds=1000)
		print(status)
		weight = np.zeros((self.pixels, self.clusters))
		for i in range(self.pixels):
			for j in range(self.clusters):
				weight[i][j] = self.w[i][j].x
		self.weight = weight


	def updateMean(self, data):
		mean = []
		for j in range(self.clusters):
			weighted = 0
			num = 0
			for i in range(self.pixels):
				weighted += self.weight[i][j]*data[i]
				num += self.weight[i][j]
			if num>0:
				mean.append(weighted/num)
			else:
				mean.append(self.mu[j])
			self.clusterLen[j].append(num)
		print(self.clusterLen)
		print('Outside loop')
		print(mean)
		print(self.mu)
		self.model.clear()
		return np.array(mean)


	def ckmMain(self):
		data = self.getData()
		self.kmPP(data)
		self.initClusterSize()
		self.plotSize()
		
		for i in range(self.iterations):
			self.plotMean(i)
			self.pymip(data)
			self.optimizer()
			self.plotCost()
			mean = self.updateMean(data)
			self.plotSize()
			print('if')
			print(mean == self.mu)
			if (mean == self.mu).all():
				print('break')
				break
			else:
				self.mu = mean
				print(self.mu)
		print('Voronoi')
		self.plotVor()
		print('Means:', self.mu)
		plt.show()
		return self.mu

	def initClusterSize(self):
		sliceNum = np.shape(self.mu)[0]
		clusterLen = [[0] for i in range(sliceNum)]
		for x, y in [(x, y) for x in range(self.xMax) for y in range(self.yMax)]:
			if self.img[y][x] == 0:
				dist = [(math.sqrt((x - i[0])**2 + (y - i[1])**2), i)[0] for i in self.mu]
				indexMin = dist.index(min(dist))
				clusterLen[indexMin][0] += 1
		self.clusterLen = clusterLen
		print(self.clusterLen)

	def plotSize(self):
		axis = [i for i in range(len(self.clusterLen[0]))]
		self.ax3.clear()
		self.ax3.set_title('(c) Pixels Per Cell')
		self.ax3.set_xlabel('Iteration')
		self.ax3.set_ylabel('No. of Pixels')
		for i in range(len(self.clusterLen)):
			self.ax3.plot(axis, self.clusterLen[i], '--o', label = 'Cluster %d' % (i+1))
			self.ax3.legend(frameon=False, fontsize = 'xx-small')
		plt.pause(0.05)


	def plotMean(self, i):
		x, y = zip(*self.mu)
		self.ax4.plot(x, y, 'o', label = 'Iter %d' % i)
		self.ax4.legend(frameon = False, fontsize = 'xx-small')
		plt.pause(0.05)


	def plotCost(self):
		self.cost.append(self.model.objective_value)
		self.ax2.plot([i+1 for i in range(len(self.cost))], self.cost, '-o')
		plt.pause(0.05)

	def plotVor(self):
		vor = Voronoi(self.mu)
		self.ax1.imshow(self.img, cmap = 'gray')
		voronoi_plot_2d(vor, ax = self.ax1, show_vertices = False, line_colors = 'orange')
		self.ax1.set_xlim(0, self.xMax)
		self.ax1.set_ylim(self.yMax,0)
		



if __name__ == '__main__':
	clusters = 5
	img  = cv2.imread('./BMP/rnd2.bmp', cv2.IMREAD_GRAYSCALE)
	iterations = 5
	test = ckMeans(img, clusters, iterations)
	test.ckmMain()
