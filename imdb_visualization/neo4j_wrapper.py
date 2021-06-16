from .models import *
from .imdb_data import get_movie_dataframe

def insert_from_imdb():
    df = get_movie_dataframe()
    