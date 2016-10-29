import tweepy
from os import environ
import json

ACCESS_TOKEN = environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = environ.get('ACCESS_TOKEN_SECRET')
CONSUMER_KEY = environ.get('CONSUMER_KEY')
CONSUMER_KEY_SECRET = environ.get('CONSUMER_KEY_SECRET')

class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        print data 
        return True
    
    def on_error(self, status):
        print status
    
if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = tweepy.Stream(auth, l)

    stream.filter(track=['USElections'])