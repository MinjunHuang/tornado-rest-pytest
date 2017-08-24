# Python
import binascii
import hashlib
import datetime
import pytz

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
    sender = Column(String(50), nullable=False)
    receiver = Column(String(50), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(String(500), nullable=False)
    send_time = Column(DateTime, default=now())
    receive_time = Column(DateTime, default=now())


class ArchiveEmail(Base):
    __tablename__ = 'archive_email'

    id = Column(Integer, primary_key=True)
    email_id = Column(Integer, nullable=False)
    bury_email_id = Column(Integer, nullable=False)
