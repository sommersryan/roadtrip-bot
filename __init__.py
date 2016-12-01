import map, trip, view, tweet, time, sys, logging
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

newPlan = map.Plan.random()
departurePoint = None

while True:
	
	if departurePoint:
		newPlan = map.Plan.toRandom(departurePoint)
	
	logging.info("Plan made: {0} to {1}".format(newPlan.origin.coord, newPlan.destination.coord))
	
	newTrip = trip.Trip.fromPlan(newPlan)
	
	logging.info("Response obtained. {0} steps.".format(len(newTrip.legs[0].steps)))
	
	tripURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
			newTrip.start.coord, newTrip.end.coord)
			
	shortTripURL = tweet.urlShorten(tripURL)
	
	preamble = 'New trip! {0} to {1}. {2}, {3} {4}'.format(newTrip.start.mediumDetail, 
		newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'], shortTripURL)
	
	tweet.makeTweet(status=preamble, lat=newTrip.start.coord[0], long=newTrip.start.coord[1])
	
	time.sleep(60)
	
	previousInterval = MINIMUM_TWEET_INTERVAL + 1
	
	for step in newTrip.legs[0].steps:
	
		replyTo = tweet.getPreviousID()
		
		mapURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/@{2[0]},{2[1]},14z/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
			newTrip.start.coord, newTrip.end.coord, step.start.coord)
			
		shortURL = tweet.urlShorten(mapURL)
		
		logging.info("Short URL obtained: {0}".format(shortURL))
		
		if previousInterval >= MINIMUM_TWEET_INTERVAL or int(step.duration['value']) >= MINIMUM_OVERRIDE_DURATION:
			
			logging.info("Tweet permitted for this step permitted.")
			
			previousInterval = int(step.duration['value'])
			stepTweet = 'Driving: {0} '.format(step.asString())
			
			logging.info("Tweet built: {0} | length {1}".format(stepTweet,len(stepTweet)))
			
			if view.checkForView(step.start.coord):
				stepTweet += shortURL
				image = view.getViewObject(step.start.coord)
				tweet.makeTweetWithImage(stepTweet, image, replyTo, lat=step.start.coord[0], long=step.start.coord[1])
				logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
				time.sleep(int(step.duration['value']))
				continue
			
			tweet.makeTweet(stepTweet,replyTo=replyTo, lat=step.start.coord[0], long=step.start.coord[1])
			logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
			time.sleep(int(step.duration['value']))
		
		logging.info("Tweet not permitted for this step. Sleeping for {0}".format(step.duration['value']))
		previousInterval = int(step.duration['value'])
		time.sleep(int(step.duration['value']))
	
	time.sleep(60)
	
	signOut = 'Trip complete! {0} traveled. Resting in {1} for a bit.'.format(newTrip.legs[0].distance['text'],newTrip.end.mediumDetail)
	
	replyTo = tweet.getPreviousID()
	
	tweet.makeTweet(signOut,replyTo=replyTo, lat=newTrip.end.coord[0], long=newTrip.end.coord[1])
	
	departurePoint = newTrip.end
	
	logging.info("Departure point reset to {0}. Sleeping for 4 hours".format(departurePoint.coord))
	
	time.sleep(14400)