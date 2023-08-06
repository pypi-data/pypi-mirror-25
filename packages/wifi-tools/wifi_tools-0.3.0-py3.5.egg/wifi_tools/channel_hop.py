import time
import logging
from random import randint
from datetime import datetime
from operator import itemgetter
from collections import Counter
from multiprocessing import Process

from wifi_tools import WiFiProcess
from wifi_tools.utils import switch_channel
from wifi_tools.events import change_channel_signal
from wifi_tools.settings import REDIS_URI, CHANGE_CHANNEL_THRESHOLD
from redis import StrictRedis

logger = logging.getLogger(__name__)


class BaseChannelHop(WiFiProcess):

    def __init__(self, iface, world=False):
        self.iface = iface
        self.world = world
        self.packets = None
        self.timeinterval = None
        self.channel_num = 0
        self.max_channel = 11 if not self.world else 13
        self.index = 0

        super(BaseChannelHop, self).__init__()

    def _pre_run_loop(self):
        self.redis_server = StrictRedis(REDIS_URI)
        self.redis_server.set('current_channel_{0}'.format(self.iface), 1)

    def tick(self):
        iface = self.iface
        force_channel = self.redis_server.get('force_channel_{0}'.format(iface))
        if force_channel:
            force_channel = int(force_channel)
            logger.debug('Using fixed channel {0}'.format(force_channel))
            self.redis_server.set('current_channel_{0}'.format(iface), force_channel)
            self._tick_force_channel(force_channel)
        else:
            self._tick()

    def _tick(self):
        raise NotImplementedError()

    def _tick_force_channel(self, channel):
        raise NotImplementedError()

    def switch_channel(self, channel_num, sleep_time):
        self.redis_server.set('current_channel_{0}'.format(self.iface), channel_num)
        switch_channel(self.iface, str(channel_num), sleep_time)


class RoundRobinChannelHop(BaseChannelHop):

    def _tick_force_channel(self, channel):
        self.switch_channel(channel, 1)

    def _tick(self):
        '''
        First time it runs through the channels it stays on each channel for 5 seconds
        in order to populate the deauth list nicely. After that it goes as fast as it can
        '''

        self.channel_num = self.channel_num + 1
        if self.channel_num > self.max_channel:
            self.channel_num = 1

        self.switch_channel(self.channel_num, 0.05)
        # For the first channel hop thru, do not deauth
        if 0 <= self.index < self.max_channel:
            logger.info('First channel hop thru...sleeping 1 second.')
            time.sleep(1)
        self.index += 1


class FrequencyChannelHop(BaseChannelHop):
    """
        Uses number of access points in each channel to weight which channels are going to
        be more used
    """

    def __init__(self, iface, world=False):
        super(FrequencyChannelHop, self).__init__(iface)
        self.used_channels = []

    def tick(self):
        channel_counter = Counter()
        for channel in range(1, self.max_channel + 1):
            channel_counter[channel] = int(self.redis_server.get('channel_count_{0}'.format(channel)))

        total = sum(channel_counter.values())

        channel_weights = {}
        for channel in range(1, self.max_channel + 1):
            channel_weights[channel] = channel_counter[channel] / float(total or 1)

        channels = sorted(channel_weights.items(), key=itemgetter(1), reverse=True)
        if len(self.used_channels) == self.max_channel:
            self.used_channels = []

        for channel, weight in channels:
            if channel in self.used_channels:
                continue
            if weight < 0.05:
                weight = 0.05
            else:
                weight += 2
            logger.debug('Switching to channel {0} with {1} weight on interface {2}'.format(channel, weight, self.iface))
            self.redis_server.set('current_channel', channel)
            self.switch_channel(channel, weight)
            self.used_channels.append(channel)
            break


class EventChannelHop(BaseChannelHop):
    """
    Uses multiprocess events to switch channels
    """

    def __init__(self, ifaces, world=False):
        super(EventChannelHop, self).__init__(ifaces)
        self.used_channels = []
        self.max_channel = 13

    def _pre_run_loop(self):
        super(EventChannelHop, self)._pre_run_loop()
        for channel in range(1, self.max_channel + 1):
            self.redis_server.delete('access_points_iface_{0}_channel_{1}'.format(self.iface, channel))

    def _tick(self):
        iface = self.iface
        channel_counter = Counter()
        for channel in range(1, self.max_channel + 1):
            channel_counter[channel] = self.redis_server.scard('access_points_iface_{0}_channel_{1}'.format(iface, channel))

        total = sum(channel_counter.values())
        channel_weights = {}
        for channel in range(1, self.max_channel + 1):
            channel_weights[channel] = channel_counter[channel] / float(total or 1)

        logger.info('Channel weights : {0}'.format(channel_weights))
        channels = sorted(channel_weights.items(), key=itemgetter(1), reverse=True)
        if len(self.used_channels) == self.max_channel:
            self.used_channels = []

        for channel, weight in channels:
            if channel in self.used_channels:
                continue
            logger.info('Trying to set channel {0} on interface {1}'.format(channel, iface))
            if total == 0 and weight == 0:
                weight = 10
            else:
                weight = CHANGE_CHANNEL_THRESHOLD * weight
            if weight < 5:
                weight = 0
                if randint(0, 100) > 80:
                    weight = 5

            skip_channel = False
            for interface in self.redis_server.lrange('interfaces', 0, -1):
                print(interface.decode('utf8'))
                if interface.decode('utf8') != self.iface:
                    if channel == self.redis_server.get('current_channel_{0}'.format(interface)):
                        logger.info('Other iface {0} channel {1}. Skipping to next channel on iface {2}'.format(interface, channel, self.iface))
                        skip_channel = True
                        break

            if skip_channel:
                continue

            self.switch_channel(channel, 0)
            self.used_channels.append(channel)
            change_channel_signal.wait(weight)


class TimerProcess(Process):

    def run(self):
        start = datetime.now()
        while True:
            now = datetime.now()
            delta = now - start
            if delta.seconds > CHANGE_CHANNEL_THRESHOLD:
                logger.info('Timeout: change channel')
                start = datetime.now()
                change_channel_signal.set()
                change_channel_signal.clear()
