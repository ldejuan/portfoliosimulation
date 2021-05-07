__version__='0.1'
__doc__='Calculates the return of a portfolio for simulation'
from Timeseries import *
import numpy as np

class Rportfolio(Timeseries):
	def __init__(self,r_underlyings,allocs,name = 0,calculator=0):
		if name ==0 : 
			name = r_underlyings[0].name

		self.r_us = r_underlyings
		self.allocs = allocs
		Timeseries.__init__(self,'Rportfolio%s'%name,r_underlyings[0].dates,calculator)

	def calculate(self,i):
		if i==0 : 
			r_i=0.
		else:
			r_i =np.sum([alloc.values[i-1]*r_under.values[i] for alloc,r_under in zip(self.allocs,self.r_us)]) 
		
		self.values[i]=r_i
		return r_i





