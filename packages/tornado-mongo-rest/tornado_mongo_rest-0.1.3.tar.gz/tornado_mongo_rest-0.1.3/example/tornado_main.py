import os
import tornado.ioloop
import tornado.web
from pymongo import MongoClient

from tornado_mongo_rest.handlers import make_rest_endpoint_rule
from example.handlers import TrickHandler

"""
Environment variable containing MongoDB Uri, mainly used in Heroku Dyno platform.
"""
MONGODB_URI_ENV_VAR_NAME = 'MONGODB_URI'

"""
MongoClient compatible MongoDB URI.
"""
MONGODB_URI = os.environ.get(MONGODB_URI_ENV_VAR_NAME,
                             'mongodb://localhost/tricks')

"""
MongoDB Database.
"""
MONGODB_DATABASE = MONGODB_URI.split('/')[-1]

db = MongoClient(host=MONGODB_URI)[MONGODB_DATABASE]


def make_app():
    rest_handlers = make_rest_endpoint_rule('trick', TrickHandler, db)

    return tornado.web.Application(handlers=rest_handlers, debug=True)


if __name__ == "__main__":
    app = make_app()
    app.listen(int(os.environ.get("PORT", 5000)))
    tornado.ioloop.IOLoop.current().start()
