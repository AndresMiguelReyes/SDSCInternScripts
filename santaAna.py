import requests
import sys
import arrow
import pylab
import matplotlib.pyplot as plt
from pprint import pprint

urlBase =  "http://florian.sdsc.edu:5000/stations/data?"
urlSelect = "selection=withinRadius"
urlCoords = "&lat=32.8400218&lon=-116.6733644"
urlSelectParam = "&radius=10"
urlObserv = "&observable=relative_humidity&observable=wind_speed&observable=wind_direction"

to = arrow.Arrow.now()
frm = to.replace(months=-6)
frm2 = frm.replace(days=-30)
urlDateTime = "&from='"+str(frm2)+"'&to='"+str(frm)+"'"

urlFinal = urlBase + urlSelect + urlCoords + urlSelectParam + urlObserv+urlDateTime

r = requests.get(urlFinal)
r_json = r.json()

#print urlFinal

if r.status_code != 200:
	print "status code: %d" % r.status_code
	sys.exit(1)

#pprint (r_json)

r_features = r_json['features']

print "number of stations: " + str(len(r_features))
for feat in r_features:
	r_featProp = feat['properties']
	keys = str(r_featProp.keys())
	name = str(r_featProp['description']['wifire_uid'])

	r_wind_speed = r_featProp['wind_speed']
	r_times = r_featProp['timestamp']
	r_wind_direction = r_featProp['wind_direction']
	r_relative_humidity = r_featProp['relative_humidity']
	
	for i, val in enumerate(r_wind_speed):
		if (r_wind_speed[i] >= 11.2) and ( (10<= r_wind_direction[i]) and (r_wind_direction[i] <= 110) ) and (r_relative_humidity[i] >= 25):
			windGraph = []
			timeGraph = []
			titleTimes = []
			for x in xrange(i-10,i+11):
				if (x == i-10):
					titleTimes.append(r_times[x])
				elif (x == i+11):
					titleTimes.append(r_times[x])

				timeDiff = (arrow.get(r_times[x]).timestamp - arrow.get(r_times[i-10]).timestamp)/60
				timeGraph.append(timeDiff)
				windGraph.append(r_wind_speed[x])
			
			plt.plot( timeGraph, windGraph )			
			plt.xlabel("time (minutes)")
			plt.ylabel("wind speed (mps)")
			plt.axhline(y=11.2,color='r',ls='dashed')
			plt.annotate('Santa Ana', xy=(20,11.3), xycoords='data',color ='r')
			title = name + " Santa Ana Winds:\n" + str(titleTimes[0]) + " - " + str(titleTimes[-1])
			plt.title(title)
			pylab.show()
			#print  name +" measured:\nTHIS IS A SANTA ANA WIND AT: " + str(timeGraph)
	#print keys
