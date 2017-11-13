import requests
import pprint

serial = '0068646'
payload = {'get_token': 'get_token'}
resp = requests.get('https://torrentapi.org/pubapi_v2.php', params=payload)
resp = resp.json()
pprint.pprint(resp)

token = resp['token']
payload = {'mode': 'search', 'search_imdb': 'tt' + str(serial), 'token': token}
resp = requests.get('https://torrentapi.org/pubapi_v2.php', params=payload)
resp = resp.json()
pprint.pprint(resp)