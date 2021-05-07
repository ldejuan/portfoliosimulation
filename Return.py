__version__='0.1'
__class__='Return'
__doc__ = 'return calculation with optimized method' 

import numpy as np
from Timeseries import *

class Return(Timeseries):
	def __init__(self,underlying,name = 0, calculator=0):
		self.u     = underlying
		if name == 0: 
			name = underlying.name
		Timeseries.__init__(self,'Return_%s'%name,self.u.dates,calculator)

	def calculate(self,i):
		if i==0:
			r_i =0.
		else:
			r_i= self.u.values[i]/self.u.values[i-1]-1.
		self.values[i] = r_i
		return r_i

	def run(self):
		uvs = self.u.values
		self.values =np.concatenate(([0],np.add(np.divide(uvs[1:],uvs[:-1]),-1.)))
	
		return self 
