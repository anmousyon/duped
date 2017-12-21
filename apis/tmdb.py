import requests


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
