from fetch import *
from pymongo import MongoClient
from collections import Counter
from pandas import DataFrame
# MONGODB_URI = environ.get('MONGODB_URI')
# client = MongoClient(MONGODB_URI)
# db = client.get_default_database()
# tweets_collection = db.tweets
# tweets = fetch_tweets_from_db(tweets_collection)
# tweets = fetch_tweets_from_json()
# tweets_df = make_dataframe(tweets)
tweets_df = df_from_csv()
def top_10_hashtags():
    hashtags = tweets_df['Hashtags']
    if not hashtags.empty and len(hashtags) > 0:
        all_hashtags = list() 
        for tags in hashtags:
            all_hashtags.extend(tags)
        # return [{e:c} for e, c in Counter(all_hashtags).most_common(10)]
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
    return dict(Counter(countries))

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

def dist_original_tweets():
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

# print get_locations()
# # print popularity()
# print top_10_hashtags()
# print dist_original_tweets()
# print dist_original_vs_retweet()