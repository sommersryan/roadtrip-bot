import tweepy, urllib.parse, urllib.request, json
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_SECRET, BITLY_PREFIX, BITLY_TOKEN

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

def makeTweetWithImage(status, image, replyTo=None, lat=0, long=0):
## Takes text status and image object and tweets it
	if replyTo:
		api.update_with_media(filename='view.jpg', status=status, in_reply_to_status_id=replyTo, lat=lat, long=long, file=image)
		return 'Tweeted {0}'.format(status)
	
	if len(status) <= 140:
		api.update_with_media(filename='view.jpg', status=status, file=image)
		return 'Tweeted {0}'.format(status)
		
	else:
		status = status[0:140]
		api.update_with_media(filename='view.jpg', status=status, file=image)
		return 'Tweeted {0}'.format(status)
	
def makeTweet(status,replyTo=None, lat=0, long=0):
## Takes text status and tweets it
	if replyTo:
		api.update_status(status=status, in_reply_to_status_id=replyTo, lat=lat, long=long)
		return 'Tweeted {0}'.format(status)
	
	if len(status) <= 140:
		api.update_status(status=status)
		return 'Tweeted {0}'.format(status)
	
	else: 
		status = status[0:140]
		api.update_status(status=status)
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
	
	
	
	
	