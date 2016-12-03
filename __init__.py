import map, trip, view, tweet, time, sys, logging, static
from config import MINIMUM_OVERRIDE_DURATION, MINIMUM_TWEET_INTERVAL
from urllib.error import HTTPError

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

lastLoc = static.getLastLocation()

departurePoint = map.Place(lastLoc[0],lastLoc[1])

logging.info("Retrieved departure point: {0}".format(departurePoint))
	
newPlan = map.Plan.toRandom(departurePoint)

logging.info("Plan made: {0} to {1}".format(newPlan.origin.coord, newPlan.destination.coord))

while True: 
	
	newTrip = trip.Trip.fromPlan(newPlan)
	
	if newTrip:
		break
	
	else:
		logging.info("Bad response. Making new plan from {0}".format(departurePoint.coord))			
		newPlan = map.Plan.toRandom(departurePoint)

logging.info("Response obtained. {0} steps.".format(len(newTrip.legs[0].steps)))

tripURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
		newTrip.start.coord, newTrip.end.coord)

try:		
	shortTripURL = tweet.urlShorten(tripURL)

except HTTPError:
	shortTripURL = ''
	
preamble = 'New trip! {0} to {1}. {2}, {3} {4}'.format(newTrip.start.mediumDetail, 
	newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'], shortTripURL)

tweet.makeTweet(status=preamble, lat=newTrip.start.coord[0], long=newTrip.start.coord[1])

time.sleep(60)

previousInterval = MINIMUM_TWEET_INTERVAL + 1

for step in newTrip.legs[0].steps:
	
	logging.info("New step: {0} to {1}, duration {2} seconds".format(step.start.coord,step.end.coord, step.duration['value']))
	
	replyTo = tweet.getPreviousID()
	
	mapURL = 'https://www.google.com/maps/dir/{0[0]},{0[1]}/{1[0]},{1[1]}/@{2[0]},{2[1]},14z/am=t/data=4m4!4m3!2m1!1b1!3e0'.format(
		newTrip.start.coord, newTrip.end.coord, step.start.coord)
		
	shortURL = tweet.urlShorten(mapURL)
	
	logging.info("Short URL obtained: {0}".format(shortURL))
	
	if previousInterval >= MINIMUM_TWEET_INTERVAL or int(step.duration['value']) >= MINIMUM_OVERRIDE_DURATION:
		
		logging.info("Tweet permitted for this step.")
		
		previousInterval = int(step.duration['value'])
		stepTweet = 'Driving: {0} '.format(step.asString())
		
		logging.info("Tweet built: {0} | length {1}".format(stepTweet,len(stepTweet)))
		
		if view.checkForView(step.start.coord):
			stepTweet += shortURL
			logging.info("URL added. Tweet length now {0}".format(len(stepTweet)))
			image = view.getViewObject(step.start.coord)
			tweet.makeTweetWithImage(stepTweet, image, replyTo, lat=step.start.coord[0], long=step.start.coord[1])
			logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
			time.sleep(int(step.duration['value']))
			continue
		
		tweet.makeTweet(stepTweet,replyTo=replyTo, lat=step.start.coord[0], long=step.start.coord[1])
		logging.info("Tweet posted. Sleeping for {0} seconds".format(step.duration['value']))
		time.sleep(int(step.duration['value']))
	
	previousInterval = int(step.duration['value'])
	logging.info("Tweet not permitted for this step. Sleeping for {0}".format(step.duration['value']))
	time.sleep(int(step.duration['value']))

time.sleep(60)

signOut = 'Trip complete! {0} traveled. Resting in {1} for a bit.'.format(newTrip.legs[0].distance['text'],newTrip.end.mediumDetail)

replyTo = tweet.getPreviousID()

tweet.makeTweet(signOut,replyTo=replyTo, lat=newTrip.end.coord[0], long=newTrip.end.coord[1])

departurePoint = newTrip.end

logging.info("Departure point reset to {0}. Exiting.".format(departurePoint.coord))
