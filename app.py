from flask import Flask, render_template, make_response
from os import environ
from analysis import *
from fetch import *

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/locations', methods=['GET'])
def location_route():
    locations = get_locations()
    response = make_response(json.dumps(locations))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/top_10_hashtags', methods=['GET'])
def hashtags_route():
    hashtags = top_10_hashtags()
    response = make_response(json.dumps(hashtags))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/dist/original_fav', methods=['GET'])
def dist_original():
    dist = dist_fav_on_original_tweets()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/dist/original_retweet', methods=['GET'])
def dist_original_retweet():
    dist = dist_original_vs_retweet()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/dist/mime_type', methods=['GET'])
def dist_mime_type():
    dist = mime_type_dist()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True)

# ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
# CONSUMER_KEY = environ.get('CONSUMER_KEY')
# CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')
# MONGODB_URI = environ.get('MONGODB_URI')
# client = MongoClient(MONGODB_URI)
# db = client.get_default_database()
# tweets_collection = db.tweets

# fetch_tweets(tweets_collection, 5261, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)