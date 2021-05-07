__doc__='files contaning standard strategies'
__version__='0.1'

from Allocvolcap import *
from Rportfolio import Rportfolio
from Return import Return
from Vol import Vol
from Substract import Substract
import datetime as dt
from dbmktdata import dbassets,dbfilename
from Nav import Nav
from Calculator import Calculator

class Stratvolcap(Rportfolio):
	def __init__(self,tsCore,tsSatellite,depthVol,capVol, name = 0,calculator=0):
		if name ==0: 
			name = tsCore.name
		self.rCore = Return(tsCore,0,calculator)
		self.rSatellite = Return(tsSatellite,0,calculator)
		self.vSatellite = Vol(self.rSatellite,depthVol,0,calculator)

		self.allocSatellite =Allocvolcap(self.vSatellite,capVol,0.05,0,calculator)
		self.allocCore = Substract(1.,self.allocSatellite,0,calculator)
  
		Rportfolio.__init__(self,[self.rCore,self.rSatellite],[self.allocCore,self.allocSatellite],name,calculator)		
	
	def run(self):
		self.rCore.run()
		self.rSatellite.run()
		self.vSatellite.run()
		self.allocSatellite.run()
		self.allocCore.run()

		return Rportfolio.run(self)

class StratCPPI(Nav): 
	def __init__(self,tsCore,tsSatellite,floor = 0.80, mfactor = 5., name =0, calculator =0):
		if name ==0: 
			name = tsCore.name
		self.floor = floor
		self.mfactor = mfactor

		self.rCore = Return(tsCore,tsCore.name,calculator)
		self.rSatellite = Return(tsSatellite,tsSatellite.name,calculator)
		self.navCore = Nav(self.rCore,name,calculator)
		self.allocSatellite = Timeseries('AllocSatellite_%s'%name,tsCore.dates,0)
		self.allocCore = Substract(1.,self.allocSatellite,name,0)
  
		self.rstrat = Rportfolio([self.rCore,self.rSatellite],[self.allocCore,self.allocSatellite],name,calculator)
		Nav.__init__(self,self.rstrat,'Cppi_%s'%name,calculator)
	
	def calculate(self,i):
		nav_i = Nav.calculate(self,i)
		floor_i = self.floor * self.navCore.values[i]
		allocSatellite_i = min(max(nav_i/floor_i-1.,0.)*self.mfactor,1.)
		self.allocSatellite.values[i]=allocSatellite_i
		self.allocCore.calculate(i)
		
		return nav_i

class Stratcstalloc(Rportfolio):
	def __init__(self,tsCore,tsSatellite,allocCore,name=0, calculator = 0):
		if name ==0 :
			self.name = tsCore.name
		self.rCore = Return(tsCore,0,calculator)
		self.rSatellite = Return(tsSatellite,0,calculator)

		self.allocCore = Timeseries('AllocCore',tsCore.dates)
		self.allocSatellite = Timeseries('AllocSatellite',tsCore.dates)

		self.allocCore.resettocstvalue(allocCore)
		self.allocSatellite.resettocstvalue(1.-allocCore)
		self.alloccore = allocCore 

		Rportfolio.__init__(self,[self.rCore,self.rSatellite],[self.allocCore,self.allocSatellite],'CstAlloc_%s'%name,calculator)
	
	def run(self): 
		self.rCore.run()
		self.rSatellite.run()

		return Rportfolio.run(self)	
		
def stratvolcap():
	yhnames = {'core':'EUROMTS3Y','satellite':'CAC'}

	enddate = np.datetime64(dt.date.today())
	startdate =np.datetime64('2004-01-01') 
	dates = np.arange(startdate,enddate, dtype ='datetime64[D]')
	dates = dates[np.is_busday(dates)]
	
	portfolio = {}

	for k,v in yhnames.iteritems():
		tsone = Timeseries(k,dates)
		tsone.readfromfile(dbfilename%v)
		portfolio[k] = tsone

	tsStratVolCap = Stratvolcap(portfolio['core'],portfolio['satellite'],40,.15,'CoreSatellite')
	tsStratVolCap.run()
	tsnav = Nav(tsStratVolCap)
	tsnav.run()

	tscorenav = Nav(tsStratVolCap.rCore)
	tssatellitenav = Nav(tsStratVolCap.rSatellite)

	tscorenav.run()
	tssatellitenav.run()

	tsnav.plot()
	tssatellitenav.plot()
	tscorenav.plot()
	
	return tsStratVolCap

def stratcppi():
	yhnames = {'core':'ETFLYXMTSPA','satellite':'IBEX35'}
	yhnames = {'core':'EUROMTS3Y','satellite':'CAC'}

	enddate = np.datetime64(dt.date.today())
	startdate =np.datetime64('2009-01-01') 
	dates = np.arange(startdate,enddate, dtype ='datetime64[D]')
	dates = dates[np.is_busday(dates)]
	
	portfolio = {}
	for k,v in yhnames.iteritems():
		tsone = Timeseries(k,dates)
		tsone.readfromfile(dbfilename%v)
		portfolio[k] = tsone

		print tsone.name

	cal = Calculator(dates) 

	tsnavcppi = StratCPPI(portfolio['core'],portfolio['satellite'],.8,5.,'CoreSatellite',cal)
	cal.run()

	tscorenav = Nav(tsnavcppi.rCore)
	tssatellitenav = Nav(tsnavcppi.rSatellite)

	tscorenav.run()
	tssatellitenav.run()

#	tsnavcppi.plot()
#	tssatellitenav.plot()
#	tscorenav.plot()
	
	return tsnavcppi

def stratcstalloc():
	yhnames = {'core':'ETFLYXMTSPA','satellite':'IBEX35'}
	yhnames = {'core':'EUROMTS3Y','satellite':'CAC'}

	enddate = np.datetime64(dt.date.today())
	startdate =np.datetime64('2009-01-01') 
	dates = np.arange(startdate,enddate, dtype ='datetime64[D]')
	dates = dates[np.is_busday(dates)]
	
	portfolio = {}
	for k,v in yhnames.iteritems():
		tsone = Timeseries(k,dates)
		tsone.readfromfile(dbfilename%v)
		portfolio[k] = tsone

		print tsone.name


	rcstalloc = Stratcstalloc(portfolio['core'],portfolio['satellite'],.6,'CoreSatellite')

	navcstalloc = Nav(rcstalloc,'CstAllocCoreSatellite')
	
	rcstalloc.run()
	navcstalloc.run()

	return navcstalloc
