import os
from functools import lru_cache

import requests
import csv
from urllib.parse import quote_plus
from pytz import timezone


LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}'
                '&sensor=false')

airports_csv_path = os.path.join(os.path.dirname(__file__), 'airports.csv')

airports_dict = {}

with open(airports_csv_path) as csvfile:
    airports_reader = csv.DictReader(
        csvfile,
        fieldnames=['id', 'name', 'city', 'country', 'iata', 'icao', 'lat',
                    'lng', 'alt', 'tz', 'dst', 'tz_olson'],
        restkey='info')
    for row in airports_reader:
        airports_dict[row['iata']] = row


@lru_cache(None)
def cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


def get_tz(lat, lng):
    tzinfo = cached_json_get(
        'https://maps.googleapis.com/maps/api/timezone/json?location={0},'
        '{1}&timestamp=0'.format(
            lat, lng
        )
    )
    return timezone(tzinfo['timeZoneId'])


def whenareyou(address):
    latlong = cached_json_get(
        LONG_LAT_URL.format(quote_plus(address))
    )['results'][0]['geometry']['location']

    return get_tz(latlong['lat'], latlong['lng'])


def whenareyou_apt(airport):
    return timezone(airports_dict[airport]['tz_olson'])


if __name__ == '__main__':
    main()
