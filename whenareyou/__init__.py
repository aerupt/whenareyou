from functools import lru_cache

import requests
from urllib.parse import quote_plus
from pytz import timezone


LONG_LAT_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address={0}'
                '&sensor=false')


@lru_cache(None)
def cached_json_get(url):
    """
    Makes a get to that URL and caches it. Simple right? Oh it also returns the
    JSON as a dict for you already!
    """
    return requests.get(url).json()


def whenareyou(address):
    latlong = cached_json_get(
        LONG_LAT_URL.format(quote_plus(address))
    )['results'][0]['geometry']['location']

    tzinfo = cached_json_get(
        'https://maps.googleapis.com/maps/api/timezone/json?location={0},'
        '{1}&timestamp=0'.format(
            latlong['lat'], latlong['lng']
        )
    )
    return timezone(tzinfo['timeZoneId'])


if __name__ == '__main__':
    main()

