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

def top_10_hashtags():
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
    print d
    return d

def popularity():
    """
    Popularity Metric Used:
    *   No. of tweets mentioning only one of the candidates Trump or Hillary have been favorited
    *   
    """
    clinton_count = 0
    trump_count = 0
    popularity_df = tweets_df[['User Mentions', 'Favorite Count']]
    for i in xrange(popularity_df.shape[0]):
        temp = dict(popularity_df.iloc[i])
        mentions = temp['User Mentions']
        if mentions != None and len(mentions) > 0:    
            fav_count = temp['Favorite Count']
            if 'Hillary Clinton' in mentions and 'Donald J. Trump' not in mentions:
                clinton_count += fav_count
            elif 'Donald J. Trump' in mentions and 'Hillary Clinton' not in mentions:
                trump_count += fav_count
    return {'Trump': trump_count, 'Clinton': clinton_count}

def dist_original_vs_retweet():
    type = list(tweets_df['Type'])
    return dict(Counter(type))

def dist_fav_on_original_tweets():
    clinton_original_count = 0
    trump_original_count = 0
    others_original_count = 0
    temp_df = tweets_df[['Handle', 'Favorite Count', 'Type']]
    for i in xrange(temp_df.shape[0]):
        temp = dict(temp_df.iloc[i])
        if temp['Type'] == 'original':
            if temp['Handle'] == 'realDonaldTrump':
                trump_original_count += 1
            elif temp['Handle'] == 'HillaryClinton':
                clinton_original_count += 1
            else: 
                others_original_count += 1
    return {'Hillary': clinton_original_count, 'Trump': trump_original_count, 'Others': others_original_count}

def mime_type_dist():
    return dict(Counter(list(tweets_df['Mime Type'])))

def refresh_data():
    tweets_df = make_dataframe(fetch_tweets_from_db(tweets_collection))