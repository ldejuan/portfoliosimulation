__version__='0.1'
__class__='substract'
__doc__ = 'difference of two timeseries' 


import numpy as np
from Timeseries import *
import inspect

class Substract(Timeseries):
	def __init__(self,ts1,ts2, name = 0, calculator=0):
		if isinstance(ts1,(float,int)):
			self.u1= Timeseries('Cst',ts2.dates,calculator)
			self.u1.resettocstvalue(ts1)
		else: 
			self.u1 = ts1

		if isinstance(ts2,(float,int)):
			self.u2 = Timeseries('Cst',ts1.dates,calculator)
			self.u2.resettocstvalue(ts2)
		else:
			self.u2 = ts2

		if name == 0: 
			name = ts2.name
		Timeseries.__init__(self,'difference_%s'%name,self.u2.dates,calculator)
	def calculate(self,i):
		d_i = self.u1.values[i] - self.u2.values[i]
		self.values[i] = d_i

		return d_i

	def run(self):
		self.values = self.u1.values - self.u2.values	
		return self 
