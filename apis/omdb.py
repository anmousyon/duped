import requests 


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