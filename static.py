from boto.s3.connection import S3Connection
from boto.s3.key import Key
from config import AWS_S3_BUCKET, SUGGESTIONS_BUCKET
import map, random, pickle

storageConnection = S3Connection()
datastore = storageConnection.get_bucket(AWS_S3_BUCKET)
suggestionsFile = storageConnection.get_bucket(SUGGESTIONS_BUCKET)

def getLastLocation():
	rawLocation = datastore.get_key('lastlocation').get_contents_as_string()
	return pickle.loads(rawLocation)

def saveLocation(location):
	zipped = pickle.dumps(location)
	datastore.get_key('lastlocation').set_contents_from_string(zipped)
	return True
	
def getIsTrip():
	rawIsTrip = datastore.get_key('isTrip').get_contents_as_string().decode('utf8')
	
	if rawIsTrip == 'True':
		return True
		
	else:
		return False
		
def saveIsTrip(isTrip):
	
	if isTrip:
		datastore.get_key('isTrip').set_contents_from_string('True')
	
	else:
		datastore.get_key('isTrip').set_contents_from_string('False')
		
	return True
	
def saveCurrentTrip(trip):
	zipped = pickle.dumps(trip)
	datastore.get_key('currentTrip').set_contents_from_string(zipped)
	return True
	
def getCurrentTrip():
	raw = datastore.get_key('currentTrip').get_contents_as_string()
	return pickle.loads(raw)

def getSinceID():
	return datastore.get_key('since_id').get_contents_as_string().decode('utf8')

def setSinceID(newID):
	datastore.get_key('since_id').set_contents_from_string(newID)
	return True
	
def resetSinceID():
	datastore.get_key('since_id').set_contents_from_string('801194189035859969')
	return True
	
def saveSuggestion(suggestion):
	##Takes a suggestion (tuple of reply and place object), pickles, saves to S3Connection
	
	zipped = pickle.dumps(suggestion)
	key_name = str(random.randrange(111111111,999999999))
	
	while True:
	
		if not suggestionsFile.get_key(key_name):
			break
			
		key_name = str(random.randrange(111111111,999999999))
	
	k = Key(suggestionsFile)
	k.key = key_name
	k.set_contents_from_string(zipped)
	
	return True
	
def pickSuggestion():
	## Retrieves and returns a suggestion from S3Connection
	
	keys = [a for a in suggestionsFile.list()]
	selection = random.choice(keys)
	raw = selection.get_contents_as_string()
	suggestionsFile.delete_key(selection.name)
	
	return pickle.loads(raw)