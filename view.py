from config import STREETVIEW_API_KEY, STREETVIEW_API_PREFIX, STREETVIEW_METADATA_API_PREFIX, STREETVIEW_PITCH, STREETVIEW_SIZE
import urllib.request, json

def checkForView(latLng):
	## Takes tuple of lat, long and returns True if street view imagery exists
	request = {
		'prefix' : STREETVIEW_METADATA_API_PREFIX,
		'location' : '{0[0]},{0[1]}'.format(latLng),
		'pitch' : 0,
		'size' : STREETVIEW_SIZE,
		'key' : STREETVIEW_API_KEY
	}
	
	requestURL = '{prefix}size={size}&location={location}&pitch={pitch}&key={key}'.format(**request)
	
	with urllib.request.urlopen(requestURL) as response:
			metadata = response.read().decode('utf8')
	
	parsed = json.loads(metadata)
	
	if parsed['status'] == 'ZERO_RESULTS':
		return False
		
	return True
	
	
	
def getViewResponse(latLng):
	## Takes tuple of lat, long and gets Street View response
	
	request = {
		'prefix' : STREETVIEW_API_PREFIX,
		'location' : '{0[0]},{0[1]}'.format(latLng),
		'pitch' : 0,
		'size' : STREETVIEW_SIZE,
		'key' : STREETVIEW_API_KEY
	}
	
	requestURL = '{prefix}size={size}&location={location}&pitch={pitch}&key={key}'.format(**request)
	
	return requestURL

	