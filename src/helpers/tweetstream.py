import sys
import tweepy

class TweetStream(object) :
    def __init__(self, consumer_key=None, consumer_secret=None, access_key=None, access_secret=None):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(auth)
    def run(self):
        sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
        sapi.filter(track=['curiosity'])

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

