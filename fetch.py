import ast
import json
import time
from os import environ
from random import randint

import pandas as pd
from pymongo import MongoClient
from numpy.random import randint
from twitter import *


# ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
# CONSUMER_KEY = environ.get('CONSUMER_KEY')
# CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')
# MONGODB_URI = environ.get('MONGODB_URI')
# client = MongoClient(MONGODB_URI)
# db = client.get_default_database()
# tweets_collection = db.tweets

def fetch_tweets(collection, no_of_tweets, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET):
    """
    Fetch Tweets from the Twitter Streaming API and store it in a MongoDB Collection

    Parameters: 
    collection - The MongoDB Collection to store the tweets in
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
                if i == no_of_tweets:
                    break
                if tweet.get('text'):
                    collection.insert_one(tweet)
                    i += 1
                    if i % 1000 == 0:
                        print "Completed " + str(i) + " iterations"
        except Exception as e:
            print "WARNING: Stream connection lost, reconnecting in a sec... " + str((type(e), e))
            time.sleep(1)
        if i == no_of_tweets:
            break
    print "Fetch Finished"


def fetch_tweets_from_db(collection):
    """
    Fetch Tweets from the MongoDB Collection(the one used in fetch_tweets)
    """
    return collection.find()

def fetch_tweets_from_json():
    """
    Fetch Tweets from a JSON file
    For testing purpopses only
    """
    f = open('analysis.json')
    return json.loads(f.read())

def unicode_to_json(e):
    return ast.literal_eval(json.loads(json.dumps(e)))

def get_hashtag_text(e):
    all_hashtags = []
    for tag in e['hashtags']:    
        if 'text' in tag:
            all_hashtags.append(tag['text']) 
    return all_hashtags

def get_user_mentions(e):
    if 'name' in e['user_mentions']:
        return e['user_mentions']['name'] 
    else:
        return None

def get_tweet_type(e):
    if e['is_retweet']:
        return 'retweeted'
    else:
        return 'original'

def has_image(e):
    return True if 'media' in e else False


def df_from_csv():
    df = pd.DataFrame().from_csv('tweets.csv')
    new_df = pd.DataFrame()
    new_df['Handle'] = df['handle']
    new_df['Name'] = df['handle'].apply(lambda e: 'Hillary Clinton' if e == 'HillaryClinton' else 'Donald J. Trump')
    new_df['Text'] = df['text']
    new_df['Country'] = df['place_country']
    entities = list(df['entities'])
    entities = map(unicode_to_json, entities)
    new_df['User Mentions'] = map(get_user_mentions, entities)
    new_df['Hashtags'] = map(get_hashtag_text, entities)
    new_df['Type'] = df.apply(get_tweet_type, axis=1)
    new_df['Retweeted Count'] = randint(100, 10000, df.shape[0])
    new_df['Favorite Count'] = randint(100, 10000, df.shape[0])
    new_df['Mime Type'] = map(lambda e: 'textimage' if has_image(e) else 'text', entities)
    return new_df


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
    tweets_df = pd.DataFrame()
    tweets_df['Handle'] = map(lambda tweet: tweet['user']['screen_name'], tweets)
    tweets_df['Name'] = map(lambda tweet: tweet['user']['name'], tweets)
    tweets_df['Text'] = map(lambda tweet: tweet['text'], tweets)
    tweets_df['Country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets)
    tweets_df['Hashtags'] = map(get_hashtags_from_tweet, tweets)
    tweets_df['Type'] = map(lambda tweet: 'retweeted' if 'retweeted_status' in tweet else 'original', tweets)
    tweets_df['Retweeted Count'] = map(lambda tweet: tweet['retweet_count'], tweets)
    tweets_df['Favorite Count'] = map(lambda tweet: 0 if 'retweeted_status' in tweet else tweet['favorite_count'], tweets)
    tweets_df['User Mentions'] = map(get_user_mentions_from_tweet, tweets)
    return tweets_df