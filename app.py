from flask import Flask
from os import environ
from pymongo import MongoClient
import analysis

ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = environ.get('CONSUMER_KEY')
CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')
MONGODB_URI = environ.get('MONGODB_URI')

app = Flask(__name__)
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
tweets = db.tweets

@app.route('/fetch_tweets', methods=['GET'])
def fetch_tweets():
    analysis.fetch_tweets(tweets, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)
    return ""


if __name__ == '__main__':
    app.run(debug=True)