import time
import logging
from multiprocessing import Process

import gpsd
from dateutil import parser

logger = logging.getLogger(__name__)


class GPSLogger(Process):

    def __init__(self, redis):
        self.redis = redis
        gpsd.connect()
        super(GPSLogger, self).__init__()

    def run(self):
        while True:
            try:
                self.tick()
            except KeyboardInterrupt:
                break

    def tick(self):
        try:
            packet = gpsd.get_current()
        except (IndexError, KeyError, UserWarning):
            logger.error('gpsd seems to be not running')
            time.sleep(30)
            gpsd.connect()
            return
        try:
            lat, lng = packet.position()
            position = {
                'lat': lat,
                'lng': lng,
                'datetime': parser.parse(packet.time),
                'satellites': packet.sats
            }
            self.redis.hmset('position', position)
            self.redis.sadd('position_history', position)
            time.sleep(3)
        except gpsd.NoFixError:
            self.redis.set('satellites', packet.sats)
            self.redis.delete('position')
            logger.info(f'No GPS fix. Satellites found {packet.sats}')
            time.sleep(60)


if __name__ == '__main__':
    from redis import StrictRedis
    redis = StrictRedis()
    gps = GPSLogger(redis)
    import ipdb
    ipdb.set_trace()
    gps.tick()
