__version__ ='0.1'
__doc__='calculates the  Volatility Cap from a Vol timeseries and a set of moving average filters. The list of MA filters must be is ascending order (short to llong filter), the size of the array list of the volcapvalues is the same than the ema filters ' 
from Timeseries import *
import numpy as np
class capmket:
	def __init__(self,vol_low,vol_high,alpha,nb_movfilters):
		self.vol_low = vol_low
		self.vol_high=vol_high
		self.alpha = alpha
		self.p_n = nb_movfilters*(nb_movfilters-1.)/2.

	def cal(self,p):
		return self.vol_low + (self.vol_high-self.vol_low)*(p/p_n)^alpha
	
class Mktcondition(Timeseries):
	def __init__(self,ma_filters,name=0, calculator=0)
		if name ==0:
			name = ma_filters[0].name
		self.mas = ma_filters
		self.n = ma_filters.size
		
		Timeseries.__init__(self,'MktCond%s'%name,self.ma_filters[0].dates,calculator)

	def calculate(self,i):
		p=0
		for k in range(0,self.n):
			for l in range(k+1,self.n):
				if self.mas[k].values[i]>self.mas[l].values[i]:
					p=p+1
		self.values[i] = p
		return p 
	
class Volmomemtumcap(Timeseries):
	def __init__(self,vol_underlying,ma_filters, volcap_values, name = 0, calculator=0):
		self.vol = vol_underlying
		self.mas = ma_filters
		self.volcaps = volcap_values
		if name ==0: 
			name = underlying.name
		
		Timeseries.__init__(self,'VolMomentumCap%s'%name,self.vol.dates,calculator)

	def calculate(self,i):
		return u_i
