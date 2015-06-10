from twython import Twython
import re
import json
import numpy as np
from langdetect import detect

#import pymongo

def getTweets(screen_name, num = None):
	consumer_key = "MLGdNZCfmzGthHTAyJU4KFvbU"
	consumer_secret ="Tfp7DIZcJLbnS8BR5CWQmZklrhsbtc3fMfssKPT4SZoYsPiQKw"
	access_token ="2383540880-s2C8xPgA4ITF7QnLRFnHK1es2UEbmW8qHQ87sX5"
	access_token_secret ="kLYgBTPeslLgaFugCx0PoiBpPIKnyCBEVfqqJCkjsSKpP"
	twitter = Twython(consumer_key, consumer_secret,access_token,access_token_secret )



	totalTweets = []
	
	if num == None:
		tweets = twitter.get_user_timeline(screen_name = screen_name, count = 200, trim_user = True, include_rts = False  )
		while len(tweets) >= 2:
			max_id = tweets[-1]["id"]
			tweets = twitter.get_user_timeline(screen_name = screen_name, max_id = max_id, count = 200, trim_user = True, include_rts = False)
			
			if len(tweets) > 1:
				totalTweets += tweets[1:]
		return totalTweets
	else:
		count = num if num < 200 else 200
		tweets = twitter.get_user_timeline(screen_name = screen_name, count = count, trim_user = True, include_rts = False  )
		while len(tweets) >= 2 and len(tweets) < num:
			max_id = tweets[-1]["id"]
			tweets = twitter.get_user_timeline(screen_name = screen_name, max_id = max_id, count = 200, trim_user = True, include_rts = False)
			
			if len(tweets) > 1:
				totalTweets += tweets[1:]
		return totalTweets[:num]

def userLangDetect(tweets, lang="en", threshold=0.95):
	langCount = 0
	for tweet in tweets:
		if lang == detect(tweet["text"]):
			langCount += 1
	langRatio = langCount / len(tweets)
	return langRatio > threshold
	


#collection = pymongo.MongoClient().idea.BDP_tweets
candidates = []  #fill in the ids you need to crawl
#candidates = json.load(open("BDP_candidates.json"))

tweets = []

for screen_name in candidates:
	tweets += getTweets(screen_name)
	print(screen_name + "is done!")

