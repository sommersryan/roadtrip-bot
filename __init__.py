import map, trip, view, tweet, time
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL

while True:
	
	newPlan = map.Plan.random()
	newTrip = trip.Trip.fromPlan(newPlan)
	
	preamble = 'New trip! {0} to {1}. {2}, {3}'.format(newTrip.start.mediumDetail, newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'])
	
	tweet.makeTweet(preamble)
	
	time.sleep(60)
	
	previousInterval = MINIMUM_TWEET_INTERVAL + 1
	
	for step in newTrip.legs[0].steps:
	
		replyTo = tweet.getPreviousID()
		
		if previousInterval >= MINIMUM_TWEET_INTERVAL or step.duration['value'] >= MINIMUM_OVERRIDE_DURATION:
			
			previousInterval = step.duration['value']
			stepTweet = 'Driving: {0}'.format(step.asString())
		
			if view.checkForView(step.start.coord):
			
				image = view.getViewObject(step.start.coord)
				tweet.makeTweetWithImage(stepTweet,image,replyTo)
				time.sleep(int(step.duration['value']))
				continue
			
			tweet.makeTweet(stepTweet,replyTo=replyTo)
		
		previousInterval = step.duration['value']
	
	time.sleep(60)
	
	signOut = 'Trip complete! {0} traveled. Resting in {1} for a bit.'.format(newTrip.legs[0].distance['text'],newTrip.end.mediumDetail)
	
	replyTo = tweet.getPreviousID()
	
	tweet.makeTweet(signOut,replyTo=replyTo)
	
	time.sleep(14400)