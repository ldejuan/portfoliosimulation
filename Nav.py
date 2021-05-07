__version__='0.1'
__class__='NAV'
__doc__='This class calculates the NAV from a return series'
from Timeseries import *
import numpy as np

class Nav(Timeseries):
	def __init__(self,r_underlying,name = 0 ,calculator=0):
		if name ==0 :
			name = r_underlying.name

		self.r_u     = r_underlying
		Timeseries.__init__(self,'Nav%s'%name,self.r_u.dates,calculator)
		self.startvalue = 100.

	def resetstartvalue(self,nav0):
		self.startvalue = nav0

	def calculate(self,i):
		if i==0:
			nav_i=self.startvalue
		else:
			nav_i = self.values[i-1]*(1.+self.r_u.values[i])
		self.values[i] = nav_i
		return nav_i

	def run(self): 
		r= self.r_u.values
		self.values = 1.+r
		self.values[0]= self.startvalue
		self.values = np.cumprod(self.values)

		return self
		
