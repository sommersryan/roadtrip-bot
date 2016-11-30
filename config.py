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
BITLY_PREFIX = 'https://api-ssl.bitly.com/v3/shorten?'

#API Keys

DIRECTIONS_API_KEY = os.environ.get('DIRECTIONS_API_KEY')
STREETVIEW_API_KEY = os.environ.get('STREETVIEW_API_KEY')
GEOCODING_API_KEY = os.environ.get('GEOCODING_API_KEY')
BITLY_TOKEN = os.environ.get('BITLY_TOKEN')

STREETVIEW_PITCH = '0'
STREETVIEW_SIZE = '640x640'

#Won't tweet more than once per MINIMUM_TWEET_INTERVAL in seconds,
#unless this step is longer than MINIMUM_OVERRIDE_DURATION in seconds

MINIMUM_OVERRIDE_DURATION = 3600
MINIMUM_TWEET_INTERVAL = 300

AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET') or ''
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID") or ''
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY") or ''

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET') or ''
CONSUMER_KEY = os.environ.get('CONSUMER_KEY') or ''
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') or ''
ACCESS_SECRET = os.environ.get('ACCESS_SECRET') or ''