import logging
import optparse

from wifi_tools import init_logging
from lcubo_helpers import (
    init_session,
    load_json,
    save_json
)

from tqdm import tqdm

init_logging()

logger = logging.getLogger(__name__)


def import_wigle(redis_server, wigle_database_filename):
    wigle_db_session= init_session(wigle_database_filename)()

    result = wigle_db_session.bind.engine.execute('select * from network')
    count_result = wigle_db_session.bind.engine.execute('select count(*) from network')
    for count in count_result:
        total = count[0]

    for row in tqdm(result, total=total):
        # bssid, ssid, frequency, capabilities, lasttime, lastlat, lastlon, type, bestlevel, bestlat, bestlon
        bssid = row[0]
        ssid = row[1]
        capability = row[3]
        con_type = row[7]
        bestlevel = row[8]
        bestlat = row[9]
        bestlon = row[10]
        if con_type != 'W':
            continue

        access_point = load_json(redis_server, 'access_point_{0}'.format(bssid))
        if access_point:
            access_point['ssid'] = ssid
            access_point['best_lat'] = bestlat
            access_point['best_lon'] = bestlon
            access_point['best_level'] = bestlevel
        else:
            logger.info(u'New Access Point {0} !'.format(ssid))
            access_point = dict(
                    bssid=bssid,
                    ssid=ssid,
                    best_lat=bestlat,
                    best_lon=bestlon,
                    best_level=bestlevel,
                    capability=capability,)
        save_json(redis_server, 'access_point_{0}'.format(bssid), access_point)

if __name__ == '__main__':

    usage = "usage: %prog -d {database_filename}"
    parser = optparse.OptionParser(usage)
    parser.add_option('-d', '--database_filename',
                      type='string',
                      default='wigle.sqlite')
    options, args = parser.parse_args()

    import_wigle(options.database_filename)
