import urllib.request, map, json, re
from config import DIRECTIONS_API_PREFIX, DIRECTIONS_API_KEY

class Trip(object):
	
	def __init__(self, start = map.Place(), end = map.Place(), legs = []):
		self.start = start
		self.end = end
		self.legs = legs
	
	@classmethod
	def fromPlan(cls, plan):
		
		request = getDirectionsURL(plan)
		jsonResponse = getDirectionsResponse(request)
		
		if jsonResponse['status'] != 'OK':
			return None
		
		start = plan.origin
		end = plan.destination
		
		legs = []
		
		for leg in jsonResponse['routes'][0]['legs']:
			legs.append(Leg.fromJSON(leg))
		
		inst = cls(start, end, legs)
		
		return inst
		
	def __repr__(self):
	
		return '<{0} to {1}>'.format(self.start.highDetail, self.end.highDetail)
		
	def __str__(self):

		return 'From {0} to {1} {2}'.format(self.start.highDetail, self.end.highDetail)
	
	
class Leg(object):

	def __init__(self, steps = [], start = map.Place(), end = map.Place(), distance = {}, duration = {}):
		self.steps = steps
		self.start = start
		self.end = end
		self.distance = distance
		self.duration = duration
		
	@classmethod
	def fromJSON(cls, jsonObject):
		start = map.Place(jsonObject['start_location']['lat'], jsonObject['start_location']['lng'])
		end = map.Place(jsonObject['end_location']['lat'], jsonObject['end_location']['lng'])
		distance = jsonObject['distance']
		duration = jsonObject['duration']
		
		steps = []
		
		for step in jsonObject['steps']:
			steps.append(Step.fromJSON(step))
		
		inst = cls(steps, start, end, distance, duration)
		
		return inst
		
	def asString(self):
		legString = ''
		legString += self.start.mediumDetail
		legString += ' to '
		legString += self.end.mediumDetail
		legString += ', '
		legString += self.distance['text']
		legString += ', '
		legString += self.duration['text']
		
		return legString
	
	def __repr__(self):
		return '<{0}, {1}, {2}>'.format(self.start.mediumDetail, self.end.mediumDetail, self.distance['text'])
		
	def __str__(self):
		return self.asString()

class Step(object):

	def __init__(self, htmlInstructions = '', start = map.Place(), end = map.Place(), distance = {}, duration = {}, maneuver = ''):
		self.htmlInstructions = htmlInstructions
		self.start = start
		self.end = end
		self.distance = distance
		self.duration = duration
		self.maneuver = maneuver
	
	@classmethod
	def fromJSON(cls, jsonObject):
		htmlInstructions = jsonObject['html_instructions']
		start = map.Place(jsonObject['start_location']['lat'], jsonObject['start_location']['lng'])
		end = map.Place(jsonObject['end_location']['lat'], jsonObject['end_location']['lng'])
		distance = jsonObject['distance']
		duration = jsonObject['duration']
		
		maneuver = 'None'
		
		if jsonObject.get('maneuver'):
			maneuver = jsonObject['maneuver']

		inst = cls(htmlInstructions, start, end, distance, duration, maneuver)
		
		return inst
		
	def asString(self):
		#change commands to verbs here? 
		divBeginOut = re.sub('<div[^>]*>', '\r', self.htmlInstructions)
		divEndOut = re.sub('</div>', '', divBeginOut)
		cleanString = re.sub('<[^<]+?>', '', divEndOut)
		return cleanString
	
	def __str__(self):
		return self.asString()
	
	def __repr__(self):
		return '<{0}, {1}>'.format(self.maneuver, self.distance['text'])

def getDirectionsURL(plan, avoidHighways=True):
	## takes map.Plan, builds request and gets response

	request = {
		'prefix' : DIRECTIONS_API_PREFIX,
		'origin' : plan.origin.coord,
		'destination' : plan.destination.coord,
		'key' : DIRECTIONS_API_KEY }

	requestURL = '{prefix}origin={origin[0]},{origin[1]}&destination={destination[0]},{destination[1]}'.format(**request)

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
