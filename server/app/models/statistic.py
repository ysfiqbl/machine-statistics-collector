"""
This class represents the statistics table in the database
"""
import datetime
from lib.util_sqlalchemy import ResourceMixin
from extensions.db import Base
from sqlalchemy import Column, Integer, String, Unicode, DateTime


class Statistic(ResourceMixin, Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    response = Column(String)

