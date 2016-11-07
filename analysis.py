from fetch import *
from pymongo import MongoClient
from collections import Counter
from pandas import DataFrame

MONGODB_URI = environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
tweets_collection = db.tweets
global tweets 
tweets = fetch_tweets_from_db(tweets_collection)
global tweets_df 
tweets_df = make_dataframe(tweets)
del tweets

def top_10_hashtags():
    """
        Get top 10 Hashtags from a list of all Hashtags.
        Used inbuilt Python Counter to get top 10 hashtags
    """
    hashtags = tweets_df['Hashtags']
    if not hashtags.empty and len(hashtags) > 0:
        all_hashtags = list() 
        for tags in hashtags:
            all_hashtags.extend(tags)
        top10 = {}
        for e, c in Counter(all_hashtags).most_common(10):
            top10[e] = c
        return top10
    else:
        return None

def get_locations():
    """
        Returns a dictionary of Number of tweets from each country
    """
    countries = tweets_df['Country']
    d = dict(Counter(countries))
    return d

def dist_original_vs_retweet():
    """
        Number of original vs retweets.
        Using inbuilt Python Counter
    """
    type = list(tweets_df['Type'])
    return dict(Counter(type))

def dist_fav_on_original_tweets():
    """
        Distibution of favorites on original tweets.
        Calculated number of favorites on tweets by Hillary, Donald and others.
    """
    clinton_original_count = 0
    trump_original_count = 0
    others_original_count = 0
    temp_df = tweets_df[['Handle', 'Favorite Count', 'Type']]
    for i in xrange(temp_df.shape[0]):
        temp = dict(temp_df.iloc[i])
        if temp['Type'] == 'original':
            if temp['Handle'] == 'realDonaldTrump':
                trump_original_count += temp['Favorite Count']
            elif temp['Handle'] == 'HillaryClinton':
                clinton_original_count += temp['Favorite Count']
            else: 
                others_original_count += temp['Favorite Count']
    return {'Hillary': clinton_original_count, 'Trump': trump_original_count, 'Others': others_original_count}

def mime_type_dist():
    """
        Number of text and text + image tweets
    """
    return dict(Counter(list(tweets_df['Mime Type'])))

def database_count():
    """
        Number of tweets in Database
    """
    return {'Count': tweets_collection.count()}

def refresh_data():
    """
        Refetch tweets from the database
    """
    tweets_df = make_dataframe(fetch_tweets_from_db(tweets_collection))