import simplekml
from wifi_tools import redis_server
from wifi_tools.utils import load_json


def main():
    kml = simplekml.Kml()
    access_points = filter(lambda key: key.startswith('access_point'), redis_server.keys())
    for access_point_key in access_points:
        access_point = load_json(access_point_key)
        name = u'{1} ({0})'.format(access_point['bssid'], access_point['ssid'])
        kml.newpoint(name=name, coords=[(access_point['best_lon'], access_point['best_lat'])])

    kml.save('aps.kml')

if __name__ == '__main__':
    main()
