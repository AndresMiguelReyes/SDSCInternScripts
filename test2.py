import requests
from pprint import pprint

url = 'http://florian.sdsc.edu:5000/stations?selection=boundingBox&minLat=33.195&maxLat=33.2&minLon=-116.795&maxLon=-116.8'
url2 = 'http://florian.sdsc.edu:5000/stations?selection=boundingBox&minLat=33.184111395518634&maxLat=33.19750724192725&minLon=-116.77082777023315&maxLon=-116.73806190490723'
url3 = 'http://florian.sdsc.edu:5000/stations?selection=closestTo&lat=32.6616377&lon=-117.0831703'

r = requests.get(url)
r_json = r.json()

r_features = r_json['features']

for feat in r_features:
	r_featProp = feat['properties']
	keys = str(r_featProp.keys())
	name = str(r_featProp['description']['wifire_uid'])

	if ('wind_speed' in r_featProp) == 1:
		r_wind_speed = r_featProp['wind_speed']	
		
		print name + " measured wind speed: " + str(r_wind_speed['value'] ) + " " + str(r_wind_speed['units']) + " at " + (r_wind_speed['timestamp']) + "\n" + keys + "\n*************************\n"
	
	else:
		print name + " has no wind speed measurement available:" + "\n" + keys + "\n*************************\n"
	
	#print str(r_featProp['distanceFromLocation'])


#print(r_keys)
#pprint(r_features)
