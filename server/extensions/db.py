from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import MySQLdb

from app.settings import (
    DB_URI, 
    DB_URI_TEST, 
    DB_TEST_ON,
    DB_DEBUG_ON
)

# Initiliaze Database Connection
if DB_TEST_ON:
    db_uri = DB_URI_TEST
else:
    db_uri = DB_URI

db = create_engine(db_uri, echo=DB_DEBUG_ON)
#db.echo = False
Base = declarative_base()
Session = sessionmaker(bind=db)
