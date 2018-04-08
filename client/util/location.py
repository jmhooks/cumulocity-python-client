import requests
import json

URL = 'http://freegeoip.net/json'


def get_lat_long():
    r = requests.get(URL)
    j = json.loads(r.text)
    return str(j['latitude']) + ',' + str(j['longitude'])