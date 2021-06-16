import os
from neomodel import (StructuredNode, StringProperty, IntegerProperty, FloatProperty,
                     StructuredRel, RelationshipTo, RelationshipFrom, config)

# from env var, example: "bolt://neo4j:test@localhost:7687"
config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

class ActedIn(StructuredRel):
    #uid = UniqueIdProperty()
    role = StringProperty()

class Directed(StructuredRel):
    #uid = UniqueIdProperty()
    pass
    
class Created(StructuredRel):
    #uid = UniqueIdProperty()
    pass

class Person(StructuredNode):
    #uid = UniqueIdProperty()
    name = StringProperty(required=True, unique_index=True)

class Actor(Person):
    movies = RelationshipTo("Movie", "ACTED_IN", model=ActedIn)
    shows = RelationshipTo("Show", "ACTED_IN", model=ActedIn)

class Director(Person):
    movies = RelationshipTo("Movie", "DIRECTED", model=Directed)

class Creator(Person):
    shows = RelationshipTo("Show", "CREATED", model=Created)

class Title(StructuredNode):
    #uid = UniqueIdProperty()
    name = StringProperty(required=True)
    rating = FloatProperty()
    metascore = IntegerProperty()
    votes = IntegerProperty()
    actors = RelationshipFrom("Actor", "ACTED_IN", model=ActedIn)

class Movie(Title):
    year = IntegerProperty(required=True)
    director = RelationshipFrom("Director", "DIRECTED", model=Directed)

class Show(Title):
    year_start = IntegerProperty(required=True)
    year_end = IntegerProperty()
    creator = RelationshipFrom("Director", "CREATED", model=Created)