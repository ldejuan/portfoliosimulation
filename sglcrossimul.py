__version__='0.1'

import Rportfolio as rp
import Timeseries as ts
import Calculator as cal
import datetime as dt
import Nav as nv
import numpy as np 
import Return as rt
from Ema import Ema
from dbmktdata import dbassets
from Singlecross import Singlecross

def singlealloc():
#part 0 : Must be Yahoo Tickers
	assets_n = 'IBEX35'
	path = '/home/luis/Work/dev/simul/db/'
#part 1 : definition of the dates schedule

	startdate = np.datetime64('2005-01-01')
	enddate   = np.datetime64(dt.date.today())
	dates = np.arange(startdate,enddate,dtype = 'datetime64[D]')
	busdates = dates[np.is_busday(dates)]
	print 'lenbusdates%s'%len(busdates) 
#part 2 : definition of the simulator and the MketData TimeSeries	
	simulator = cal.Calculator(busdates)
	ts_asset = ts.Timeseries(assets_n,busdates,0)
	ts_asset.readfromfile(path+'%s.txt'%assets_n)

#part 3 : definition of the allocations
	ts_long = Ema('Long',ts_asset,75*5,0)
	ts_short = Ema('Short',ts_asset,25*5,0)
	ts_long.run()
	ts_short.run()
 
	allocs = Singlecross('AllocSingle',ts_long,ts_short,simulator)

#part 4 :  calculation of the returns (constant)
	rts = rt.Return(assets_n,ts_asset,0)
	rts.run()

#part 5 : definition of the fund properties 
	fund = rp.Rportfolio('testportfolio',np.array([rts]),np.array([allocs]),simulator)
	fund_nav = nv.Nav('Navtest',fund,simulator)

	fund_nav.resetstartvalue(ts_asset.values[0])

#part 6 : run the simulation
	simulator.run()

#part 7 : return of the nav of the fund
	fund_nav.plot()
	ts_long.plot(True)
	ts_short.plot(True)
	ts_asset.plot(True)
	return (fund_nav,ts_long,ts_short,ts_asset)
