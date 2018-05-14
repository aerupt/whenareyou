import os
from functools import lru_cache
from dateutil import tz

import requests
import csv
from urllib.parse import quote_plus
from pytz import timezone
from tzwhere import tzwhere
from django.conf.settings import GOOGLE_MAPS_API_KEY
    

LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?key={0}&address={1}'
                '&sensor=false')

tzw = tzwhere.tzwhere()


@lru_cache(None)
def cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


def get_tz(lat, lng):
    tzinfo = tzw.tzNameAt(lat, lng)
    if tzinfo:
        return timezone(tzinfo)
    else:
        return None


def whenareyou(address):
    latlong = cached_json_get(
        LONG_LAT_URL.format(GOOGLE_MAPS_API_KEY, quote_plus(address))
    )['results'][0]['geometry']['location']

    return get_tz(latlong['lat'], latlong['lng'])


if __name__ == '__main__':
    main()
