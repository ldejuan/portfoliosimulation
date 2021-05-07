__doc__ = "this files containts functions to calculate Timeseries utilities"
__version__ = '0.2'

import numpy as np
from scipy.stats import (kurtosis,skew)a
from pandas import expanding_max

def ret_statistics(ret_ts,first = True):
	r = ret_ts.values
	if not first:
		r = r[1:]
	r.vol = np.std(r) * getvolfactor(ret_ts.dates.dtype)
	r.skew =skew(r)
	r.kurt = kurtosis(r)
	r.nav = np.cumprod(1.+r)
	r.ret = r.nav[-1]-1.
	r.dd =getdd(r.nav) 
	result = {'vol':r.vol, \
		'skew':r.skew, \
		'kurt':r.kurt, \
		'ret':r.ret, \
		'dd': r.dd}


	return result 


def getvolfactor(dt64type):
	if dt64type == 'M8[D]':
		factor = 1./sqrt(252.)
	elif dt64type == 'M8[M]':
		factor = 1./sqrt(12.)
	else:
		factor = 1.
	return factor

def getdd(nav):
	mvmax = expanding_max(nav)
	mvdd = nav - mvmax
	return mvdd.min()
