#! /usr/bin/env python

import gcodeParser
import vizualizer
import threading

class simulate():

	def __init__(self, timeStep):

		self.gcode = gcodeParser.parse()
		self.gcode.openFile('sample.gcode')
		self.plot  = vizualizer.vizualize(xSize = 200, ySize = 200, xInit = 0, yInit =0)
		self.timeStep = timeStep
		self.steps = self.gcode.getLines()
		self.gcode.openFile('sample.gcode')


	def update(self, i):
 
		line  = self.gcode.parseLine()
		print(line)
		typeCmd = self.gcode.process(line)

		if typeCmd == 'Move':
			x, y = self.gcode.getCoordinate()
			self.plot.appendPath(x, y)

		elif typeCmd == 'Feed':
			x, y = self.gcode.getCoordinate()
			self.plot.appendFeed(x, y)

		else:
			pass

		return self.plot.getArtists()			


	def main(self):
		self.plot.animate(callback = self.update, steps = self.steps, freq = self.timeStep)
	
if __name__ == '__main__':

	simulator = simulate(timeStep = 1)
	simulator.main()

	# sprinterOne = threading.Thread(target = simulator.main)
	# sprinterTwo = threading.Thread(target = simulator.main)

	# sprinterOne.start()
	# sprinterTwo.start()

	# sprinterOne.join()	
	# sprinterTwo.join()

	# print("Printing Over!")
