import map, trip, view, tweet, time
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL

while True:
	
	newPlan = map.Plan.random()
	newTrip = trip.Trip.fromPlan(newPlan)
	
	preamble = 'New trip! {0} to {1}. {2}, {3}'.format(newTrip.start.mediumDetail, 
		newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'])
	
	tweet.makeTweet(status=preamble, lat=newTrip.start.coord[0], long=newTrip.start.coord[1])
	
	time.sleep(60)
	
	previousInterval = MINIMUM_TWEET_INTERVAL + 1
	
	for step in newTrip.legs[0].steps:
	
		replyTo = tweet.getPreviousID()
		
		if previousInterval >= MINIMUM_TWEET_INTERVAL or int(step.duration['value']) >= MINIMUM_OVERRIDE_DURATION:
			
			previousInterval = int(step.duration['value'])
			stepTweet = 'Driving: {0}'.format(step.asString())
		
			if view.checkForView(step.start.coord):
			
				image = view.getViewObject(step.start.coord)
				tweet.makeTweetWithImage(stepTweet, image, replyTo, lat=step.start.coord[0], long=step.start.coord[1])
				time.sleep(int(step.duration['value']))
				continue
			
			tweet.makeTweet(stepTweet,replyTo=replyTo, lat=step.start.coord[0], long=step.start.coord[1])
			time.sleep(int(step.duration['value']))
		
		previousInterval = int(step.duration['value'])
		time.sleep(int(step.duration['value']))
	
	time.sleep(60)
	
	signOut = 'Trip complete! {0} traveled. Resting in {1} for a bit.'.format(newTrip.legs[0].distance['text'],newTrip.end.mediumDetail)
	
	replyTo = tweet.getPreviousID()
	
	tweet.makeTweet(signOut,replyTo=replyTo, lat=newTrip.end.coord[0], long=newTrip.end.coord[1])
	
	time.sleep(14400)