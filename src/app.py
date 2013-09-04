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
#import controllers
import helpers
import os
import sys

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
        ]
        tornado.web.Application.__init__(self, app_handlers, **settings)


        self.translator = helpers.Translator(client_id="Immunizer",
                                             client_secret="qRP81ZLwANsnfjKg8MLyzoLla4XG+j288lLSGZq949Y=")
        self.tweetstream = helpers.TweetStream(consumer_key="",
                                               consumer_secret="",
                                               access_key="",
                                               access_secret="")
        self.get_twitter_stream()
    
    @property
    def logging(self) :
        return Settings.logging

    def get_twitter_stream(self):
        def _ensure() :
            id_string = "Setiap orang berhak mendapat pendidikan."
            response = self.translator.translate(lang_from='id', query=id_string)
            print response
        tornado.ioloop.IOLoop.instance().add_callback(_ensure)

 
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    Settings.logging.info("Started immunizer.")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
