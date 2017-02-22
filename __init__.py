import map, trip, view, tweet, time, sys, logging, static
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL
from urllib.error import HTTPError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

departurePoint = static.getLastLocation()
logging.info("Retrieved departure point: {0}".format(departurePoint.coord))

if static.getIsTrip():
	logging.info("In progress trip detected. Resuming.")
	newTrip = static.getCurrentTrip()

else:
	orig = departurePoint
	
	suggestion = static.pickSuggestion()
	suggestionTweet = suggestion[1]
	suggestionDestination = suggestion[0]
	
	newPlan = map.Plan(orig, suggestionDestination)

	logging.info("Plan made: {0} to {1}".format(newPlan.origin.coord, newPlan.destination.coord))

	while True: 
	
		newTrip = trip.Trip.fromPlan(newPlan)
	
		if newTrip:
			break
	
		else:
			logging.info("Bad response. Making new plan from {0}".format(orig.coord))			
			suggestion = static.pickSuggestion()
			suggestionTweet = suggestion[1]
			suggestionDestination = suggestion[0]
			newPlan = map.Plan(orig, suggestionDestination)

	logging.info("Response obtained. {0} steps.".format(len(newTrip.legs[0].steps)))
	
	attribution = "OK, @{0}. Let's go to {1}".format(suggestionTweet.user.screen_name, suggestionDestination.highDetail)
	
	tweet.makeTweet(status=attribution, replyTo=str(suggestionTweet.id))
	
	tripURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
		newTrip.start.coord, newTrip.end.coord)

	try:		
		shortTripURL = tweet.urlShorten(tripURL)

	except HTTPError:
		shortTripURL = ''
	
	preamble = 'New trip! {0} to {1}. {2}, {3} {4}'.format(newTrip.start.lowDetail, 
		newTrip.end.lowDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'], shortTripURL)

	tweet.makeTweet(status=preamble, lat=newTrip.start.coord[0], long=newTrip.start.coord[1])
	
	static.saveIsTrip(True)
	static.saveCurrentTrip(newTrip)
	time.sleep(60)

previousInterval = MINIMUM_TWEET_INTERVAL + 1

for index, step in enumerate(newTrip.legs[0].steps[newTrip.currentStep:]):
	
	logging.info("New step: {0} to {1}, duration {2} seconds".format(step.start.coord,step.end.coord, step.duration['value']))
	
	replyTo = tweet.getPreviousID()
	
	mapURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/@{2[0]},{2[1]},14z/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
		newTrip.start.coord, newTrip.end.coord, step.start.coord)
		
	shortURL = tweet.urlShorten(mapURL)
	
	logging.info("Short URL obtained: {0}".format(shortURL))
	
	newTrip.currentStep = index + 1
	
	if previousInterval >= MINIMUM_TWEET_INTERVAL or int(step.duration['value']) >= MINIMUM_OVERRIDE_DURATION:
		
		logging.info("Tweet permitted for this step.")
		
		previousInterval = int(step.duration['value'])
		stepTweet = 'Driving: {0} '.format(step.asString())
		
		logging.info("Tweet built: {0} | length {1}".format(stepTweet,len(stepTweet)))
		
		if view.checkForView(step.start.coord):
			
			if len(stepTweet) > 115:
				stepTweet = stepTweet[:115] + ' '
			
			stepTweet += shortURL
			logging.info("URL added. Tweet length now {0}".format(len(stepTweet)))
			image = view.getViewObject(step.start.coord)
			tweet.makeTweetWithImage(stepTweet, image, replyTo, lat=step.start.coord[0], long=step.start.coord[1])
			logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
			static.saveCurrentTrip(newTrip)
			time.sleep(int(step.duration['value']))
			continue
		
		else:
			tweet.makeTweet(stepTweet,replyTo=replyTo, lat=step.start.coord[0], long=step.start.coord[1])
			logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
			static.saveCurrentTrip(newTrip)
			time.sleep(int(step.duration['value']))
			continue
			
	previousInterval = int(step.duration['value'])
	logging.info("Tweet not permitted for this step. Sleeping for {0}".format(step.duration['value']))
	static.saveCurrentTrip(newTrip)
	time.sleep(int(step.duration['value']))

time.sleep(60)

signOut = 'Trip complete! {0} traveled. Resting in {1} for a bit.'.format(newTrip.legs[0].distance['text'],newTrip.end.mediumDetail)

replyTo = tweet.getPreviousID()

tweet.makeTweet(signOut,replyTo=replyTo, lat=newTrip.end.coord[0], long=newTrip.end.coord[1])

static.saveLocation(newTrip.end)

logging.info("Departure point reset to {0}. Exiting.".format(newTrip.end.coord))

static.saveIsTrip(False)

time.sleep(7200)
