import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
import os
import uuid
import pymongo
import json
 
from tornado.options import define, options
 
class BaseHandler(tornado.web.RequestHandler):
    @property
    def logging(self) :
        return self.application.logging
    @property
    def db(self) :
        return self.application.db
    @property
    def tweet_controller(self) :
        return self.application.tweet_controller
    def return_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(tornado.escape.json_encode(data))

class MainHandler(BaseHandler):
    def get(self):
        self.write('Hello, world!')
        self.finish()

class AllTweetsHandler(BaseHandler) :
    def get(self) :
        all_tweets = [{'status' : t.status,
                       'translation' : t.translation }
                      for t in self.tweet_controller.all()]
        self.return_json(all_tweets)
