import requests
import pylab
import arrow
import sys
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

url = "http://florian.sdsc.edu:5000/stations/data?selection=withinRadius&lat=32.6616377&lon=-117.0831703&radius=2&observable=wind_speed&from='2016-06-07T00:00:00-07:00'"

FMT = '%Y-%m-%d %H:%M:%S'

r = requests.get(url)
r_json = r.json()

if r.status_code != 200:
	print "status code: %d" % r.status_code
	sys.exit(1)

r_features = r_json['features']

#pprint(r_features)

for feat in r_features:
	r_featProp = feat['properties']
	keys = str(r_featProp.keys())
	name = str(r_featProp['description']['wifire_uid'])
	
	r_wind_speed = r_featProp['wind_speed']
	r_wind_unit = r_featProp['units']['wind_speed']
	r_times = r_featProp['timestamp']
	r_timesArrow = [0] * len(r_times)
	r_timesMins = [0] * len(r_times)

	for i, val in enumerate(r_wind_speed):

		#r_times[i] = str(r_times[i])[:-5]
		#r_times[i] 
		r_timesArrow[i] = arrow.get(r_times[i]) 
		r_timesMins[i] = (r_timesArrow[i].timestamp - r_timesArrow[0].timestamp)/60
		
		print str(r_timesMins[i]) + " " + str(r_wind_speed[i]) + " -- timestamp: " + str(r_timesArrow[i])

		#print name + " measured a speed of " + str(val) + " " + str(r_wind_unit) + " on " + str(r_times[i]) + ". This is " + str(r_timesMins[i]) + " minutes since we started measuring."
	print "size of times: " + str(len(r_timesMins)) + " - size of temps: " + str(len(r_wind_speed))
	plt.plot( r_timesMins, r_wind_speed )
	plt.xlabel("time (minutes)")
	plt.ylabel("wind speed (mps)")
	pylab.show()
	print "\n*****************************\n"
	
