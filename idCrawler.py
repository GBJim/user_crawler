from twython import Twython
import re
import json
import numpy as np
from langdetect import detect
from langdetect.detector import LangDetectException


#import pymongo

def getTweets(screen_name=None, user_id=None, num = None):
	consumer_key = "MLGdNZCfmzGthHTAyJU4KFvbU"
	consumer_secret ="Tfp7DIZcJLbnS8BR5CWQmZklrhsbtc3fMfssKPT4SZoYsPiQKw"
	access_token ="2383540880-s2C8xPgA4ITF7QnLRFnHK1es2UEbmW8qHQ87sX5"
	access_token_secret ="kLYgBTPeslLgaFugCx0PoiBpPIKnyCBEVfqqJCkjsSKpP"
	twitter = Twython(consumer_key, consumer_secret,access_token,access_token_secret )

	if screen_name == None:
		tweets = twitter.get_user_timeline(user_id = user_id, count = 200, trim_user = False, include_rts = True  )
	else:
		tweets = twitter.get_user_timeline(screen_name = screen_name, count = 200, trim_user = False, include_rts = True  )

	totalTweets = tweets
	while len(tweets) >= 2:
		max_id = tweets[-1]["id"]
		tweets = twitter.get_user_timeline(screen_name = screen_name, max_id = max_id, count = 200, trim_user = False, include_rts = True)
		if len(tweets) > 1:
			totalTweets += tweets[1:]
	return totalTweets

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

def langDetect(tweets ,lang, threshold, method = "simple"):
	langCount = 0
	if method == "simple":
		for tweet in tweets:
			try:
				if lang == tweet["lang"]:
					langCount += 1
			except LangDetectException:
				pass
	else:
		for tweet in tweets:
			try:
				if lang == detect(tweet["text"]):
					langCount += 1
			except LangDetectException:
				pass
	langRatio = langCount / len(tweets)
	print(langRatio)
	if len(tweets) == 0:
		return False
	else:
		return langRatio > threshold





def userLangDetect(screen_name=None, user_id=None, lang="en", threshold=0.9, num = 100):
	if screen_name == None:
		tweets = getTweets(screen_name=None,user_id=user_id)
	else:
		tweets = getTweets(screen_name)
	return langDetect(tweets,lang,threshold)




if __name__ == '__main__':
	print(userLangDetect(user_id=5402612))
