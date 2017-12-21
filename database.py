import json
from peewee import Model, TextField, BooleanField, SqliteDatabase


class Database:
    def __init__(self):
        self.movies = SqliteDatabase('movies.db')
    
    def setup(self):
        self.movies.connect()
        self.movies.create_table(Movie)

    def get(self, serial):
        movie = Movie.get(Movie.serial == serial)
        if movie is None:
            return None
        movie = MovieMetadata(movie.serial, json.loads(movie.metadata))
        return movie

    def add(self, movie):
        row = Movie.create(
            serial=movie.serial,
            metadata=json.dumps(movie.metadata)
        )
        row.save()

    def is_duplicate(self, serial):
        db_movie = Movie.select().where(Movie.serial == serial)
        return db_movie is None


class Movie(Model):
    '''movie object for database'''
    serial = TextField()
    metadata = TextField()

    class Meta:
        '''set database for the model'''
        database = DB.movies

class MovieMetadata:
    def __init__(self, serial, metadata):
        self.serial = serial
        self.metadata = {}
    
    def set_metadata(self, omdb, rarbg):
        self.metadata.update(omdb)
        self.metadata.update(rarbg)
    
    def add_metadata(metadata):
        self.metadata.update(metadata)