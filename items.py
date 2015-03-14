# coding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, String, Column, SmallInteger, Text)


Base = declarative_base()


class ReviewItem(Base):
    __tablename__ = 'review'

    user_id = Column(String(128), primary_key=True)
    service = Column(String(64))
    username = Column(String(64))
    text = Column('text', Text)
    rating = Column('rating', SmallInteger)
    create_date = Column('create_date', Integer)
