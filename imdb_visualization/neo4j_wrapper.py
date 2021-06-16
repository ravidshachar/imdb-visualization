from .models import *
from .imdb_data import get_movie_dataframe

MOVIE_PROPERTIES = ["name", "year", "rating", "metascore", "votes"]

def insert_from_imdb():
    df = get_movie_dataframe()
    records = df.to_dict("records")
    movies = []
    actors = []
    directors = []
    for record in records:
        movie_dict = {k: v for (k, v) in record.items() if k in MOVIE_PROPERTIES}
        actors_dict = [{"name": val} for val in record["actors"]]
        director_dict = {"name": record["director"]}
        movie = Movie.get_or_create(movie_dict)[0]
        actors = Actor.get_or_create(*actors_dict)
        director = Director.get_or_create(director_dict)[0]
        movie.director.connect(director)
        for actor in actors:
            movie.actors.connect(actor)