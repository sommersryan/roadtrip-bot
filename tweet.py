import tweepy
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

def makeTweetWithImage(status, image, replyTo):
## Takes text status and image object and tweets it
	api.update_with_media(filename='view.jpg', status=status, in_reply_to_status_id=replyTo, file=image)
	return True
	
def makeTweet(status,replyTo):
## Takes text status and tweets it
	api.update_status(status=status, in_reply_to_status_id=replyTo)
	return True