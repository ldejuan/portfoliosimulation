from Timeseries import *
from dbmktdata import *
from Ema import Ema
from Calculator import Calculator
from Singlecross import Singlecross
from Return import Return
from Rportfolio import Rportfolio
from Nav import Nav
from Vol import Vol 
from Allocvolcap import Allocvolcap

print dbfilename

dates = np.arange('1998-01-01','2014-02-18',dtype = 'datetime64[D]')
busdates = dates[np.is_busday(dates)]
ts= Timeseries('IBEX35',busdates)
ts.readfromfile(dbfilename%'IBEX35')

tsret = Return(ts)
tsret.run()

tsshort = Ema(ts,25*5)
tslong = Ema(ts,75*5)
tsshort.run()
tslong.run()

allocs = Singlecross(tslong,tsshort)
allocs.run()

port =Rportfolio([tsret],[allocs])
port.run()

navport = Nav(port)
navport.run()
navts = Nav(tsret)
navts.run()
navport.plot()
navts.plot()

tsVol = Vol(tsret,20) 
tsVol.run()
tsVol252 = Vol(tsret,252)
tsVol252.run()
tsAllocvolcap = Allocvolcap(tsVol,tsVol252)
tsAllocvolcap.run()
tsVol.plot()
tsVol252.plot()
tsAllocvolcap.plot(False)
