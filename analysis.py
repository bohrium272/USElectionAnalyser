import tweepy
from os import environ
import json
import pandas

class TweetFetcher(tweepy.StreamListener):

    def __init__(self, collection):
        self.collection = collection
        self.count = 0

    def on_data(self, data):
        self.push_to_db(self.collection, data)
        self.count += 1
        print self.count
        if self.count == 15000:
            return False
        return True
    
    def push_to_db(self, collection, data):
        tweet = json.loads(data)
        collection.insert_one(tweet)

    def on_error(self, status):
        print status
    
def fetch_tweets(collection, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET):
    tweet_stream = TweetFetcher(collection)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, tweet_stream)

    stream.filter(track=['USElections'])

def create_data_frame(collection):
    tweets_db = collection.find()
    tweets = pandas.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_db)