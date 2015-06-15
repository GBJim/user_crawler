import pymongo
from pymongo import MongoClient
import operator
import json
from twython import Twython
from twython import TwythonAuthError
from  twython import TwythonRateLimitError
from  twython import TwythonError
import re
import numpy as np
import bisect
import random
from time import sleep
from idCrawler import *




def getUserFrequency():

	client = MongoClient('localhost', 27017)   # Change the IP address
	collection = client['idea']['geo_tweets_2']


	userFrequency = {}
	for tweet in collection.find({"lang": "en"}):
		userID = tweet["user"]["id"]
		userFrequency[userID] = userFrequency.get(userID, 0) + 1

	frequencyList = sorted(userFrequency.items(), key=operator.itemgetter(1), reverse = True)  # This is the data you need
	return frequencyList

def randomSampleUser(frequencyList,n = 1000, lower_bound = 1, upper_bound = 1500):
	userID, frequency = zip(*frequencyList)
	upper_index = bisect.bisect_right(frequency, upper_bound)
	lower_index = bisect.bisect_left(frequency, lower_bound)

	return random.sample(userID[lower_index:upper_index], n)


def loadUsers(path="../../Tweets/regular_userFrequency"):
	frequencyList = json.load(open(path))
	frequencyList = sorted(frequencyList , key=operator.itemgetter(1))
	randomUsers = randomSampleUser(frequencyList)
	print("Users ID Loaded")
	return randomUsers


def writeUsers(tweets, collectionName = "regularUser_en"):
	collection = MongoClient("localhost", 27017)["idea"][collectionName]
	collection.insert(tweets)
	print("{} tweets inserted".format(len(tweets)))





randomUsers = loadUsers()



tweets = []
i = 0
times = 0

for user_id in randomUsers[i:]:
	try:
		i +=1
		print("validated {}".format(times))
		print("trial {}".format(i))
		if userLangDetect(user_id = user_id, threshold = 0.9):
			tweets += getTweets(user_id = user_id)
			times += 1
	except  TwythonAuthError:
		print("Bad Authentication")
	except TwythonRateLimitError:
		print("Fall sleep")
		sleep(300)
	except TwythonError:
		print("404 not found!")
