#! /usr/bin/env python

import gcodeParserTest
import threading

import vizualizerTest

class simulate():

	def __init__(self, bots, path, initPose, timeStep):

		self.numBots = bots
		self.timeStep = timeStep
		self.steps = [0 for _ in range(self.numBots)]

		self.gcode = [gcodeParserTest.parse() for i in range(self.numBots)]
		for i in range(self.numBots):
			print(path[i])
			self.gcode[i].openFile(path[i])
			self.steps[i] = self.gcode[i].getLines()
			print(self.steps)

		for i in range(self.numBots):
			self.gcode[i].openFile(path[i])

		self.vizualizer = vizualizerTest.figure(xSize = 200, ySize = 200)
		figure = self.vizualizer.getAxes()
		self.plot  = [vizualizerTest.vizualize(figure, initPose[i][0], initPose[i][1]) for i in range(self.numBots)]




	def update(self, i):
 
		line  = self.gcode[i].parseLine()
		print(line)
		typeCmd = self.gcode[i].process(line)

		if typeCmd == 'Move':
			x, y = self.gcode[i].getCoordinate()
			self.plot[i].appendPath(x, y)
			self.vizualizer.show()

		elif typeCmd == 'Feed':
			x, y = self.gcode[i].getCoordinate()
			self.plot[i].appendFeed(x, y)
			self.vizualizer.show()

		else:
			pass

		# return self.plot[i].getArtists()	


	def process(self, bot):
		while True:
			line  = self.gcode[bot].parseLine()
			if line == None:
				break

			print(line)
			typeCmd = self.gcode[bot].process(line)

			if typeCmd == 'Move':
				x, y = self.gcode[bot].getCoordinate()
				self.plot[bot].appendPath(x, y)
				if bot == 0:
					self.vizualizer.pause()

			elif typeCmd == 'Feed':
				x, y = self.gcode[bot].getCoordinate()
				self.plot[bot].appendFeed(x, y)
				if bot == 0:
					self.vizualizer.pause()

			else:
				pass

	def show(self):
		self.vizualizer.show()


	def main(self):
		self.plot.animate(callback = self.update, steps = self.steps, freq = self.timeStep)

	def threads(self):
		simulation = [threading.Thread(target = self.process, args = (i, )) for i in range(self.numBots)]
		
		for i in range(self.numBots):
			simulation[i].start()

		for i in range(self.numBots):
			simulation[i].join()
	

if __name__ == '__main__':
	filename = '../GCODE-Slicer/GCODE/test4-slice'
	bots = 1

	paths = [filename + '-' + str(i) + '.gcode' for i in range(bots)]
	initPose = [(0,0) for i in range(bots)]

	simulator = simulate(bots = bots, path = paths, initPose = initPose, timeStep = 1)
	simulator.process(0)
	simulator.show()
	# simulator.threads()

	print("Printing Over!")
