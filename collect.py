import static, tweet, map, time

suggestions = tweet.getSuggestions()

if suggestions:

	for suggestion in suggestions:
	
		static.saveSuggestion(suggestion)

IDs = [str(item[1].id) for item in suggestions]

IDs.sort()

static.setSinceID(IDs[-1])

time.sleep(7200)