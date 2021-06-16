import os
from neomodel import from neomodel import StructuredNode, StringProperty, IntProperty, FloatProperty, 
                                          StructuredRel, RelationshipTo, RelationshipFrom, config

config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class Actor(Person):
    pass

class Director(Person):
    pass

class Creator(Person):
    pass

class Title(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    rating = FloatProperty()

class Movie(Title):
    year = IntProperty(required=True)

class Show(Title):
    year_start = IntProperty(required=True)
    year_end = IntProperty()

class ActedIn(StructuredRel):
    uid = UniqueIdProperty()
    role = StringProperty()

class Directed(StructuredRel):
    uid = UniqueIdProperty()
    
class Created(StructuredRel):
    uid = UniqueIdProperty()