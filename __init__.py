import map, trip, view, tweet, time

while True:
	
	newPlan = map.Plan.random()
	newTrip = trip.Trip.fromPlan(newPlan)
	
	preamble = 'New trip! {0} to {1}. {2}, {3}'.format(newTrip.start.mediumDetail, newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'])
	
	tweet.makeTweet(preamble)
	
	time.sleep(60)
	
	for step in newTrip.legs[0].steps:
		
		stepTweet = 'Driving: {0}'.format(step.asString())
		
		if view.checkForView(step.start.coord):
			
			image = view.getViewObject(step.start.coord)
			tweet.makeTweetWithImage(stepTweet,image)
			time.sleep(int(step.duration['value']))
			continue
		
		tweet.makeTweet(stepTweet)
	
	time.sleep(60)
	
	signOut = 'Trip complete! Resting in {0} for a bit.'.format(newTrip.start.mediumDetail)
	
	time.sleep(14400)