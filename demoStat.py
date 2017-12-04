import requests
import pandas

def buildObserv():
	observ = raw_input( "select your desired observable  valid observables are: temperature, dew_point, relative_humidity, wind_speed, wind_direction, pressure, solar_radiation, precipitation, fuel_temperature, and fuel_moisture:\n" )
	urlObserv = "&observable="+observ
	return observ

def buildDateTime():
	date = raw_input("Select a date to start gathering data from (Format:YYYY-MM-DD) :\n")
	dateTime = "&from='"+date+"T00:00:00-07:00'"
	return dateTime

def urlBuild():
	urlBase =  "http://florian.sdsc.edu:5000/stations/data?"
	urlSelect = "selection=withinRadius"
	urlCoords = "&lat=32.6616377&lon=-117.0831703"
	urlSelectParam = "&radius=2"
	observ = buildObserv()
	urlObserv = "&observable=" + observ #work on returning stuff and observs with r_featProp['observ']
	urlDateTime = buildDateTime()
	urlFinal = urlBase + urlSelect + urlCoords + urlSelectParam + urlObserv + urlDateTime
	return urlFinal


urlFinal = urlBuild()
r = requests.get(urlFinal)
r_json = r.json()

if r.status_code != 200:
	print "status code: %d" % r.status_code
	sys.exit(1)

r_features = r_json['features']
for feat in r_features:
	r_featProp = feat['properties']
	name = str(r_featProp['description']['wifire_uid'])
	r_wind_speed = r_featProp['wind_speed']
	r_temperature = r_featProp['temperature']
	df = pandas.DataFrame(r_wind_speed)
	df2 = pandas.DataFrame(r_temperature)
	print "\t" + name + ":\n----------------------------------"
	print df.describe()
	print "\n----------------------------------"
	print df2.describe()
	print "\n----------------------------------"
