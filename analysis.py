from twitter import TwitterStream, OAuth
from os import environ
import json
import pandas

tweets = []
    
def fetch_tweets(collection, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET):
    print "Inside fetch_tweets"
    tweet_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
    print "Constructed Stream"
    iterator = tweet_stream.statuses.filter(track='USElections')
    print "Iterator Obtained"
    i = 0
    for tweet in iterator:
        if i == 1:
            break
        print json.dumps(tweet)
        collection.insert_one(json.dumps(tweet))
        i += 1 
    print "Iteration Finished"

def create_data_frame(collection):
    tweets_db = collection.find()
    tweets = pandas.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_db)
