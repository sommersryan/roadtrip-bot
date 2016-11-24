import random
from config import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE

def randomLocation():
	## Returns tuple of randomly selected lat/long point
	lat = round(random.uniform(MIN_LATITUDE, MAX_LATITUDE),6)
	long = round(random.uniform(MIN_LONGITUDE, MAX_LONGITUDE, 6)
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
	pass

def generateWaypoints(num):
	## Generator for num waypoints
	for i in range(0,num):
		latLong = randomLocation()
		placeName = revGeocode(latLong)
		key = 'waypoint' + str(i)
		waypoint = { 'latLong' : latLong, 'placeName' : placeName }
		yield { key : waypoint }