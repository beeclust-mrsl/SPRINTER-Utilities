#! /usr/bin/env python

import gcodeParser
import vizualizer
import threading

class simulate():

	def __init__(self, path, timeStep):

		self.gcode = gcodeParser.parse()
		self.gcode.openFile(path)
		self.plot  = vizualizer.vizualize(xSize = 200, ySize = 200, xInit = 0, yInit =0)
		self.timeStep = timeStep
		self.steps = self.gcode.getLines()
		self.gcode.openFile(path)


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

	simulator1 = simulate(path = 'sample.gcode' , timeStep = 1)
	simulator2 = simulate(path = 'test.gcode' , timeStep = 1)

	sprinterOne = threading.Thread(target = simulator1.main)
	sprinterTwo = threading.Thread(target = simulator2.main)

	sprinterOne.start()
	sprinterTwo.start()

	sprinterOne.join()	
	sprinterTwo.join()

	print("Printing Over!")
