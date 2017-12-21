import requests
import pprint

serial = '0068646'
payload = {'i': 'tt' + serial, 'apikey': 'c5909197'}
resp = requests.get('http://www.omdbapi.com/', params=payload)
resp = resp.json()
pprint.pprint(resp)