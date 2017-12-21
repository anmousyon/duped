import requests


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