import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import handlers
import pymongo
import uuid
import base64
import hashlib
import Settings
import controllers
import helpers
import os
import sys
import threading

from tornado.options import define, options
 
define('port', default=8083, help="run on the given port", type=int)

def random256() :
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
 
class Application(tornado.web.Application):
    def __init__(self):
        self.db = pymongo.Connection()['immunize']
        settings = {
            "template_path":Settings.TEMPLATE_PATH,
            "static_path":Settings.STATIC_PATH,
            "debug":Settings.DEBUG,
            "cookie_secret": Settings.COOKIE_SECRET,
            "root_path": Settings.ROOT_PATH,
            "login_url": "/auth/login/"
        }

        app_handlers = [
            (r'/', handlers.MainHandler),
            (r'/test/?', handlers.MainHandler),
            (r'/tweets/all/?', handlers.AllTweetsHandler)
        ]
        tornado.web.Application.__init__(self, app_handlers, **settings)

        self.tweet_controller = controllers.TweetController(self.db)

        self.translator = helpers.Translator(client_id="Immunizer",
                                             client_secret="qRP81ZLwANsnfjKg8MLyzoLla4XG+j288lLSGZq949Y=")
        self.tweetstream = helpers.TweetStream(consumer_key="KFF5bxzKp4O8Frm7PQ5lLg",
                                               consumer_secret="lPthCjoNKYcMHczVICuFRqdVHr8a85osRJivfQq2g",
                                               access_key="324125277-ljc3saqxszAZzQbqHF8qQMjWjfKRhGE399MBqskO",
                                               access_secret="26yiGFYVP5Sf3it89NSJVW02q1Tc2atYZykApnR0")
        self.get_twitter_stream()
    
    @property
    def logging(self) :
        return Settings.logging

    def get_twitter_stream(self):
        def run_tss_threaded() :
            threading.Thread(target=tweetstream_sub).start()
            
        def tweetstream_sub() :
            self.tweetstream.run(callback=handle_tweet)

        def handle_tweet(status) :
            translation = self.translator.translate(lang_from='id', query=status)
            tweet = self.tweet_controller.create(status=status, translation=translation)
            self.logging.info(tweet.serialize())

        tornado.ioloop.IOLoop.instance().add_callback(run_tss_threaded)

 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    Settings.logging.info("Started immunizer.")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
