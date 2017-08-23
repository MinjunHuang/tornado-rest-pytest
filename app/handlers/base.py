import json
import tornado.web
from app.storage import db


class RequestHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.database_engine
