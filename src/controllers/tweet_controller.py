
from models import Tweet
from datetime import datetime

class TweetController(object) :
    def __init__(self, db=None) :
        self.db = db
    def create(self, status=None, translation=None) :
        tweet = Tweet(status=status,
                      translation=translation,
                      time=datetime.utcnow())
        self.db.tweets.insert(tweet.serialize())
        return tweet
    def all(self) :
        r = self.db.tweets.find()
        return [Tweet.deserialize(**d) for d in r]
