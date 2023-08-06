from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from tgappcategories.model import DBSession


class Category(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'tgappcategories_categories'
        indexes = [
            ('name',),
        ]

    _id = FieldProperty(s.ObjectId)
    
    name = FieldProperty(s.String)
    description = FieldProperty(s.String)
