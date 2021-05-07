__version__='0.1'
__class__='Exponential Moving Average Filter'
__doc__='This class defines a standard EMA Filter'
from Timeseries import *
from scipy.signal import (lfilter,lfiltic)
import numpy as np

class Ema(Timeseries):
	def __init__(self,underlying,depth=20,name = 0,calculator=0):
		if name ==0:
			name = underlying.name
		self.factor =2./(1.+depth) 
		self.u     = underlying
		Timeseries.__init__(self,'Ema%s'%name,self.u.dates,calculator)

	def calculate(self,i):
		if i==0: 
			u_i=self.u.values[0] 
		else:
			u_i =self.u.values[i]*self.factor +(1.-self.factor)*self.values[i-1]
		self.values[i]=u_i
		return u_i

	def run(self):
		a_s = np.array([1.,-1.+self.factor])
		b_s = np.array([self.factor])
		z = lfiltic(b_s,a_s,self.u.values)
		self.values = lfilter(b_s,a_s,self.u.values,-1,z)[0]
		self.values[0] = self.u.values[0]
	
		return self
