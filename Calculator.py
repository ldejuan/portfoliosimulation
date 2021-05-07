__version__='0.1'
__doc__='Handles a vector of TimeSeries for calculation purposes'
import numpy as np

class Calculator:
	def __init__(self,dates):
		self.tselts = []
		self.dates = dates

	def add(self,tselt):
		self.tselts.append(tselt)

	def run(self):
		n = self.dates.size
		for i in np.arange(0,n):
			print i 
			for elt in self.tselts :
				elt.calculate(i)
				print elt.name
