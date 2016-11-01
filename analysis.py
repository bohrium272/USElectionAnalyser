from twitter import *
from os import environ
import json
import pandas
import time
    
def fetch_tweets(collection, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET):
    print "Inside fetch_tweets"
    tweet_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
    print "Constructed Stream"
    global i
    i = 0
    while True:
        try:
            for tweet in tweet_stream.statuses.filter(track=['USElections', 'USelections', '#USElections', '#USelections']):
                if not tweet or tweet.get("timeout"):
                    continue
                if tweet.get("disconnect") or tweet.get("hangup"):
                    print("WARNING Stream connection lost: %s" % msg)
                    break
                if i == 9400:
                    break
                if tweet.get('text'):
                    collection.insert_one(tweet)
                    i += 1
                    if i % 1000 == 0:
                        print "Completed " + str(i) + " iterations"
        except(TwitterHTTPError, BadStatusLine, URLError, SSLError, socket.error) as e:
            print "WARNING: Stream connection lost, reconnecting in a sec... " + (type(e), e)
            time.sleep(1)
        if i == 9400:
            break
    print "Fetch Finished"

def create_data_frame(collection):
    tweets_db = collection.find()
    tweets = pandas.DataFrame()
    tweets['text'] = map(lambda tweet: tweet['text'], tweets_db)