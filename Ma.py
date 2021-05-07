__version__='0.1'
__class__='Mean Average Filter'
__doc__='This class defines a standard Mean Average Filter'
from TimeSeries import *
from scipy.signal import (lfilter,lfiltic)
import numpy as np

class Ma(Timeseries):
	def __init__(self,underlying,depth=20,name = 0,calculator=0):
		if name ==0 : 
			name = underlying.name
		self.depth = depth
		self.u     = underlying
		Timeseries.__init__(self,'Ma%s'%name,self.u.dates,calculator)
	def calculate(self,i):
		if i<depth-1 : 
			u_i = np.average(self.u.values[0:i])
		else:
			x_s = self.u.values
			u_i =self.values[i-1]+1./self.depth*(x_s[i]-x_s[i-depth+1])
		self.values[i]=u_i
		return u_i
	
	def run(self):
		a_s = np.array([1.])
		b_s = np.empty(self.depth)
		b_s.fill(1./self.depth)
		z = lfiltic(b_s,a_s,self.u.values,self.u.values)
		self.values = lfilter(b_s,a_s,self.u.values,-1,z)[0]
		
		return self	
