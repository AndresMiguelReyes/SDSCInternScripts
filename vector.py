import requests
import sys
import arrow
import matplotlib.pyplot as plt
from pprint import pprint
from scipy.misc import imread

urlBase =  "http://florian.sdsc.edu:5000/stations/data/latest?"
urlSelect = "selection=withinRadius"
urlCoords = "&lat=32.8400218&lon=-116.6733644"
urlSelectParam = "&radius=10"
urlObserv = "&observable=temperature&observable=wind_speed&observable=wind_direction"
### CHANGE QUERY TO SELECT LATEST , FORMAT IN NOTEBOOK ###
to = arrow.Arrow.now()
frm = to.replace(hours=-1)
urlDateTime = "&from='"+str(frm)+"'&to='"+str(to)+"'"
#urlDateTime = "/latest"

urlFinal = urlBase + urlSelect + urlCoords + urlSelectParam + urlObserv#+urlDateTime

r = requests.get(urlFinal)
r_json = r.json()

print urlFinal

if r.status_code != 200:
	print "status code: %d" % r.status_code
	sys.exit(1)

r_features = r_json['features']

#pprint (r_features)

r_lat = []
r_lon = []
r_wind_speed = []
r_wind_direction = []
r_temperature = []

for feat in r_features:
	r_featProp = feat['properties']
	keys = str(r_featProp.keys())
	name = str(r_featProp['description']['wifire_uid'])

	r_lat.append(feat['geometry']['coordinates'][1])
	r_lon.append(feat['geometry']['coordinates'][0])
	
	#print name + " has keys: \n" + keys 
	r_wind_speed.append(r_featProp['wind_speed']['value'])
	#r_wind_unit = r_featProp['wind_speed']['units']
	r_wind_direction.append(r_featProp['wind_direction']['value'])
	r_temperature.append(r_featProp['temperature']['value'])
	#print str(r_location)
	#print str(r_wind_speed)

	#print "\t" + name + "\n*********************************\n" + "wind speed:  \t" + str(r_wind_speed) + " " + str(r_wind_unit) + "\nwind direction:\t" + str(r_wind_direction) + "\ntemperature: \t" + str(r_temperature) + "\nlat:\t\t" +str(r_lat) + "\nlon:\t\t" +str(r_lon)+"\n*********************************\n"

plot2 = plt.figure()
#img = imread("staticmap.png")
#plt.imshow(img,zorder=0)
ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
plt.quiver(r_lon,r_lat,r_wind_speed,r_wind_direction,color = 'Teal', headlength = 4,zorder =1 )
plt.title('lat=32.6616377&lon=-117.0831703')
plt.xlabel("lon (deg.N)")
plt.ylabel("lat (deg.W")
plt.show()

	 

