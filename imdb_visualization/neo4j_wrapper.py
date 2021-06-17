from .models import *
from .imdb_data import get_movie_dataframe
from tqdm import tqdm
from neomodel import db
import traceback
import pandas as pd
import json

MOVIE_PROPERTIES = ["name", "year", "rating", "metascore", "votes", "length", "certificate", "genre"]

def insert_from_imdb(pages_number=2,years=[str(i) for i in range(2000,2021)]):
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

def get_nodes_by_years(year_start, year_end):
    df = pd.DataFrame([json.loads(json.dumps(m.__properties__)) for m in Movie.nodes.filter(year__gte=year_start).filter(year__lte=year_end)])
    df.set_index("id", inplace=True)
    return df

def get_top_actors(year_start, year_end, top_num=10):
    results, _ = db.cypher_query("""MATCH (a:Actor)-[rs:ACTED_IN]->(m)
                                    WHERE m.year >= {} AND m.year <= {}
                                    WITH a, count(m) AS movies_num, avg(m.rating) AS avg_rating, avg(m.metascore) AS avg_metascore
                                    RETURN id(a), a.name, movies_num, avg_rating, avg_metascore
                                    ORDER BY movies_num DESC LIMIT {}""".format(year_start, year_end, top_num))
    df = pd.DataFrame(results, columns=["id", "name", "movies_num", "avg_movie_rating", "avg_metascore"])
    df.set_index("id", inplace=True)
    return df

def get_top_directors(year_start, year_end, top_num=10):
    results, _ = db.cypher_query("""MATCH (d:Director)-[rs:DIRECTED]->(m)
                                    WHERE m.year >= {} AND m.year <= {}
                                    WITH d, count(m) AS movies_num, avg(m.rating) AS avg_rating, avg(m.metascore) AS avg_metascore
                                    RETURN id(d), d.name, movies_num, avg_rating, avg_metascore
                                    ORDER BY movies_num DESC LIMIT {}""".format(year_start, year_end, top_num))
    df = pd.DataFrame(results, columns=["id", "name", "movies_num", "avg_movie_rating", "avg_metascore"])
    df.set_index("id", inplace=True)
    return df