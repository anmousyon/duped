from flask import Flask request
from flask_restful import Resource Api
from apis.rarbg import Rarbg
from apis.bittorrent import Bittorrent
from apis.omdb import Omdb
from apis.tmdb import Tmdb
from .weeder import Weeder
from .database import Database, Movie, MovieMetadata

BT = Bittorrent()
DB = Database()
OMDB = Omdb()
WEEDER = Weeder()
RARBG = Rarbg()

DB.setup()

app = Flask(__name__)
api = Api(app)

criteria = {
    'format': 'x264',
    'resolution': '1080'
}

class Movies(Resource):
    def get(self, serial):
        movie = DB.get(serial)
        # unserialize the the movie
        return movie
    
    def post(self, serial):
        movie = MovieMetadata(serial, {})
        torrents = RARBG.get_torrents(movie.serial)
        WEEDER.weed(torrents)
        torrents = WEEDER.sort(torrents, criteria)
        rarbg_metadata = torrents[0]
        if DB.is_duplicate(serial):
            return 'we already have this movie or its downloading'
        omdb_metadata = OMDB.get_metadata(movie.serial)
        movie.set_metadata(omdb_metadata, rarbg_metadata)
        DB.add(movie)
        BT.download(movie)
        return 'now downloading: ' + movie.metadata.title

api.add_resource(Movies, '/<string:serial>')

if __name__ == '__main__':
    app.run(debug=True)
