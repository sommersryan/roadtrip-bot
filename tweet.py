import tweepy
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

def makeTweetWithImage(status, image, replyTo=None, lat, long):
## Takes text status and image object and tweets it
	if replyTo:
		api.update_with_media(filename='view.jpg', status=status, in_reply_to_status_id=replyTo, lat=lat, long=long, file=image)
		return 'Tweeted {0}'.format(status)
	
	api.update_with_media(filename='view.jpg', status=status, file=image)
	return 'Tweeted {0}'.format(status)
	
def makeTweet(status,replyTo=None, lat, long):
## Takes text status and tweets it
	if replyTo:
		api.update_status(status=status, in_reply_to_status_id=replyTo, lat=lat, long=long)
		return 'Tweeted {0}'.format(status)
	
	api.update_status(status=status)
	return 'Tweeted {0}'.format(status)
	
def getPreviousID():
## Gets status ID for authenticated user's previous tweet
	statusID = api.user_timeline(count=1)[0].id_str
	return statusID