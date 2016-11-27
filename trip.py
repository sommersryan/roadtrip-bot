import urllib.request, map, json, re
from config import DIRECTIONS_API_PREFIX, DIRECTIONS_API_KEY

class Trip(object):
	
	def __init__(self, startLocation, endLocation, legs = []):
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.startText = map.revGeocode(startLocation)
		self.endText = map.revGeocode(endLocation)
		self.legs = legs
	
	@classmethod
	def fromTrip(cls, trip):
		
		request = getDirectionsURL(trip)
		jsonResponse = getDirectionsResponse(request)
			
		startLocation = trip['origin']['latLong']
		endLocation = trip['destination']['latLong']
		
		legs = []
		
		for leg in jsonResponse['routes'][0]['legs']:
			legs.append(Leg.fromJSON(leg))
		
		inst = cls(startLocation, endLocation, legs)
		
		return inst
		
	def __repr__(self):
	
		return '<{0} to {1}>'.format(self.startText, self.endText)
		
	def __str__(self):
	
		return 'From {0} to {1}'.format(self.startText, self.endText)
	
	
class Leg(object):

	def __init__(self, steps = [], startLocation =(), endLocation =(), distance = {}, duration = {}):
		self.steps = steps
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.startText = map.revGeocode(startLocation)
		self.endText = map.revGeocode(endLocation)
		self.distance = distance
		self.duration = duration
		
	@classmethod
	def fromJSON(cls, jsonObject):
		startLocation = (jsonObject['start_location']['lat'], jsonObject['start_location']['lng'])
		endLocation = (jsonObject['end_location']['lat'], jsonObject['end_location']['lng'])
		distance = jsonObject['distance']
		duration = jsonObject['duration']
		
		steps = []
		
		for step in jsonObject['steps']:
			steps.append(Step.fromJSON(step))
		
		inst = cls(steps, startLocation, endLocation, distance, duration)
		
		return inst
		
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
	
	def __repr__(self):
		return '<{0}, {1}, {2}>'.format(self.startText, self.endText, self.distance['text'])
		
	def __str__(self):
		return self.asString()

class Step(object):

	def __init__(self, htmlInstructions = '', startLocation = (), endLocation = (), distance = {}, duration = {}, maneuver = ''):
		self.htmlInstructions = htmlInstructions
		self.startLocation = startLocation
		self.startText = map.revGeocode(startLocation)
		self.endLocation = endLocation
		self.endText = map.revGeocode(endLocation)
		self.distance = distance
		self.duration = duration
		self.maneuver = maneuver
	
	@classmethod
	def fromJSON(cls, jsonObject):
		htmlInstructions = jsonObject['html_instructions']
		startLocation = (jsonObject['start_location']['lat'], jsonObject['start_location']['lng'])
		endLocation = (jsonObject['end_location']['lat'], jsonObject['end_location']['lng'])
		distance = jsonObject['distance']
		duration = jsonObject['duration']
		
		maneuver = 'None'
		
		if jsonObject.get('maneuver'):
			maneuver = jsonObject['maneuver']

		inst = cls(htmlInstructions, startLocation, endLocation, distance, duration, maneuver)
		
		return inst
		
	def asString(self):
		#change commands to verbs here? 
		cleanString = re.sub('<[^<]+?>', '', self.htmlInstructions)
		return cleanString
	
	def __str__(self):
		return self.asString()
	
	def __repr__(self):
		return '<{0}, {1}>'.format(self.maneuver, self.distance['text'])

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
