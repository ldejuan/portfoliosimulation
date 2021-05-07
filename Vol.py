__version__ ='0.1'
__doc__='calculates the volatility of a return timeseries (standard deviation)'
from Timeseries import *
import numpy as np

class Vol(Timeseries):
	def __init__(self,underlying,depth = 20, name = 0, calculator=0):
		self.depth = depth
		self.u = underlying
		if name ==0: 
			name = underlying.name
		Timeseries.__init__(self,'Volatility%s'%name,self.u.dates,calculator)
		self.factor = np.sqrt(252.)

	def calculate(self,i):
		if i<self.depth-1:
			u_i = self.factor*np.std(self.u.values[0:self.depth])
		else:
			u_i = self.factor*np.std(self.u.values[i+1-self.depth:i+1])
		self.values[i]=u_i
		return u_i
