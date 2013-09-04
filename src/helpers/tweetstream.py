import sys
import tweepy

class TweetStream(object) :
    all_terms = ['haram', 'halal', 'alcohol', 'alkohol', 'miras', 'minuman keras', 'rokok', 'kretek', 'merokok', 'adhmadiyah', 'admadiyah', 'ahmadiah', 'shia', 'syiah', 'shiah', 'sesat', 'lady gaga', 'porno', 'polygamy', 'pollgami', 'poligami', 'imunsasi', 'vaksin', 'vaksinisasi', 'immunization']
    def __init__(self, consumer_key=None, consumer_secret=None, access_key=None, access_secret=None):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(self.auth)
    def run(self, callback=None):
        sapi = tweepy.streaming.Stream(self.auth, HaramStreamListener(callback=callback))
        sapi.filter(track=self.all_terms,locations=[94.97,-11.00,141.01,10.61])

class HaramStreamListener(tweepy.StreamListener):
    all_terms = ['haram', 'halal', 'alcohol', 'alkohol', 'miras', 'minuman keras', 'rokok', 'kretek', 'merokok', 'adhmadiyah', 'admadiyah', 'ahmadiah', 'shia', 'syiah', 'shiah', 'sesat', 'lady gaga', 'porno', 'polygamy', 'pollgami', 'poligami', 'imunsasi', 'vaksin', 'vaksinisasi', 'immunization']
    haram_terms = ['haram', 'halal']

    def __init__(self, callback=None) :
        self.callback = callback
        super(HaramStreamListener, self).__init__()

    def on_status(self, status):
        country = getattr(status.place, 'country', '').lower()
        country_code = getattr(status.place, 'country_code', '').lower()
        if country != 'indonesia' and country_code != 'id' :
            return
        status = " ".join(status.text.split()).lower() # Normalize tweet
        status = status.encode('ascii', errors='ignore')
        if self.is_tweet_of_interest(status) :
            self.callback(status)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def is_tweet_of_interest(self, status) :
        return self.is_alcohol_tweet(status) or self.is_tobacco_tweet(status) or self.is_adhmadiyah_tweet(status) or self.is_shia_tweet(status) or self.is_gaga_tweet(status) or self.is_polygamy_tweet(status) or self.is_immunization_tweet(status)

    alcohol_terms = ['alcohol', 'alkohol', 'miras', 'minuman keras']

    def is_alcohol_tweet(self, status) :
        has_alcohol_term = False
        for at in self.alcohol_terms :
            if at in status :
                has_alcohol_term = True
                break
        if has_alcohol_term:
            for ht in self.haram_terms :
                if ht in status :
                    return has_alcohol_term
        return False

    tobacco_terms = ['rokok', 'kretek', 'merokok']

    def is_tobacco_tweet(self, status) :
        has_tobacco_term = False
        for at in self.tobacco_terms :
            if at in status :
                has_tobacco_term = True
                break
        if has_tobacco_term :
            for ht in self.haram_terms :
                if ht in status :
                    return has_tobacco_term
        return False

        
    def is_adhmadiyah_tweet(self, status) :
        return 'adhmadiyah' in status or 'admadiyah' in status or 'ahmadiah' in status

    def is_shia_tweet(self, status) :
        return ('shia' in status or 'syiah' in status or 'shiah' in status) and ('sesat' in status)

    def is_gaga_tweet(self, status) :
        return 'lady gaga' in status

    def is_polygamy_tweet(self, status) :
        return 'polygamy' in status or 'pollgami' in status or 'poligami' in status

    def is_immunization_tweet(self, status) :
        return 'imunisasi' in status or 'vaksin' in status or 'vaksinisasi' in status
