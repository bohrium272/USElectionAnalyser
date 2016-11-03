from fetch import *
from pymongo import MongoClient
from collections import Counter

# MONGODB_URI = environ.get('MONGODB_URI')
# client = MongoClient(MONGODB_URI)
# db = client.get_default_database()
# tweets_collection = db.tweets
# tweets = fetch_tweets_from_db(tweets_collection)
tweets = fetch_tweets_from_json()
tweets_df = make_dataframe(tweets)

def top_10_hastags():
    hashtags = tweets_df['Hashtags']
    all_hashtags = list()
    for tags in hashtags:
        all_hashtags.extend(tags)
    return [e for e, c in Counter(all_hashtags).most_common(10)]

def get_locations():
    places = tweets_df['Places']
    return places