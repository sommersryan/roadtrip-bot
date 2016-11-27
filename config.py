import os

#Bound the places our bot can travel

MIN_LATITUDE = os.environ.get('MIN_LATITUDE') or ''
MAX_LATITUDE = os.environ.get('MAX_LATITUDE') or ''
MIN_LONGITUDE = os.environ.get('MIN_LONGITUDE') or ''
MAX_LONGITUDE = os.environ.get('MAX_LONGITUDE') or ''

#API URL stuff

DIRECTIONS_API_PREFIX = 'https://maps.googleapis.com/maps/api/directions/json?'
STREETVIEW_API_PREFIX = 'https://maps.googleapis.com/maps/api/streetview?'
STREETVIEW_METADATA_API_PREFIX = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
GEOCODING_API_PREFIX = 'https://maps.googleapis.com/maps/api/geocode/json?'

#API Keys

DIRECTIONS_API_KEY = os.environ.get('DIRECTIONS_API_KEY')
STREETVIEW_API_KEY = os.environ.get('STREETVIEW_API_KEY')
GEOCODING_API_KEY = os.environ.get('GEOCODING_API_KEY')

STREETVIEW_PITCH = '0'
STREETVIEW_SIZE = '600x300'

#Minimum interval in minutes between tweets

MINIMUM_INTERVAL = 180

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET') or ''
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID") or ''
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY") or ''
