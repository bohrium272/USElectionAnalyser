from flask import Flask
from os import environ
from pymongo import MongoClient
import analysis

ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN = '1516282950-fcUr4Sh0xsljfQKuTPcGwzgbEHG0nmfE6BtRwQY'
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
ACCESS_TOKEN_SECRET = 'KiGFtdqowNi1wR27K8D1KQ7LF5oQYKzFYBooS3EZATWnP'
CONSUMER_KEY = environ.get('CONSUMER_KEY')
CONSUMER_KEY = 'SR2i7XpkTDyzwS3hrDfRrFZ87'
CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')
CONSUMER_KEY_SECRET = 'VIeb9fA3h7n7dXyKI7PEWSB78uvZD7DBcU35RDKaj0ZexOWqyi'
MONGODB_URI = environ.get('MONGODB_URI')

app = Flask(__name__)
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
tweets = db.tweets

@app.route('/fetch_tweets', methods=['GET'])
def fetch_tweets():
    return ""


if __name__ == '__main__':
    app.run(debug=True)
    analysis.fetch_tweets(tweets, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET)