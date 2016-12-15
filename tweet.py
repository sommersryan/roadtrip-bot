import tweepy, urllib.parse, urllib.request, json, random, static, map, trip
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_SECRET, BITLY_PREFIX, BITLY_TOKEN

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

def makeTweetWithImage(status, image, replyTo=None, lat=0, long=0):
## Takes text status and image object and tweets it
	if len(status) >= 140:
		status = status[:140]
	
	if replyTo:
		api.update_with_media(filename='view.jpg', status=status, in_reply_to_status_id=replyTo, lat=lat, long=long, file=image)
		return 'Tweeted {0}'.format(status)
	
	else:
		api.update_with_media(filename='view.jpg', status=status, lat=lat, long=long, file=image)
		return 'Tweeted {0}'.format(status)
	
def makeTweet(status,replyTo=None, lat=0, long=0):
## Takes text status and tweets it
	if len(status) >= 140:
		status = status[:140]

	if replyTo:
		api.update_status(status=status, in_reply_to_status_id=replyTo, lat=lat, long=long)
		return 'Tweeted {0}'.format(status)

	else: 
		api.update_status(status=status, lat=lat, long=long)
		return 'Tweeted {0}'.format(status)

	
def getPreviousID():
## Gets status ID for authenticated user's previous tweet
	statusID = api.user_timeline(count=1)[0].id_str
	return statusID
	
def urlShorten(url):
## Shortens URL with Bitly
	values = {'longUrl' : url}
	data = urllib.parse.urlencode(values)
	req = urllib.request.Request('{0}access_token={1}&{2}&format=txt'.format(BITLY_PREFIX, BITLY_TOKEN, data))
	
	with urllib.request.urlopen(req) as response:
		shortened = response.read().strip().decode('utf8')
		
	return shortened
	
def getReplies(sinceID):
## retrieve and return list of replies since last ID at the user	
	tweets = api.search(q='@{0}'.format(api.me().screen_name), since_id=static.getSinceID())
	return tweets
	
def getSuggestions():
## take a list of replies and attempt to pick a new destination; return tuple of status and map.place object 
	
	suggestions = getReplies(static.getSinceID)
	possiblePlaces = []
	
	for suggestion in suggestions:
		
		sugString = suggestion.text
		
		for user in suggestion.entities['user_mentions']:
		
			sugString = sugString.replace('@{0} '.format(user['screen_name']),'')
		
		place = map.findPlaceNames(sugString)
		
		if place:
		
			possiblePlaces.append((place, suggestion))
	
	return possiblePlaces