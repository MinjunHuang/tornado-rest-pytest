import tornado.web
import sqlalchemy

from app.storage import db
from app.urls import urls
from sqlalchemy.orm import scoped_session, sessionmaker



class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings = kwargs
       
        # setup sql database connection
        engine = sqlalchemy.create_engine(kwargs['database'])
        db.metadata.create_all(engine)
        self.database_engine = scoped_session(sessionmaker(bind=engine))


def create_application(**options):
    return Application(urls, **options)