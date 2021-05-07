__version__= '0.1'
__title__='TimeSeries class'
__doc__='Defines a TimeSeries object to handle vectors of dates and values'

import numpy as np
import bisect as bs
from urllib2 import Request,urlopen
from urllib import urlencode
import datetime as dt
import StringIO as io
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Timeseries:
	def __init__(self,name,dates=0,calculator = 0):
		self.name = name
		self.dates = dates
		if dates <> 0:
			n =dates.size 
			self.values = np.ones(shape=n,dtype=float)
		if calculator <>0:
			calculator.add(self)

	def calculate(self,i):
		return self.values[i]

	def run(self):
		self.values = np.array([self.calculate(i) for i in np.arange(0,self.dates.size)])
		return self

	def readfromfile(self,csvfilename,usecols=(0,1)):
		result = np.sort(np.genfromtxt(csvfilename,delimiter=',',names=True,usecols=usecols,dtype="datetime64[D],f8"),axis=0,kind='mergesort')
		self.values = result['Close']
		if self.dates == 0: 
			self.dates = result['Date']
		else : 
			idates = self.dates
			self.dates = result['Date']
			self.resetschedule(idates)			
		return  self

	def readfromyahoo(self,yahooticker):
		startdate = '1900-01-01'
		enddate = dt.date.today()
		params = urlencode({
		's': yahooticker,
		'a': int(startdate[5:7]) - 1,
		'b': int(startdate[8:10]),
		'c': int(startdate[0:4]),
		'd': enddate.month - 1,
		'e': enddate.day,
		'f': enddate.year,
		'g': 'd',
		'ignore': '.csv',
		})

		url = 'http://ichart.yahoo.com/table.csv?%s'%params
		resq = Request(url)
		response = urlopen(resq)
		result = response.read()
		self.readfromfile(io.StringIO(result),usecols=(0,4))

	def writetofile(self,csvfilename):
		sg_dates = np.array([str(date) for date in self.dates])
		sg_values = np.array(['%11.5f'%v for v in self.values])
		np.savetxt(csvfilename,np.column_stack((sg_dates[:,np.newaxis],sg_values[:,np.newaxis])),fmt='%s',delimiter=',',header='Date,Close')
		return self 

	def resettocstvalue(self,value):
		self.values.fill(value)

		return self
	
	def plot(self,add=True):
		if not plt.isinteractive():
			plt.ion()
		if add:
			ax = plt.gca()
		else:
			fig = plt.figure()
			ax = fig.add_subplot(111)
		ax.plot(self.dates.astype(object),self.values, label = self.name)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
		ax.xaxis.set_major_locator(mdates.YearLocator())
		plt.gcf().autofmt_xdate()
		ax.legend()
		plt.show()
		
		return self

	def resetschedule(self,idates):
		if idates == self.dates : 
			return self
		else:
			i_s =np.searchsorted(self.dates,idates,side='left')
			if i_s[-1]==len(self.dates):
				mx = np.ones(len(idates), dtype = int)
				mx.fill(len(self.dates)-1)
				i_s = np.fmin(i_s,mx)

			self.values = self.values[i_s]
			self.dates = idates

		return self
