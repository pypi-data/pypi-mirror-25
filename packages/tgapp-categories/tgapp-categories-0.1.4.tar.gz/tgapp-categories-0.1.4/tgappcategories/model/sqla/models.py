from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase = declarative_base()


class Category(DeclarativeBase):
    __tablename__ = 'tgappcategories_categories'

    _id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(Unicode())
    description = Column(Unicode())