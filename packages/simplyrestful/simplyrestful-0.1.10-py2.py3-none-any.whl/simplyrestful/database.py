from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from settings import settings


Base = declarative_base()

print 'Using database: {}'.format(settings['DATABASE'])

engine = create_engine(settings['DATABASE'])
Base.metadata.bind = engine
DBSession = scoped_session(sessionmaker(bind=engine))
session = DBSession()
