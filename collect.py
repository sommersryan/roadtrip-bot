import static, tweet, map

suggestions = tweet.getSuggestions()

if suggestions:

	for suggestion in suggestions:
	
		static.saveSuggestion(suggestion)		

