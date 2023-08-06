# -*- coding: utf-8 -*-
import logging

from redis import StrictRedis

from wifi_tools import WiFiProcess
from wifi_tools.channel_hop import (
    EventChannelHop,
    FrequencyChannelHop,
)
from wifi_tools.settings import (
    DUMP_DIRECTORY,
)
from wifi_tools.attack import (
    DeauthAttack,
    WEPAttack,
    AireplayAttack,
    AireplayWEPAttack,
)
from wifi_tools.settings import REDIS_URI
from wifi_tools.sniff.analyzer import Analyzer, AirodumpAnalyzer
# from wifi_tools.attack.management import BeaconFloodAttack
from wifi_tools.sniff import ProbeRequestFloodSniffer

logger = logging.getLogger(__name__)


class Orchester(WiFiProcess):
    """
         Orchester/Orchesta: Is a large instrumental ensemble, often used in classical music,
         that contains sections of string (violin, viola, cello and double bass), brass, woodwind, and percussion instruments.

         Think of every instrument as a process and let's play music with packtes
    """

    def __init__(self, access_points, clients, dump_directory=DUMP_DIRECTORY, mon_ifaces=None, force_channel=None):
        super().__init__()
        self.mon_ifaces = mon_ifaces
        self.dump_directory = dump_directory
        self.redis_server = StrictRedis(REDIS_URI)
        self.monitors = []
        self.generic_attacks = []
        self.analyzers = []
        self.attacks = []
        self.channel_hops = []
        self.redis_server.delete('interfaces')

        # we set the default attack as generic_attack
        for mon_iface in self.mon_ifaces:
            self.redis_server.lpush('interfaces', mon_iface)
            logger.info('Initializing interface {0}'.format(mon_iface))
            self.redis_server.delete('force_channel_{0}'.format(mon_iface))
            self.redis_server.set('current_channel_{0}'.format(mon_iface), force_channel or 1)
            self.channel_hops.append(
                EventChannelHop(mon_iface),
            )

            self.attacks.append(
                AireplayAttack(
                    iface=mon_iface,
                ))
            self.attacks.append(
                AireplayWEPAttack(
                    iface=mon_iface
                )
            )
            self.analyzers.append(
                AirodumpAnalyzer(
                    iface=mon_iface)
            )

        if force_channel:
            for mon_iface in mon_ifaces:
                self.redis_server.set('force_channel_{0}'.format(mon_iface), force_channel)

        self._init_cleanup()
        self._configure_ttls()
        self._start_processes()

    def _init_cleanup(self):
        for channel in range(1, 14):
            self.redis_server.set('channel_count_{0}'.format(channel), 0)
            self.redis_server.delete('last_seen_access_points_{0}'.format(channel))

    def _configure_ttls(self):
        for channel in range(1, 14):
            ttl = self.redis_server.ttl('last_seen_access_points_{0}'.format(channel)) or -1
            if ttl <= 0:
                logger.debug('Setting expire time on channel {0}'.format(channel))
                self.redis_server.expire('last_seen_access_points_{0}'.format(channel), 10)

    def _start_processes(self):
        for process in self.attacks + self.channel_hops + self.analyzers:
            process.start()

    def shutdown(self):
        for process in self.attacks + self.channel_hops + self.analyzers:
            process.is_alive() and process.terminate()

    def tick(self):
        self._configure_ttls()


class ScapyOrchester(WiFiProcess):
    """
        This class was the original Orchester, however this was discarded since
        scapy was processing only 10% (at most) of the packets.
    """

    def __init__(self, access_points, clients, dump_directory=DUMP_DIRECTORY, mon_ifaces=None, offline_pcaps=None, force_channel=None):
        WiFiProcess.__init__(self)
        self.mon_ifaces = mon_ifaces
        self.dump_directory = dump_directory
        self.redis_server = StrictRedis(REDIS_URI)
        self.monitors = []
        self.generic_attacks = []
        self.analyzers = []
        self.wep_attacks = []
        self.open_attacks = []
        self.offline_pcaps = offline_pcaps
        self.redis_server.set('current_attack', 'generic_attack')
        self.redis_server.set('stop_analyzer', False)
        self.previous_attack = 'generic_Attack'

        for mon_iface in mon_ifaces:
            self.redis_server.set('force_channel_{0}'.format(mon_iface), force_channel)
            self.redis_server.set('current_channel_{0}'.format(mon_iface), force_channel or 1)

        for mon_iface in self.mon_ifaces:
            self.generic_attacks = [
                WEPAttack(
                    iface=mon_iface,
                ),
                # AuthenticationAttack(
                #    iface=mon_iface,
                #    redis_server=self.redis_server,
                # ),
                DeauthAttack(iface=mon_iface),
                # BeaconFloodAttack(iface=mon_iface)
            ]
            for mon_iface in self.mon_ifaces:
                self.monitors = [FrequencyChannelHop(iface=mon_iface)]
            self.analyzers = [
                Analyzer(
                    iface=mon_iface,
                    redis_server=self.redis_server,
                    dump_directory=self.dump_directory,)]

        self.target_last_seen = None
        self._init_cleanup()
        self._configure_ttls()
        self._start_processes()

    def _init_cleanup(self):
        for channel in range(1, 14):
            self.redis_server.set('channel_count_{0}'.format(channel), 0)
            self.redis_server.delete('last_seen_access_points_{0}'.format(channel))

    def _configure_ttls(self):
        for channel in range(1, 14):
            ttl = self.redis_server.ttl('last_seen_access_points_{0}'.format(channel)) or -1
            if ttl <= 0:
                logger.debug('Setting expire time on channel {0}'.format(channel))
                self.redis_server.expire('last_seen_access_points_{0}'.format(channel), 10)

    def _start_processes(self):
        for process in self.generic_attacks + self.monitors + self.analyzers:
            process.start()

    def shutdown(self):
        for process in self.generic_attacks + self.monitors + self.analyzers:
            process.is_alive() and process.terminate()

    def swtich_to_target_mode(self):
        pass

    def tick(self):
        if self.offline_pcaps:
            return
        new_attack = self.redis_server.get('current_attack').decode('utf8')
        self._configure_ttls()

        change_status = self.previous_attack != new_attack
        if change_status:
            logger.info('Detected attack mode change from {0} to {1}'.format(self.previous_attack, new_attack))
            self.previous_attack = new_attack
            self.redis_server.set('current_attack', new_attack)
            if new_attack == 'beacon_flood':
                self.redis_server.set('stop_analyzer', True)
                for mon_iface in self.mon_ifaces:
                    flood_analyzer_process = ProbeRequestFloodSniffer(iface=mon_iface)
                    flood_analyzer_process.start()
            else:
                self.redis_server.set('stop_analyzer', False)
                for mon_iface in self.mon_ifaces:
                    analyzer_process = Analyzer(
                            iface=mon_iface,
                            redis_server=self.redis_server,
                            dump_directory=self.dump_directory)
                analyzer_process.start()
