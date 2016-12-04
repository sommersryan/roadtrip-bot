import random, json, urllib.request
from config import MIN_LATITUDE, MAX_LATITUDE, MIN_LONGITUDE, MAX_LONGITUDE, GEOCODING_API_PREFIX, GEOCODING_API_KEY

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

class Place(object):
	
	def __init__(self, latitude=39.828194, longitude=-98.580100):
		self.latitude = latitude
		self.longitude = longitude
		self.coord = (latitude, longitude)
		
		geo = getGeoCodeResponse((latitude, longitude))
		
		if geo['status'] != 'OK':
			self.valid = False
			self.lowDetail = ''
			self.mediumDetail = ''
			self.highDetail = ''
			
		else:
			self.valid = True
			self.lowDetail = ''
			if len(geo['results']) >= 3:
				self.lowDetail = geo['results'][2]['formatted_address']
			self.mediumDetail = ''
			if len(geo['results']) >= 2:
				self.mediumDetail = geo['results'][1]['formatted_address']
			self.highDetail = geo['results'][0]['formatted_address']
	
	@classmethod
	def random(cls):
		lat = round(random.uniform(float(MIN_LATITUDE), float(MAX_LATITUDE)),6)
		long = round(random.uniform(float(MIN_LONGITUDE), float(MAX_LONGITUDE)), 6)
		inst = cls(lat,long)
		return inst

class Plan(object):
	#A plan represents a proposed trip; these can be fed to Directions API to produce a Trip object
	def __init__(self, origin, destination):
		self.origin = origin
		self.destination = destination

	@classmethod
	def random(cls):
		while True:
			origin = Place.random()
			destination = Place.random()
			
			if origin.valid and destination.valid:
				inst = cls(origin,destination)
				return inst
	
	@classmethod
	def toRandom(cls, origin=Place()):
		while True:
			origin = origin
			destination = Place.random()
			
			if destination.valid:
				inst = cls(origin,destination)
				return inst		

	@classmethod
	def fromToCoords(cls, originLatLng, destinationLatLng):
		origin = Place(latitude = originLatLng[0], longitude = originLatLng[1])
		destination = Place(latitude = destinationLatLng[0], longitude = destinationLatLng[1])
		inst = cls(origin, destination)
		return inst
		