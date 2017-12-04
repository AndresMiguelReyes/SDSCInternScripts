import requests
import pylab
import arrow
import sys
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

urlBase = "http://florian.sdsc.edu:5000/stations/data?"
#the base url that we use to query the database
urlSelect = "selection=withinRadius"
#selection type for the stations
urlCoords = "&lat=32.8400218&lon=-116.6733644"
#lat and lon act as the center of the circle
urlSelectParam = "&radius=2"
#radius of the circle from given coords
urlObserv = "&observable=temperature"
#choose what ?metric? you want to query the database for
to = arrow.Arrow.now()
#use arrow to form a timestamp of the current time
frm = to.replace(months=-1)
#use arrow functions to step back a month
urlDateTime = "&from='"+str(frm)+"'&to='"+str(to)+"'"
#place the timestamps given by arrow into the url, arrow formatted timestamps are valid for the REST services
urlFinal = urlBase + urlSelect + urlCoords + urlSelectParam + urlObserv+urlDateTime
#Combine the four main aspects of the URL 1.Base 2.GeoSpatial 3.Observable 4.Time Frame

r = requests.get(urlFinal)
r_json = r.json()
#use requests get to retrieve json from url created above

if r.status_code != 200:
	print "status code: %d" % r.status_code
	sys.exit(1)

r_features = r_json['features']
#create a list of features from the dictionary provided by JSON. features meaning the stations

for feat in r_features:
#step through the list of stations
	r_featProp = feat['properties']
	#properties of the features, this is where time,observable and descriptive data is held, nested dictionary design
	keys = str(r_featProp.keys())
	print keys
	## available keys
	name = r_featProp['description']['wifire_uid']
	#name is stored in description, however this is the wifire assigned ID for the station, simply using name may result in duplicates
	r_temp = r_featProp['temperature']
	#temp is our observable
	r_tempUnit = r_featProp['units']['temperature']
	r_times = r_featProp['timestamp']
	#timestamp is the timestamp generated when data is generated
	keys = str(r_featProp.keys())
	print keys
	print str()

	r_timesMins = []
	for i, val in enumerate(r_temp):
		r_timesMins.append((arrow.get(r_times[i]).timestamp-arrow.get(r_times[0]).timestamp)/60)
	
	plt.plot( r_timesMins, r_temp )
	plt.xlabel("time (minutes)")
	plt.ylabel("wind speed ("+str(r_tempUnit)+")")
	pylab.show()



