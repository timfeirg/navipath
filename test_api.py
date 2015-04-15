import requests
import json


def test_poi():
    with open('/Users/timfeirg/Documents/navipath/shapefiles/single_poi.geojson') as f:
        poi_location = json.loads(f.read())
    payload = {
        'location': poi_location,

    }


if __name__ == '__main__':
    test_poi()
