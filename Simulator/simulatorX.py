#! /usr/bin/env python

import vizualizerX
import gcodeParserX

class simulate():

	def __init__(self, bots, path, initPose, timeStep):

		self.numBots = bots
		self.timeStep = timeStep

		parser = gcodeParserX.parse()

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


	def getPoses(self):
		self.metaDict = [parser.getPoseDict() for i in range(self.numBots)]


	def callback(self, iteration):
		for i in self.numBots:
			x = self.metaDict[i]['xPath'][iteration]
			y = self.metaDict[i]['yPath'][iteration]
			feed = self.metaDict[i]['feed'][iteration]

			setData()

		return



	def process(self, bot):
		while True:
			line  = self.gcode[bot].parseLine()
			if line == None:
				return lines, path, feed, head
				break

			print(bot)
			typeCmd = self.gcode[bot].process(line)

			if typeCmd == 'Move':
				x, y = self.gcode[bot].getCoordinate()
				self.plot[bot].appendPath(x, y)
				self.vizualizer.pause()

			elif typeCmd == 'Feed':
				x, y = self.gcode[bot].getCoordinate()
				self.plot[bot].appendFeed(x, y)
				self.vizualizer.pause()

			else:
				pass