import json
from collections import namedtuple
import googlemaps

Coordinates = namedtuple('coordinates', ['longitude', 'latitude'])


def getRegionCoordinates(gmaps: googlemaps.Client, region: str) -> Coordinates:
    # Geocoding an address
    geocode_result = gmaps.geocode(region)

    parsed = json.loads(json.dumps(geocode_result[0]))

    geometry = parsed['geometry']
    longitude = geometry['location']['lng']
    latitude = geometry['location']['lat']

    return Coordinates(longitude = longitude, latitude = latitude)