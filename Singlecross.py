__version__='0.1'
__class__='Single Cross Filter Allocation'
__doc__='This class defines a standard EMA Filter'
from Timeseries import *

class Singlecross(Timeseries):
	def __init__(self,tsLong,tsShort,name = 0, calculator=0):
		if name ==0 :
			name = tsLong.name
		self.tslong = tsLong
		self.tsshort = tsShort	
		Timeseries.__init__(self,'SingleCrossAlloc%s'%name,self.tslong.dates,calculator)

	def calculate(self,i):
		if self.tsshort.values[i] >= self.tslong.values[i]:
			alloc_i = 1.
		else :
			alloc_i =-1.
		self.values[i] = alloc_i
		return alloc_i
