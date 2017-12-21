from flask import Flask
import time
import requests
import pprint
import omdb as omdb1
from peewee import Model, TextField, BooleanField, SqliteDatabase
from qbittorrent import Client

class Bittorrent:
    def __init__(self):
        self.bittorrent = Client('http://localhost:8080/')
        self.bittorrent.login('pavo', 'buffalo12')
    
    def download(self, movie):
        filename = str(movie.metadata.title) + ' (' + str(movie.metadata.year) + ')'
        self.bittorrent.download_from_link(movie.metadata.magnet_link, savepath=filename)


class Rarbg:
    def __init__(self):
        self.token, self.token_time = self._get_token()

    def get_torrents(self, serial):
        if time.time()-self.token_time > 600:
            self.token, self.time = self._get_token()
        payload = {
            'mode': 'search',
            'search_imdb': 'tt' + str(serial),
            'token': self.token
        }
        response = requests.get('https://torrentapi.org/pubapi_v2.php', params=payload)
        decoded_response = response.json()
        return self._clean_response(decoded_response['torrent_results'])
        
    def _clean_response(self, torrents):
        metadata = []
        for torrent in torrents:
            # split the category string to get the format and resolution
            # example: 'Movies/x264/1080' -> ['Movies','x264','1080']
            file_info = torrent['category'].split('/')
            if len(file_info) > 2:
                cleaned_metadata = {
                    'format': file_info[1],
                    'resolution': file_info[2],
                    'filename': torrent['filename'],
                    'magnet_link': torrent['download']
                }
                metadata.append(cleaned_metadata)
        return metadata
    
    def _get_token(self):
        payload = {'get_token': 'get_token'}
        response = requests.get('https://torrentapi.org/pubapi_v2.php', params=payload)
        resp = response.json()
        return response['token'], time.time()


class Tmdb:
    def __init__(self):
        self.api_key = self._load_key()
    
    def _load_key(self):
        with open('tmdb.txt') as file:
            for row in file:
                return row.strip()

    def is_released(self, serial):
        payload = {'api_key': self.api_key,}
        resp = requests.get('https://api.themoviedb.org/3/movie/' + serial + '/release_dates', params=payload)
        resp = resp.json()
        release_dates = resp['results']
        for country in release_dates:
            if country['iso_3166_1'] == 'US':
                for release in country['release_dates']:
                    if release['type'] == 5:
                        date = release['release_date']
                        return self._time_convert(date[:10]) < time.time()
    
    def _time_convert(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))


class Weeder:    
    def weed(self, items):
        for item in items:
            if not self._satisfactory(item):
                self.items.pop(item)
    
    def _satisfactory(self, item):
        if (
                (
                    item['format'] == 'x264' or
                    item['format'] == 'h264'
                 ) and
                (
                    item['resolution'] == '1080' or
                    item['resolution'] == '720'
                )
        ):
            return True
        else:
            return False

    def sort(self, items, criteria):
        sorted = []
        for item in items:
            for criterion_type, criterion in criteria.items():
                if self._satisfies(item, criterion, criterion_type):
                    sorted.append(item)
        return sorted
    
    def _satisfies(self, item, criterion, criterion_type):
        if item[criterion_type] == criterion:
            return True
        else:
            return False


class Omdb:
    def __init__(self):
        self.api_key = self._load_key()
    
    def _load_key(self):
        with open('omdb.txt') as f:
            for row in f:
                return row.strip()

    def get_metadata(self, serial):
        payload = {'apikey': self.api_key, 'i': 'tt' + serial}
        resp = requests.get('http://www.omdbapi.com/', params=payload)
        resp = resp.json()
        return self._clean_response(resp)
    
    def _time_convert(self, date):
        return int(time.mktime(time.strptime(date, '%Y-%m-%d')))
        metadata = omdb1.imdb_id(serial)
        return self._clean_response(metadata)
    
    def _clean_response(self, metadata):
        clean_metadata = {
            'title': metadata['Title'],
            'image': metadata['Poster'],
            'year': metadata['Year'],
            'plot': metadata['Plot'],
            'runtime': metadata['Runtime'],
            'rating': metadata['imdbRating'],
        }
        return clean_metadata


class MovieMetadata:
    def __init__(self, serial, metadata):
        self.serial = serial
        self.metadata = Metadata()
    
    def set_metadata(self, omdb, rarbg):
        pprint.pprint(omdb)
        pprint.pprint(rarbg)
        self.metadata.set_omdb_metadata(omdb)
        self.metadata.set_rarbg_metadata(rarbg)


class Metadata:
    def set_all(self, metadata):
        # add metadata from omdb
        self.title = metadata['title']
        self.image = metadata['image']
        self.year = metadata['year']
        self.plot = metadata['plot']
        self.runtime = metadata['runtime']
        self.rating = metadata['rating']

        # add metadata from rarbg
        self.format = metadata['format']
        self.resolution = metadata['resolution']
        self.filename = metadata['filename']
        self.magnet_link = metadata['magnet_link']

    def set_omdb_metadata(self, omdb):
        # add metadata from omdb
        self.title = omdb['title']
        self.image = omdb['image']
        self.year = omdb['year']
        self.plot = omdb['plot']
        self.runtime = omdb['runtime']
        self.rating = omdb['rating']
    
    def set_rarbg_metadata(self, rarbg):
        self.format = rarbg['format']
        self.resolution = rarbg['resolution']
        self.filename = rarbg['filename']
        self.magnet_link = rarbg['magnet_link']


class Database:
    def __init__(self):
        self.movies = SqliteDatabase('movies.db')
    
    def setup(self):
        self.movies.connect()
        self.movies.create_table(Movie)

    def add(self, movie):
        row = Movie.create(
            serial=movie.serial,
            title=movie.metadata.title,
            image=movie.metadata.image,
            year=movie.metadata.year,
            plot=movie.metadata.plot,
            runtime=movie.metadata.runtime,
            rating=movie.metadata.rating,
            format=movie.metadata.format,
            resolution=movie.metadata.resolution,
            filename=movie.metadata.filename,
            magnet_link=movie.metadata.magnet_link,
            downloaded=False
        )
        row.save()

    def is_duplicate(self, serial):
        db_movie = Movie.select().where(Movie.serial == serial)
        return db_movie is None


BT = Bittorrent()
DB = Database()
OMDB = Omdb()
WEEDER = Weeder()
RARBG = Rarbg()

criteria = {
    'format': 'x264',
    'resolution': '1080'
}

class Movie(Model):
    '''movie object for database'''
    serial = TextField()
    title = TextField()
    image = TextField()
    year = TextField()
    plot = TextField()
    runtime = TextField()
    rating = TextField()
    format = TextField()
    resolution = TextField()
    filename = TextField()
    magnet_link = TextField()
    downloaded = BooleanField()

    class Meta:
        '''set database for the model'''
        database = DB.movies


app = Flask(__name__)


@app.route('/movie/download/<serial>')
def download_movie(serial):
    DB.setup()
    movie = MovieMetadata(serial, None)
    torrents = RARBG.get_torrents(movie.serial)
    WEEDER.weed(torrents)
    torrents = WEEDER.sort(torrents, criteria)
    rarbg_metadata = torrents[0]
    if DB.is_duplicate(serial):
        return 'we already have this movie or its downloading'
    omdb_metadata = OMDB.get_metadata(serial)
    movie.set_metadata(omdb_metadata, rarbg_metadata)
    DB.add(movie)
    BT.download(movie)
    return 'now downloading: ' + movie.metadata.title


