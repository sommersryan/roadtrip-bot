import urllib.request, map, json, re
from config import DIRECTIONS_API_PREFIX, DIRECTIONS_API_KEY

class RoadTrip(object):
	
	def __init__(self, legs = []):
		self.legs = legs
		
class Leg(object):

	def __init__(self, steps = [], startLocation =(), endLocation =(), distance = {}, duration = {}):
		self.steps = steps
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.distance = distance
		self.duration = duration
	
	def asString(self):
		legString = ''
		legString += map.revGeocode(self.startLocation)
		legString += ' to '
		legString += map.revGeocode(self.endLocation)
		legString += ', '
		legString += self.distance['text']
		legString += ', '
		legString += self.duration['text']
		
		return legString
		

class Step(object):

	def __init__(self, htmlInstructions = '', startLocation = (), endLocation = (), distance = {}, duration = {}):
		self.htmlInstructions = htmlInstructions
		self.startLocation = startLocation
		self.startText = map.revGeocode(startLocation)
		self.endLocation = endLocation
		self.endText = map.revGeocode(endLocation)
		self.distance = distance
		self.duration = duration
	
	@classmethod
	def fromJSON(cls, jsonObject):
		htmlInstructions = jsonObject['html_instructions']
		startLocation = (jsonObject['start_location']['lat'], jsonObject['start_location']['lng'])
		endLocation = (jsonObject['end_location']['lat'], jsonObject['end_location']['lng'])
		startText = map.revGeocode(startLocation)
		endText = map.revGeocode(endLocation)
		distance = jsonObject['distance']
		duration = jsonObject['duration']
		
		inst = cls(htmlInstructions, startLocation, endLocation, distance, duration)
		
		return inst
		
	def asString(self):
		#change commands to verbs here? 
		cleanString = re.sub('<[^<]+?>', '', self.htmlInstructions)
		return cleanString
		
def getDirectionsURL(trip, avoidHighways=True):
	## takes Trip dict from buildTrip, checks for waypoints, builds request and gets response
	
	waypoints = []
	
	for key, value in trip.items():
		if key.startswith('waypoint'):
			waypoints.append(value['latLong'])
	
	request = {
		'prefix' : DIRECTIONS_API_PREFIX,
		'origin' : trip['origin']['latLong'],
		'destination' : trip['destination']['latLong'],
		'waypoints' : waypoints,
		'key' : DIRECTIONS_API_KEY }

	requestURL = '{prefix}origin={origin[0]},{origin[1]}&destination={destination[0]},{destination[1]}'.format(**request)
		
	if waypoints:
		requestURL += '&waypoints='
			
		for waypoint in waypoints:
			requestURL+= 'via:{0[0]}%2c{0[1]}%7c'.format(waypoint)
		
	if avoidHighways:
	
		requestURL += '&avoid=highways'
		
	requestURL += '&key={0}'.format(request['key'])
	
	return requestURL
	
def getDirectionsResponse(requestURL):
	## takes request URL from getDirectionsURL and retrieves response
	
	with urllib.request.urlopen(requestURL) as response:
		directionsResponse = response.read().decode('utf8')
		
	serialResponse = json.loads(directionsResponse)
	
	return serialResponse

def parseDirectionsResponse(response):
	
	if response['status'] != 'OK':
		return None
		
