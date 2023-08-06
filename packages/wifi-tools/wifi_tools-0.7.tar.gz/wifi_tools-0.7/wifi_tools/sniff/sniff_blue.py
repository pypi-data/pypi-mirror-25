import time
import logging
from multiprocessing import Process

import bluetooth

#from wifi_tools.sniff.CVE20170785 import exploit

logger = logging.getLogger(__name__)


class BluetoothSniff(Process):

    def __init__(self, redis):
        super().__init__()
        self.redis = redis
        logger.info('Starting bluetooth sniffer.')

    def run(self):
        while True:
            try:
                try:
                    logger.debug('Searching for bluetooth devices')
                    nearby_devices = bluetooth.discover_devices(
                                duration=8, lookup_names=True, flush_cache=True, lookup_class=False)
                except OSError as ex:
                    logger.exception(ex)
                    time.sleep(2)
                    continue
                for addr, name in nearby_devices:
                    logger.info('Found bluetooth device {0} with name {1}'.format(addr, name))
                    if self.redis.sadd('session_bt_devices', addr):
                        self.redis.hincrby('session_stats', 'bt')
                    bluetooth_device = {
                        'name': name,
                    }
                    position = self.redis.hgetall('position')
                    services = bluetooth.find_service(address=addr)
                    if position:
                        bluetooth_device.update(position)
                    if services:
                        bluetooth_device.update({'services': services})
                    self.redis.hmset('bluetooth_{0}'.format(addr.upper()), bluetooth_device)
                    #try:
                    #    exploit(addr)
                    #except Exception as ex:
                    #    logger.exception(ex)

                time.sleep(0.5)
            except KeyboardInterrupt:
                break



if __name__ == '__main__':
    from redis import StrictRedis
    redis = StrictRedis()
    bsniff =BluetoothSniff(redis)
    bsniff.start()
