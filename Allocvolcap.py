__version__='0.1'
__doc__='Volatility cap allocation strategy'
__class__='Volatility Cap Strategy : Returns de allocation'
from Timeseries import * 
from Vol import Vol

class Allocvolcap(Timeseries):
	def __init__(self,ts_volu,ts_volcap,hedgestep = 0.05,name = 0, calculator=0):
		self.volu = ts_volu
		if name ==0:
			name = ts_volu.name
		if isinstance(ts_volcap,(int,float)):
			self.volcap = Timeseries("Volcap",ts_volu.dates,calculator)
			self.volcap.resettocstvalue(ts_volcap)
		else:
			self.volcap = ts_volcap

		self.hedgestep = hedgestep
		Timeseries.__init__(self,'allocvolcap%s'%name,ts_volu.dates,calculator)

	def calculate(self,i):
		alloc_i = min(self.volcap.values[i]/self.volu.values[i],1.)
		print i, self.volcap.values[i], self.volu.values[i], alloc_i
		alloc_i_1 = alloc_i 
		if i == 0:
			alloc_i_1 = alloc_i
		else:
			alloc_i_1 =self.values[i-1] 

		if abs(alloc_i-alloc_i_1)<self.hedgestep:
			alloc_i = alloc_i_1
		self.values[i] =alloc_i 
	
		return alloc_i
