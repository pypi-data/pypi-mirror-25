# -*- coding: utf-8 -*-
import logging
import operator

from redis import StrictRedis
from pcap import pcap
from wifi_tools import WiFiProcess
from wifi_tools.gps import GPSLogger
from wifi_tools.channel_hop import (
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
from wifi_tools.attack.twin import MITMAttack
from wifi_tools.settings import REDIS_URI
from wifi_tools.sniff.sniff_blue import BluetoothSniff
from wifi_tools.sniff.aircrack import (
    AllChannelsAirodumpAnalyzer,
    FixedChannelAirodumpAnalyzer
)
from wifi_tools.sniff.analyzer import Analyzer

from wifi_tools.sniff import ProbeRequestFloodSniffer
from wifi_tools.sniff.nrf24l01 import NRF24Sniffer

logger = logging.getLogger(__name__)


class Orchester(WiFiProcess):
    """
         Orchester/Orchesta: Is a large instrumental ensemble, often used in classical music,
         that contains sections of string (violin, viola, cello and double bass), brass, woodwind, and percussion instruments.

         Think of every instrument as a process and let's play music with packtes
    """

    def __init__(self, redis_server, access_points, clients, dump_directory=DUMP_DIRECTORY, mon_ifaces=None, force_channel=None):
        super().__init__()
        self.redis_server = redis_server
        self.mon_ifaces = mon_ifaces
        self._init_cleanup()
        self.dump_directory = dump_directory
        self.monitors = []
        self.generic_attacks = []
        self.analyzers = []
        self.attacks = []
        self.channel_hops = []
        self.force_channel = force_channel

        # we set the default attack as generic_attack
        logger.info('Initialize strategy processes')
        self.init_strategy()
        if self.force_channel:
            for mon_iface in mon_ifaces:
                self.redis_server.set('force_channel_{0}'.format(mon_iface), self.force_channel)

        logger.info('Clean up redis stats')
        logger.info('Restarting TTLs')
        self._configure_ttls()
        self._start_processes()

    def _init_cleanup(self):
        self.redis_server.delete('interfaces')
        self.redis_server.delete('position')
        self.redis_server.delete('session_probe_requests')
        self.redis_server.delete('session_stats')
        self.redis_server.delete('session_aps')
        self.redis_server.delete('session_bt_devices')
        self.redis_server.set('satellites', 0)
        self.redis_server.hset('session_stats', '4way', 0)
        self.redis_server.hset('session_stats', 'nrf24', 0)
        self.redis_server.hset('session_stats', 'bt', 0)
        self.redis_server.hset('session_stats', 'open', 0)
        self.redis_server.hset('session_stats', 'wep', 0)
        self.redis_server.hset('session_stats', 'wpa', 0)
        self.redis_server.hset('session_stats', 'wpa2', 0)
        self.redis_server.hset('session_stats', 'wpa2 wpa', 0)
        self.redis_server.hset('session_stats', 'attack_count', 0)
        for mon_iface in self.mon_ifaces:
            self.redis_server.delete('session_probe_request_{0}'.format(mon_iface))
            self.redis_server.delete('client_attack_queue_{0}'.format(mon_iface))
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
            logger.info('Starting process {0}'.format(process))
            process.start()

    def shutdown(self):
        for process in self.attacks + self.channel_hops + self.analyzers:
            logger.info('Shutdown process {0}'.format(process))
            process.terminate()

    def tick(self):
        self._configure_ttls()

    def init_strategy(self):
        raise NotImplementedError('Abstract class')


class WarDrivingOrchester(Orchester):

    def init_strategy(self):
        stats = {1: 3042, 6: 2931, 11: 2711, 4: 286, 3: 285, 9: 282, 7: 265, 10: 243, 2: 204, 8: 183, 5: 154, 13: 59, 12: 26, 0: 6, 54: 2, 15: 1, 22: 1, 68: 1, 52: 1}
        stats = sorted(stats.items(), key=operator.itemgetter(1))
        bt_sniffer = BluetoothSniff(self.redis_server)
        bt_sniffer.start()
        nrf24_sniffer = NRF24Sniffer(self.redis_server)
        nrf24_sniffer.start()
        gps_loggger = GPSLogger(self.redis_server)
        gps_loggger.start()
        for index, mon_iface in enumerate(self.mon_ifaces):
            sniffer = pcap(name=mon_iface, promisc=True, immediate=True, timeout_ms=50)
            self.redis_server.lpush('interfaces', mon_iface)
            channel = stats.pop()[0]

            logger.info(f'Starting wardriving analyzer on {mon_iface} on channel {channel}')
            for _ in range(0, 2):
                self.attacks.append(
                    DeauthAttack(iface=mon_iface),
                )
            self.analyzers.append(
                FixedChannelAirodumpAnalyzer(self.redis_server, mon_iface, channel),
            )


class AttackOrchester(Orchester):

    def init_strategy(self):
        for mon_iface in self.mon_ifaces:
            self.redis_server.lpush('interfaces', mon_iface)
            logger.info('Initializing Attack Strategy on interface {0}'.format(mon_iface))
            self.redis_server.delete('force_channel_{0}'.format(mon_iface))
            self.redis_server.set('current_channel_{0}'.format(mon_iface), self.force_channel or 1)

            self.attacks.append(
                AireplayAttack(
                    iface=mon_iface,
                ))
            # self.attacks.append(
            #    AireplayWEPAttack(
            #        iface=mon_iface
            #    )
            #)
            self.analyzers.append(
                AllChannelsAirodumpAnalyzer(
                    iface=mon_iface)
            )
            self.analyzers.append(
                GPSLogger(self.redis_server)
            )


class ConferenceStrategy(Orchester):

    def init_strategy(self):
        """
            This strategy will use interfaces like:
             * one interface will always attack and sense with airodump.
             * one interface will start airbase and will use ether connection for internet.
             * if more interfaces are connected it will use the most comon beacon frame in order
               until all interfaces are used.
        """
        for index, mon_iface in enumerate(self.mon_ifaces):
            if index == 0:
                logger.info('Starting MITMAttack on iface: {0}'.format(mon_iface))
                self.attacks.append(
                    MITMAttack(
                        redis_server=self.redis_server,
                        iface=mon_iface,
                ))
            else:
                logger.info('Starting AllChannelsAirodumpAnalyzer on iface: {0}'.format(mon_iface))
                self.analyzers.append(
                    AllChannelsAirodumpAnalyzer(
                        iface=mon_iface)
                )
                self.attacks.append(
                    AireplayAttack(
                        iface=mon_iface,
                ))
            self.analyzers.append(
                GPSLogger(self.redis_server)
            )


class ScapyOrchester(WiFiProcess):
    """
        This class was the original Orchester, however this was discarded since
        scapy was processing only 10% (at most) of the packets.
    """

    def __init__(self, access_points, clients, dump_directory=DUMP_DIRECTORY, mon_ifaces=None, offline_pcaps=None, force_channel=None):
        WiFiProcess.__init__(self)
        self.mon_ifaces = mon_ifaces
        self.dump_directory = dump_directory
        self.redis_server = StrictRedis(REDIS_URI, decode_responses=True, charset="utf-8")
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
            self.redis_server.sadd('mon_interfaces', mon_iface)

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
        self.redis_server.delete('mon_interfaces')
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
