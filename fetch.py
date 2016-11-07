import json
import time
from os import environ
from bson import json_util
import pandas as pd
from pymongo import MongoClient
from twitter import *

def stream_tweets_to_db(collection, no_of_tweets, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET):
    """
        Stream Tweets from the Twitter Streaming API and store it in a MongoDB Collection

        Parameters: 
        collection - The MongoDB Collection to store the tweets in
        no_of_tweets - Number of Tweets to fetch
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET - Twitter API Credentials
    """
    tweet_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
    global i
    i = 0
    while True:
        try:
            for tweet in tweet_stream.statuses.filter(track='USelections'):
                if not tweet or tweet.get("timeout"):
                    continue
                if tweet.get("disconnect") or tweet.get("hangup"):
                    print("WARNING Stream connection lost: %s" % msg)
                    break
                if tweet.get('text'):
                    collection.insert_one(tweet)
                    i += 1
                    if i % 1000 == 0:
                        print "Completed " + str(i) + " iterations"
                if i == no_of_tweets:
                    break
        except Exception as e:
            print "WARNING: Stream connection lost, reconnecting in a sec... " + str((type(e), e))
            time.sleep(1)
        if i == no_of_tweets:
            break
    print "Stream Finished"

def fetch_tweets_from_db(collection):
    """
        Fetch Tweets from the MongoDB Collection(the one used in fetch_tweets)
    """
    print "Downloading Tweets..."
    tweets_from_db = collection.find()[:3000]
    l = list(tweets_from_db)
    tweets_from_db_2 = collection.find()[3001:6000]
    temp = list(tweets_from_db_2)
    l.extend(temp)
    tweets_from_db_3 = collection.find()[6001:]
    temp = list(tweets_from_db_3)
    l.extend(temp)
    return l

def has_image(e):
    """
        Check if the tweet has an image or not. Current only check the 'media' entity list. The new Twitter API has 'extended-media' as well which supports more than just photos 
    """
    return True if 'media' in e['entities'] else False


def get_hashtags_from_tweet(tweet):
    """
        Get Hashtags from a Tweet
    """
    if 'hashtags' in tweet['entities']:
        tags = []
        for tag in tweet['entities']['hashtags']:
            tags.append(tag['text'])
        return tags
    else:
        return None

def get_user_mentions_from_tweet(tweet):
    """
        Get User Mentions from a Tweet
    """
    if 'user_mentions' in tweet['entities']:
        mentions = []
        for user in tweet['entities']['user_mentions']:
            mentions.append(user['name'])
        return mentions
    else:
        return None

def make_dataframe(tweets):
    """
        Convert the Tweets from JSON Structure to a Panda's DataFrame
    """
    print "Converting tweets to a DataFrame Structure"
    tweets_df = pd.DataFrame()
    #   Username
    tweets_df['Handle'] = map(lambda tweet: tweet['user']['screen_name'], tweets)
    #   Full Name
    tweets_df['Name'] = map(lambda tweet: tweet['user']['name'], tweets)
    #   Text of the Tweet
    tweets_df['Text'] = map(lambda tweet: tweet['text'], tweets)
    #   Country of origin
    tweets_df['Country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets)
    #   Text of the hastags in the tweet
    tweets_df['Hashtags'] = map(get_hashtags_from_tweet, tweets)
    #   Type of Tweet: (Retweeted, Original)
    tweets_df['Type'] = map(lambda tweet: 'retweeted' if 'retweeted_status' in tweet else 'original', tweets)
    #   Number of retweets
    tweets_df['Retweeted Count'] = map(lambda tweet: tweet['retweet_count'], tweets)
    #   Number of favorites
    tweets_df['Favorite Count'] = map(lambda tweet: 0 if 'retweeted_status' in tweet else tweet['favorite_count'], tweets)
    #   Twitter Users mentioned in the tweets (using '@')
    tweets_df['User Mentions'] = map(get_user_mentions_from_tweet, tweets)
    #   Mime Type: (text, text+image)
    tweets_df['Mime Type'] = map(lambda e: 'textimage' if has_image(e) else 'text', tweets)
    print "Conversion Finished"
    return tweets_df

if __name__ == '__main__':
    """
        To stream tweets in the background using Heroku: heroku run:detached python fetch.py
    """
    #===    Twitter Credentials
    ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
    CONSUMER_KEY = environ.get('CONSUMER_KEY')
    CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')
    #===
    #   MongoDB URI (hosted on mLab)
    MONGODB_URI = environ.get('MONGODB_URI')
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    #   Collection of tweets
    tweets_collection = db.tweets
    print "Streaming Tweets to DB"
    stream_tweets_to_db(tweets_collection, 5000, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)