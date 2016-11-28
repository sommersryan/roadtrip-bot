import map, trip, view, tweet, time

while True:
	
	newPlan = map.Plan.random()
	newTrip = trip.Trip.fromPlan(newPlan)
	
	preamble = 'New trip! {0} to {1}, {2}, {3}'.format(newTrip.start.mediumDetail, newTrip.end.mediumDetail, newTrip.legs[0].distance['text'], newTrip.legs[0].duration['text'])
	

