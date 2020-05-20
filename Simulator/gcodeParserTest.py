#! /usr/bin/env python

import re
import time
import vizualizerTest

def _clean_codestr(value):
	if value < 10:
		return "0%g" % value
	return "%g" % value

REGEX_FLOAT = re.compile(r'^\s*-?(\d+\.?\d*|\.\d+)')
REGEX_INT = re.compile(r'^\s*-?\d+')
REGEX_POSITIVEINT = re.compile(r'^\s*\d+')
REGEX_CODE = re.compile(r'^\s*\d+(\.\d)?')

CLEAN_NONE = lambda v: v
CLEAN_FLOAT = lambda v: "{0:g}".format(round(v, 3))
CLEAN_CODE = _clean_codestr
CLEAN_INT = lambda v: "%g" % v

class wordType():

	def __init__(self, cls, valueRegex, description, clean_value):
		self.cls = cls
		self.valueRegex = valueRegex
		self.description = description
		self.clean_value = clean_value

class parse():

	def __init__(self):

		self.x = None
		self.y = None

		self.codeDict = {

		    'G': wordType(
		        cls=float,
		        valueRegex=REGEX_CODE,
		        description="Address for preparatory commands",
		        clean_value=CLEAN_CODE,
		    ),
		
		    'M': wordType(
		        cls=float,
		        valueRegex=REGEX_CODE,
		        description="Miscellaneous function",
		        clean_value=REGEX_CODE,
		    ),
		
		    'X': wordType(
		        cls=float,
		        valueRegex=REGEX_FLOAT,
		        description="Absolute or incremental position of X axis",
		        clean_value=CLEAN_FLOAT,
		    ),
		
		    'Y': wordType(
		        cls=float,
		        valueRegex=REGEX_FLOAT,
		        description="Absolute or incremental position of Y axis",
		        clean_value=CLEAN_FLOAT,
		    ),
		
		    'P': wordType(
		        cls=float,
		        valueRegex=REGEX_FLOAT,
		        description="Serves as parameter address for various G and M codes",
		        clean_value=CLEAN_FLOAT,
		    ),
		
		    'S': wordType(
		        cls=float,
		        valueRegex=REGEX_POSITIVEINT,
		        description="Absolute or incremental position of A axis (rotational axis around X axis)",
		        clean_value=CLEAN_INT,
		    ),
		
		    'F': wordType(
		        cls=float,
		        valueRegex=REGEX_FLOAT,
		        description="Feedrate",
		        clean_value=CLEAN_FLOAT,
		    )
		
		}

	def getLines(self):
		num = 0
		for lines in self.file:
			num += 1

		return num


	def openFile(self, path):
		self.file = open(path, "rt")


	def readLine(self):
		gcLine = self.file.readline()
		gcLine = gcLine.rstrip('\n')
		gcLine = gcLine.replace(" ", "")

		return gcLine


	def getCoordinate(self):
		return self.x, self.y

	def parseLine(self):
		line = self.readLine()

		nextWord = re.compile(r'^.*?(?P<letter>[%s])' % ''.join(self.codeDict.keys()), re.IGNORECASE)
		index = 0

		lineDict = {}

		while line != '':

			letterMatch = nextWord.search(line[index:])

			if letterMatch:
				# Letter
				letter = letterMatch.group('letter').upper()
				if index == 0:
					self.lastCommand = letter
				index += letterMatch.end()

				# Value
				valueRegex = self.codeDict[letter].valueRegex
				valueMatch = valueRegex.search(line[index:])

				value = valueMatch.group() # matched text
				index += valueMatch.end() # propogate index to end of value

				lineDict[letter] = value

			else:
				return lineDict
				break

		return None


	def process(self, dict):
		
		if 'G' in dict.keys():
			if dict['G'] == '1':
				self.x = float(dict['X'])
				self.y = float(dict['Y'])	

				#return float(dict['X']), float(dict['Y'])
				return 'Move'

			elif dict['G'] == '4':
				if dict['P']:
					#time.sleep(float(dict['P'])/1000)
					pass

			elif dict['G'] == '92':
				pass


		elif 'M' in dict.keys():
			if dict['M'] == '240':
				return 'Feed'
 


	def main(self):
		self.openFile("sample.gcode")
