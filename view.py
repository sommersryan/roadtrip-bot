from config import STREETVIEW_API_KEY, STREETVIEW_API_PREFIX, STREETVIEW_METADATA_API_PREFIX, STREETVIEW_PITCH, STREETVIEW_SIZE, AWS_S3_BUCKET, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import urllib.request, json, io

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
	
	
	
def getViewRequest(latLng):
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

def getViewObject(latLng):
	## Takes tuple of lat/lng and returns image object
	if checkForView(latLng):
		with urllib.request.urlopen(getViewRequest(latLng)) as response:
			image = response.read()
			
		imageObj = io.BytesIO(image)
		
		return imageObj
		
	return False
	