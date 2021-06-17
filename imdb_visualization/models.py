import os
from neomodel import (StructuredNode, StringProperty, IntegerProperty, FloatProperty, ArrayProperty,
                     StructuredRel, RelationshipTo, RelationshipFrom, config)

# from env var, example: "bolt://neo4j:test@localhost:7687"
config.DATABASE_URL = os.environ["NEO4J_BOLT_URL"]

class ActedIn(StructuredRel):
    role = StringProperty()

class Directed(StructuredRel):
    pass
    
class Created(StructuredRel):
    pass

class Person(StructuredNode):
    name = StringProperty(required=True, unique_index=True)

class Actor(Person):
    acted_in_movies = RelationshipTo("Movie", "ACTED_IN", model=ActedIn)
    shows = RelationshipTo("Show", "ACTED_IN", model=ActedIn)

class Director(Person):
    directed_movies = RelationshipTo("Movie", "DIRECTED", model=Directed)

class Creator(Person):
    shows = RelationshipTo("Show", "CREATED", model=Created)

class ActorAndDirector(Actor, Director):
    pass

class Title(StructuredNode):
    #uid = UniqueIdProperty()
    name = StringProperty(required=True, index=True)
    rating = FloatProperty()
    metascore = IntegerProperty()
    votes = IntegerProperty()
    actors = RelationshipFrom("Actor", "ACTED_IN", model=ActedIn)

class Movie(Title):
    year = IntegerProperty(required=True, index=True)
    length = IntegerProperty()
    certificate = StringProperty()
    genre = ArrayProperty()
    director = RelationshipFrom("Director", "DIRECTED", model=Directed)

class Show(Title):
    year_start = IntegerProperty(required=True, index=True)
    year_end = IntegerProperty()
    creator = RelationshipFrom("Director", "CREATED", model=Created)