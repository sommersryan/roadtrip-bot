import urllib.request, json
from config import DIRECTIONS_API_PREFIX, DIRECTIONS_API_KEY

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
		
	