from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import settings


Base = declarative_base()

engine = create_engine(settings['DATABASE'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
