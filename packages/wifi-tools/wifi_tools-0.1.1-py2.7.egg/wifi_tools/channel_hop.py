import time
import logging

from wifi_tools.utils import switch_channel
from wifi_tools import WiFiProcess

logger = logging.getLogger(__name__)


class ChannelHop(WiFiProcess):

    def __init__(self, iface, redis_server, world=False):
        self.redis_server = redis_server
        self.iface = iface
        self.world = world
        self.packets = None
        self.timeinterval = None
        force_channel = self.redis_server.get('force_channel_{0}'.format(self.iface))
        self.redis_server.set('current_channel', force_channel or 1)
        self.channel_num = 1
        self.max_channel = 11 if not self.world else 13
        self.index = 0
        self.redis_server.set('current_channel', 1)
        super(ChannelHop, self).__init__()

    def tick(self):
        '''
        First time it runs through the channels it stays on each channel for 5 seconds
        in order to populate the deauth list nicely. After that it goes as fast as it can
        '''
        force_channel = self.redis_server.get('force_channel_{0}'.format(self.iface))
        if not force_channel:
            self.channel_num = self.channel_num + 1
            if self.channel_num > self.max_channel:
                self.channel_num = 1

            self.mon_channel = str(self.channel_num)
        else:
            logger.info('Using fixed channel {0}'.format(force_channel))
            self.mon_channel = force_channel
        # self.change_channel.wait()
        logger.debug('Current channel {0}'.format(self.mon_channel))
        self.redis_server.set('current_channel', self.mon_channel)
        switch_channel(self.iface, str(self.mon_channel))

        time.sleep(0.05)
        # For the first channel hop thru, do not deauth
        if 0 <= self.index < self.max_channel:
            logger.info('First channel hop thru...sleeping 1 second.')
            time.sleep(1)
        self.index += 1
