# -*- coding: utf-8 -*-
import logging
from time import sleep
from multiprocessing import Process, Event

from wifi_tools import redis_server
from wifi_tools.channel_hop import (
    ChannelHop,
)
from wifi_tools.attack import (
    GenericAttack,
    WEPAttack,
    AuthenticationAttack
)
from wifi_tools.attack.management import BeaconFloodAttack
from wifi_tools.sniff.analyzer import Analyzer
from wifi_tools.sniff import ProbeRequestFloodSniffer

logger = logging.getLogger(__name__)


class Orchester(Process):

    def __init__(self, access_points, clients, mon_iface=None, offline_pcaps=None):
        Process.__init__(self)
        self.change_channel = Event()
        self.mon_iface = mon_iface
        self.monitors = []
        self.generic_attacks = []
        self.analyzers = []
        self.wep_attacks = []
        self.open_attacks = []
        self.offline_pcaps = offline_pcaps
        if offline_pcaps:
            self.analyzers.append(
                Analyzer(
                    iface=mon_iface,
                    change_channel=self.change_channel,
                    offline_pcaps=offline_pcaps))
        else:
            # we set the default attack as generic_attack
            redis_server.set('current_attack', 'generic_attack')
            redis_server.set('current_channel', 1)
            redis_server.set('stop_analyzer', 'False')
            self.generic_attacks = [GenericAttack(iface=mon_iface), BeaconFloodAttack(iface=mon_iface)]
            self.monitors = [ChannelHop(iface=mon_iface, change_channel=self.change_channel)]
            self.analyzers.append(Analyzer(
                iface=mon_iface,
                change_channel=self.change_channel,
            ))
            self.wep_attacks = [WEPAttack(
                iface=mon_iface,
            )]
            self.open_attacks = [AuthenticationAttack(
                iface=mon_iface,
            )]

        self.target_last_seen = None
        self._init_cleanup()
        self._configure_ttls()
        self._start_threads()

    def _init_cleanup(self):
        for channel in range(1, 14):
            redis_server.delete('last_seen_access_points_{0}'.format(channel))

    def _configure_ttls(self):
        for channel in range(1, 14):
            ttl = redis_server.ttl('last_seen_access_points_{0}'.format(channel)) or 0
            if ttl <= 0:
                logger.debug('Setting expire time on channel {0}'.format(channel))
                redis_server.expire('last_seen_access_points_{0}'.format(channel), 10)

    def _start_threads(self):
        for thread in self.generic_attacks + self.monitors + self.analyzers:
            thread.deamon = True
            thread.start()

    def _normal_mode(self):
        for thread in self.attacks + self.monitors:
            thread.unforce_channel()

    def _attack_mode(self):
        for thread in self.attacks + self.monitors:
            thread.force_channel()

    def swtich_to_target_mode(self):
        pass

    def run(self):
        previous_attack = redis_server.get('current_attack')
        while True and not self.offline_pcaps:
            self._configure_ttls()
            current_attack = redis_server.get('current_attack')
            change_status = current_attack != previous_attack
            previous_attack = current_attack
            if change_status:
                if current_attack == 'beacon_flood':
                    redis_server.set('stop_analyzer', True)
                    flood_analyzer_process = ProbeRequestFloodSniffer(iface=self.mon_iface, change_channel=self.change_channel)
                    flood_analyzer_process.start()
                else:
                    analyzer_process = Analyzer(iface=self.mon_iface, change_channel=self.change_channel)
                    analyzer_process.start()

            sleep(0.1)
            # for thread in self.attacks + self.monitors + self.analyzers:
            #    thread.join()
            #    sleep(0.1)
            # access_point = self._check_queue()
            # now = datetime.now()
            # delta = now - self.target_last_seen
            # if True: #  adelta.seconds > 300:
            #    self._normal_mode()
            # else:
            #    self._attack_mode(access_point.channel)
        # if a target if found, set all interfaces to a specific channel
        # if target was last seen 5 minutes ago, go back to normal mode
        # ejecutar sonido

        # si encuentra open, apuntar todo el mismo channel. inciiar otro thread?

        # si encuentra wep, apuntar todo. iniciar ataque para wep
