from twitter import *
from os import environ
import json
import pandas as pd
import time
import ast
from pymongo import MongoClient

# ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
# CONSUMER_KEY = environ.get('CONSUMER_KEY')
# CONSUMER_KEY_SECRET = environ.get('CONSUMEzR_KEY_SECRET')
# MONGODB_URI = environ.get('MONGODB_URI')

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
        except(TwitterHTTPError, BadStatusLine, URLError, SSLError, socket.error) as e:
            print "WARNING: Stream connection lost, reconnecting in a sec... " + (type(e), e)
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

def temp(e):
    return ast.literal_eval(json.loads(json.dumps(e)))

def temp2(e):
    all_hashtags = []
    for tag in e['hashtags']:    
        if 'text' in tag:
            all_hashtags.append(tag['text']) 
    return all_hashtags

def temp3(e):
    if 'name' in e['user_mentions']:
        return e['user_mentions']['name'] 
    else:
        return None

def temp4(e):
    if e['is_retweet']:
        return 'retweeted'
    else:
        return 'original'

def df_from_csv():
    df = pd.DataFrame().from_csv('tweets.csv')
    new_df = pd.DataFrame()
    new_df['Text'] = df['text']
    new_df['Country'] = df['place_country']
    entities = list(df['entities'])
    entities = map(temp, entities)
    new_df['User Mentions'] = map(temp3, entities)
    new_df['Hashtags'] = map(temp2, entities)
    new_df['Type'] = df.apply(temp4, axis=1)
    new_df['Retweeted Count'] = 100
    new_df['Favorite Count'] = 100
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
# print df_from_csv()
# fetch_tweets(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)