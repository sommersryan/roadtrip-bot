import os

#Bound the places our bot can travel

MIN_LATITUDE = os.environ.get('MIN_LATITUDE') or ''
MAX_LATITUDE = os.environ.get('MAX_LATITUDE') or ''
MIN_LONGITUDE = os.environ.get('MIN_LONGITUDE') or ''
MAX_LONGITUDE = os.environ.get('MAX_LONGITUDE') or ''

#API URL stuff

DIRECTIONS_API_PREFIX = 'https://maps.googleapis.com/maps/api/directions/json?'
STREETVIEW_API_PREFIX = 'https://maps.googleapis.com/maps/api/streetview?'

#API Keys

DIRECTIONS_API_KEY = os.environ.get('DIRECTIONS_API_KEY')
STREETVIEW_API_KEY = os.environ.get('STREETVIEW_API_KEY')

#Minimum interval in minutes between tweets

MINIMUM_INTERVAL = 180

