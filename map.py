import random, json, urllib.request
from config import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE, GEOCODING_API_PREFIX, GEOCODING_API_KEY

def randomLocation():
	## Returns tuple of randomly selected lat/long point
	lat = round(random.uniform(float(MIN_LATITUDE), float(MAX_LATITUDE)),6)
	long = round(random.uniform(float(MIN_LONGITUDE), float(MAX_LONGITUDE)), 6)
	return (lat,long)
	
def buildTrip():
	## Selects a destination and origin and builds dict to return
	originLatLong = randomLocation()
	origin = { 'latLong' : originLatLong, 'placeName' : revGeocode(originLatLong) }
	destinationLatLong = randomLocation()
	destination = { 'latLong' : destinationLatLong, 'placeName' : revGeocode(destinationLatLong) }
	trip = { 'origin' : origin, 'destination' : destination }
	return trip
	
def revGeocode(latLong):
	## Takes a tuple of latitude, longitude and returns string of place name
	response = getGeoCodeResponse(latLong)
	return parseGeoCodeResponse(response)

def getGeoCodeResponse(latLong):
	## Takes a tuple of latitude, longitude, builds request and gets geocode data	
	request = { 
		'prefix' : GEOCODING_API_PREFIX,
		'latitude' : latLong[0], 
		'longitude' : latLong[1], 
		'key' : GEOCODING_API_KEY
		}
	
	requestURL = '{prefix}latlng={latitude},{longitude}&key={key}'.format(**request)
	
	with urllib.request.urlopen(requestURL) as response:
		geoData = response.read().decode('utf8')
	
	parsed = json.loads(geoData)
	
	return parsed
	
def parseGeoCodeResponse(response):
	## Parses a response from getGeoCodeResponse
	if not 'results' in response:
		return None
	
	if len(response['results']) > 1:
		return response['results'][1]['formatted_address']
		
	else:
		return response['results'][0]['formatted_address']
	

def generateWaypoints(num):
	## Generator for num waypoints
	for i in range(0,num):
		latLong = randomLocation()
		placeName = revGeocode(latLong)
		waypoint = { 'latLong' : latLong, 'placeName' : placeName }
		yield waypoint

def addWaypoints(trip, numWaypoints):
	## Adds waypoints to trip
	for i in enumerate(generateWaypoints(numWaypoints)):
		trip.update({'waypoint' + str(i[0]) : i[1]})
	
	return trip