import urllib.request, json, re
from config import DIRECTIONS_API_PREFIX, DIRECTIONS_API_KEY

class RoadTrip(Object):
	
	def __init__(self, legs = []):
		self.legs = legs
		
class TripLeg(Object):

	def __init__(self, steps = [], startLocation =(), endLocation =(), distance = 0, duration =0):
		self.steps = steps
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.distance = distance
		self.duration = duration

class LegStep(Object):

	def __init__(self, htmlInstructions = '', startLocation = (), endLocation = (), distance = 0, duration = 0):
		self.htmlInstructions = htmlInstructions
		self.startLocation = startLocation
		self.endLocation = endLocation
		self.distance = distance
		self.duration = duration
		
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
		
