from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE


Base = declarative_base()

engine = create_engine(DATABASE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
