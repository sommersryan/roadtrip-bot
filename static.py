from boto.s3.connection import S3Connection
from boto.s3.key import Key
from config import AWS_S3_BUCKET
import map

storageConnection = S3Connection()
datastore = storageConnection.get_bucket(AWS_S3_BUCKET)

def getLastLocation():
	rawCoordinates = datastore.get_key('lastlocation').get_contents_as_string().decode('utf8')
	return tuple([float(a) for a in rawCoordinates.split(',')])

def saveLocation(location):
	coordString = ",".join([str(a) for a in location.coord])
	datastore.get_key('lastlocation').set_contents_from_string(coordString)
	return True