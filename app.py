from flask import Flask, render_template
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

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)