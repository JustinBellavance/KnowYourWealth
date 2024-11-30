import os
from sqlmodel import create_engine, Session

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URL = 'sqlite:///' + os.path.join(basedir, '../database/database.db')
engine = create_engine(DATABASE_URL, echo=True)

db = Session(engine)