from flask import Flask, render_template, make_response
from os import environ
from analysis import *
from fetch import *

app = Flask(__name__)
"""
    Index Route
"""
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

"""
    Locations Route
"""
@app.route('/locations', methods=['GET'])
def location_route():
    locations = get_locations()
    response = make_response(json.dumps(locations))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Top 10 Hashtags Route
"""
@app.route('/top_10_hashtags', methods=['GET'])
def hashtags_route():
    hashtags = top_10_hashtags()
    response = make_response(json.dumps(hashtags))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Route for Distribution of Favorites on Original Tweets
"""
@app.route('/dist/original_fav', methods=['GET'])
def dist_original():
    dist = dist_fav_on_original_tweets()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Route for distribution of Originals vs Retweets
"""
@app.route('/dist/original_retweet', methods=['GET'])
def dist_original_retweet():
    dist = dist_original_vs_retweet()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Mime Type Route
"""
@app.route('/dist/mime_type', methods=['GET'])
def dist_mime_type():
    dist = mime_type_dist()
    response = make_response(json.dumps(dist))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Get number of Tweets
"""
@app.route('/number_of_tweets', methods=['GET'])
def tweet_count():
    response = make_response(json.dumps(database_count()))
    response.headers['Content-Type'] = 'application/json'
    return response

"""
    Refreshing the Tweets from the Database
"""
@app.route('/refresh_data', methods=['GET'])
def refresh():
    try:
        refresh_data()
    except Exception as e:
        response = make_response(json.dumps({"Message": "Failed!"}))
        response.headers['Content-Type'] = 'application/json'
        return response
    response = make_response(json.dumps({"Message": "Success!"}))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(debug=True)
