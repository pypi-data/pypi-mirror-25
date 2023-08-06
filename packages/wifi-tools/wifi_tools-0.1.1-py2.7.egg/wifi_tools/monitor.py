import time
import logging
from multiprocessing import Process

from wifi_tools import redis_server
from wifi_tools.utils import switch_channel

logger = logging.getLogger(__name__)


class ChannelHop(Process):

    def __init__(self, iface, change_channel, world=False):
        self.change_channel = change_channel
        self.iface = iface
        self.world = world
        self.packets = None
        self.timeinterval = None
        super(ChannelHop, self).__init__()

    def run(self):
        '''
        First time it runs through the channels it stays on each channel for 5 seconds
        in order to populate the deauth list nicely. After that it goes as fast as it can
        '''
        logger.info('Starting Channel Hop')
        redis_server.set('current_channel', 1)
        channel_num = 0
        max_channel = 11 if not self.world else 13
        index = 0

        while True:
            force_channel = redis_server.get('force_channel_{0}'.format(self.iface))
            if not force_channel:
                channel_num = ((channel_num + 1) % max_channel) + 1
                self.mon_channel = str(channel_num)
            else:
                logger.info('Using fixed channel {0}'.format(force_channel))
                self.mon_channel = force_channel
            self.change_channel.wait()
            logger.debug('Current channel {0}'.format(self.mon_channel))
            redis_server.set('current_channel', self.mon_channel)
            switch_channel(self.iface, str(self.mon_channel))

            index += 1
            time.sleep(0.1)
            # For the first channel hop thru, do not deauth
            if 0 < index < max_channel:
                logger.info('First channel hop thru...sleeping 1 second.')
                time.sleep(1)
                continue
