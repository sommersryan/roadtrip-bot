import map, trip, view, tweet, time
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL

newPlan = map.Plan.random()
departurePoint = None

while True:
	
	if departurePoint:
		newPlan = map.Plan.toRandom(departurePoint)
	
	newTrip = trip.Trip.fromPlan(newPlan)
	
	preamble = 'New trip! {0} to {1}. {2}, {3}'.format(newTrip.start.mediumDetail, 
		newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'])
	
	tweet.makeTweet(status=preamble, lat=newTrip.start.coord[0], long=newTrip.start.coord[1])
	
	time.sleep(60)
	
	previousInterval = MINIMUM_TWEET_INTERVAL + 1
	
	for step in newTrip.legs[0].steps:
	
		replyTo = tweet.getPreviousID()
		
		mapURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/{2[0]},{2[1]}/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
			newTrip.start.coord, step.start.coord, newTrip.end.coord)
		
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
	
	departurePoint = newTrip.end
	
	time.sleep(14400)