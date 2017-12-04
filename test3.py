import requests
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
import pylab

def minConv(convTime):
	hrs = convTime[0:2]
	
	if (hrs[0:1] == '0'):
		mins = int(hrs[1:2])*60
		mins = mins + int(convTime[3:5])
		return mins
	elif (hrs[0:1] == '1' or hrs[0:1] == '2'):
		mins = int(hrs[0:2]) *60
		mins = mins + int(convTime[3:5])
		return mins

url = 'http://florian.sdsc.edu:5000/stations/data?selection=withinRadius&lat=32.6616377&lon=-117.0831703&radius=2&observable=wind_speed&from=2016-07-08'
FMT = '%Y-%m-%d %H:%M:%S'

r = requests.get(url)
r_json = r.json()

r_features = r_json['features']

#pprint(r_features)

for feat in r_features:
	r_featProp = feat['properties']
	keys = str(r_featProp.keys())
	name = str(r_featProp['description']['wifire_uid'])
	
	r_wind_speed = r_featProp['wind_speed']
	r_wind_unit = r_featProp['units']['wind_speed']
	r_times = r_featProp['timestamp']
	r_timesDT = r_featProp['timestamp']
	r_timesMins = [0] * len(r_timesDT)

	for i, val in enumerate(r_wind_speed):
		r_times[i] = str(r_times[i])[:-5]
		r_timesDT[i] = datetime.strptime(r_times[i],FMT)
		r_timesDT[i] = r_timesDT[i] - r_timesDT[0]
		
		caller = str(r_timesDT[i])[11:]		
		called = minConv(caller)
		r_timesMins[i] = called
		#print str(called)
		#print str(r_timesMins[i]) + " " + str(r_wind_speed[i])

		#print name + " measured a speed of " + str(val) + " " + str(r_wind_unit) + " on " + str(r_times[i]) + ". This is " + str(r_timesMins[i]) + " minutes since we started measuring."
	print "size of times: " + str(len(r_timesMins)) + " - size of temps: " + str(len(r_wind_speed))
	plt.plot( r_timesMins, r_wind_speed )
	plt.xlabel("time (minutes)")
	plt.ylabel("wind speed (mps)")
	pylab.show()
	print "\n*****************************\n"
	 
