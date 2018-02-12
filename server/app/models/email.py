"""
This class represents the emails table in the database
"""
import datetime
from lib.util_sqlalchemy import ResourceMixin
from extensions.db import Base
from sqlalchemy import Column, Integer, String, Unicode, DateTime


class Email(ResourceMixin, Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    to = Column(String)
    sender = Column(String)
    message = Column(String)
    status = Column(Integer)
    retry_count = Column(Integer, default=0)
