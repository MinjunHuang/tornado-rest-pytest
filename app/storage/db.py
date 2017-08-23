# Python
import binascii
import hashlib
import datetime

# SQLAlchemy
from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Index, Integer, LargeBinary, Numeric, String, Table,
                        Text, UniqueConstraint, text)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

def init_db(engine):
    Base.metadata.create_all(bind=engine)

def now():
    return datetime.datetime.now(tz=pytz.utc)


class EmailEmail(Base):
    __tablename__ = 'email_email'

    id = Column(Integer, primary_key=True)
    body = Column(String(500), nullable=False, unique=True)
