from flask import Flask
from flask_restful import Resource, Api
from tmdbv3api import TMDb, Movie
import time
import requests
import requests
import pprint

BT = setup_bittorrent()

@app.route('/movie/download/<movie_id>')
def download_movie(id):
    movie = MovieMetadata(serial, None)
    torrents = rarbg.(movie.serial)
    sorter = GrandTourney()
    torrents = sorter.tourney()
    if is_duplicate(rarbg_metadata):
        return 'we already have this movie or its downloading'
    omdb_metadata = omdb_search(movie.serial)
    movie.set_metadata()rarbg_metadata, omdb_metadata)
    db.add_movie(movie_metadata)
    send_download(movie)


def setup_bittorrent():
    '''setup connection to bittorrent and login'''
    bittorrent = Client('http://localhost:8080/')
    bittorrent.login('pavo', 'buffalo12')
    return bittorrent


def send_download(movie):
    filename = str(movie.title) + ' (' + str(movie.year) + ')'
    print(filename)
    BT.download_from_link(movie.magnet_link, savepath=filename)
    # change downloaded flag


class Rarbg():
    def __init__(self):
        self.token, self.token_time = self.get_token()

    def get_torrents(self, serial):
        if time.time()-self.token_time > 600:
            self.token, self.time = self.get_token()
        payload = {
            'mode': 'search',
            'search_imdb': 'tt' + str(serial),
            'token': self.token
        }
        resp = requests.get('https://torrentapi.org/pubapi_v2.php', params=payload)
        resp = resp.json()
        return _clean_response(resp['torrent_results'])
        
    def _clean_response(self, torrents):
        metadata = []
        for torrent in torrents:
            file_info = torrent['category'].split('/')
            cleaned_metadata = {
                'format': file_info[1],
                'resolution': file_info[2],
                'filename': torrent['filename'],
                'magnet_link': torrent['download']
            }
            metadata.append(cleaned_metadata)
        return metadata

def is_released(serial):
    tmdb = TMDb()
    tmdb.api_key = 'YOUR_API_KEY'
    movie = Movie()
    details = movie.details(serial)
    release_date = get_release_dates(movie_id)
    return release_date < time.time()


class GrandTourney:
    def __init__(self, items, criteria):
        self.items = items
        self.criteria = criteria
    
    def _weeder():
        for item in items:
            if not self._satisfactory(item):
                self.items.pop(item)
    
    def _satisfactory(item):
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

    def tourney():
        _weeder()
        sorted = []
        for item in items:
            for criterion_type, criterion in criteria.items():
                if self._satisfies(item, criteria, criterion_type):
                    sorted.append(item)
        return sorted
    
    def _satisfies(item, criteria, criterion_type):
        if item[criterion_type] == criteria:
            return True
        


class Omdb:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_metadata(serial):
        metadata = omdb.imdb_id(serial)
        return _clean_response(metadata)
    
    def _clean_response(metadata):
        clean_metadata = {
            'title': metadata['title'],
            'image': metadata['poster'],
            'year': metadata['year'],
            'plot': metadata['plot'],
            'runtime': metadata['runtime'],
            'rating': metadata['imdb_rating'],
        }


class MovieMetadata:
    def __init__(self, serial, metadata):
        self.serial = serial
        self.metadata = metadata
    
    def set_metadata(self, omdb, rarbg):
        self.metadata.set_omdb_metadata(omdb)
        self.metadata.set_rarbg_metadata(rarbg)


class Metadata:
    def __init__(self, metadata):
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
            self.title = metadata['title']
            self.image = metadata['image']
            self.year = metadata['year']
            self.plot = metadata['plot']
            self.runtime = metadata['runtime']
            self.rating = metadata['rating']
        
        def set_rarbg_metadata(self, rarbg):
            self.format = rarbg['format']
            self.resolution = rarbg['resolution']
            self.filename = rarbg['filename']
            self.magnet_link = rarbg['magnet_link']
