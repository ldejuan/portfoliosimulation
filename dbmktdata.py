__version__='0.1'
__doc__='Defines the instruments on the database and updates them'

from Timeseries import *
dbpath = '/home/luis/Work/dev/simul/db/'
dbfilename = dbpath+'%s.txt'
dbassets = {'GOOG':'GOOG', \
		'MSFT':'MSFT', \
		'CAC':'^FCHI', \
		'FTSE100':'^FTSE', \
		'DAX':'^GDAXI', \
		'IBEX35':'^IBEX', \
		'SP500':'^GSPC', \
		'ETFBAEURGO':'GOVY.PA', \
		'ETFLYXMTSPA':'MTX.PA', \
		'ETFLYXMTSDE':'LYQ1.DE', \
		'EUROMTS3Y':'MA13.PA', \
		'ETFLYXCAC60':'CACM.PA'}

def dbupdate():
	for key,yhticker in dbassets.iteritems():
		print "reading %s"%key
		ts = Timeseries(key)
		ts.readfromyahoo(yhticker)
		ts.writetofile(dbfilename%key)
		print "Succes for %s"%key

	return "Sucess"
