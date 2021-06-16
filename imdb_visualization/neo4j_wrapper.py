from .models import *
from .imdb_data import get_movie_dataframe
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from neomodel import db
import traceback

MOVIE_PROPERTIES = ["name", "year", "rating", "metascore", "votes"]

def insert_from_imdb(pages_number=5,years=[str(i) for i in range(2000,2021)]):
    df = get_movie_dataframe(pages_number=pages_number, years=years)
    records = df.to_dict("records")
    movies = []
    actors = []
    directors = []
    #with ThreadPoolExecutor(max_workers=4) as ex:
    #    results = list(tqdm(ex.map(insert_record_to_neo4j, records), total=len(records)))
    for record in tqdm(records):
        insert_record_to_neo4j(record)

        
def insert_record_to_neo4j(record):
    movie_dict = {k: v for (k, v) in record.items() if k in MOVIE_PROPERTIES}
    actors_dict = [{"name": val} for val in record["actors"]]
    director_dict = {"name": record["director"]}
    try:
        movie = Movie.get_or_create(movie_dict)[0]

        for actor in actors_dict:
            temp_actor = Person.nodes.get_or_none(**actor)
            if temp_actor and "Actor" not in temp_actor.labels():
                name = temp_actor.name
                directed_movies = [m for m in temp_actor.directed_movies]
                temp_actor.delete()
                new_actor = ActorAndDirector(name=name).save()
                for m in directed_movies:
                    m.director.connect(new_actor)

        actors = Actor.get_or_create(*actors_dict)
        
        temp_director = Person.nodes.get_or_none(**director_dict)
        if temp_director and "Director" not in temp_director.labels():
            name = temp_director.name
            acted_in_movies = [m for m in temp_director.acted_in_movies]
            temp_director.delete()
            new_director = ActorAndDirector(name=name).save()
            for m in acted_in_movies:
                m.actors.connect(new_director)
            actors = Actor.get_or_create(*actors_dict)

        director = Director.get_or_create(director_dict)[0]

        movie.director.connect(director)
        for actor in actors:
            movie.actors.connect(actor)
    except Exception:
        print(traceback.print_exc())
        print("{}\n{}\n{}\n".format(movie_dict, actors_dict, director_dict))
        print("{}\n{}\n{}\n".format(movie, actors, director))