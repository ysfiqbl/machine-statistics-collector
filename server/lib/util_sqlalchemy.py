import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.types import TypeDecorator

from extensions.db import Base, Session


class ResourceMixin(object):
    # Keep track when records are created and updated.
    session = Session()
    created_on = Column(DateTime(), default=datetime.datetime.now)
    updated_on = Column(DateTime(), onupdate=datetime.datetime.now)

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        
        self.session.add(self)
        self.session.commit()
        #session.close()

        return self


    def delete(self):
        """
        Delete a model instance.

        :return: db.session.commit()'s result
        """
        self.session.delete(self)
        result = self.session.commit()
        return result


    def close_session(self):
        self.session.close()