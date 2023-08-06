import os
import ntpath
import logging
from datetime import datetime
from shutil import copyfile
from collections import defaultdict
from io import BytesIO

from scapy.error import Scapy_Exception
from scapy.utils import _RawPcapNGReader
from scapy.all import (
    wrpcap,
    RawPcapReader,
    ARP,
    EAPOL,
    Dot11,
    Dot11Auth,
    Dot11AssoReq,
    Dot11Beacon,
    Dot11ProbeResp,
    Dot11ProbeReq,
    Dot11Elt,
    Dot11WEP,
    Dot11ATIM,
    Dot11AssoResp,
    Dot11ReassoResp,
    RadioTap,
)

from wifi_tools.iface import (
    set_channel
)
from wifi_tools.settings import (
    HANDSHAKE_DUMP
)
from wifi_tools.sniff.analyzer import Analyzer
from wifi_tools.settings import (
    DUMP_DIRECTORY,
    ACTIVITY_LOG
)
from lcubo_helpers import (
    new_directory,
    incremental_filename,
)
logger = logging.getLogger(__name__)


class ScapyAnalyzer(Analyzer):

    def __init__(self, redis_server, iface, channel, sniffer=None):
        super(ScapyAnalyzer, self).__init__()
        set_channel(iface, channel)
        self.redis_server = redis_server
        logger.info(f'Initializing PcapAnalyzer on iface {iface}')
        self.sniffer = sniffer
        self.iface = iface
        self.activity_log = open(ACTIVITY_LOG, 'a')
        self.count = 0
        if not os.path.exists(DUMP_DIRECTORY):
            os.mkdir(DUMP_DIRECTORY)
        self.directory = new_directory(DUMP_DIRECTORY)
        self.channel = channel
        self.wpa_handshake_state = defaultdict(lambda : [0,0,0,0,0])
        logger.info('Starting packet analyzer on interface {0}'.format(iface))
        self.authentication_packets = defaultdict(list)
        self.ignore = [
            'ff:ff:ff:ff:ff:ff',
            '00:00:00:00:00:00',
            '33:33:00:',
            '33:33:ff:',
            '01:80:c2:00:00:00',
            '01:00:5e:'
        ]
        self.wpa_handshake_bssids = set()

    def run(self):
        ticks = 0
        pcap_filename = os.path.join(self.directory, incremental_filename(self.directory, f'pcap_fixed_channel_{self.channel}_iface_{self.iface}.save'))

        try:
            for timestamp, raw_packet in self.sniffer:
                start = datetime.now()
                packet = RadioTap(raw_packet)
                self.tick(packet)
                wrpcap(pcap_filename, packet, append=True)
                end = datetime.now()
                delta = end - start
                total_time = delta.microseconds
                if ticks % 1000 == 0:
                    logger.info(f'Packets per microsecond processed {ticks/total_time}')
                ticks += 1

        except KeyboardInterrupt:
            return

    def tick(self, pkt):
        '''
        Look for dot11 packets that aren't to or from broadcast address,
        are type 1 or 2 (control, data), and append the addr1 and addr2
        to the list of deauth targets.
        '''

        # We're adding the AP and channel to the deauth list at time of creation rather
        # than updating on the fly in order to avoid costly for loops that require a lock
        if pkt.haslayer(Dot11):
            # AGREGAR https://github.com/ivanlei/airodump-iv/blob/master/airoiv/airodump-iv.py#L116
            channel = self._determine_ap_channel(pkt)
            data = {
                'channel': channel
            }
            signal_strength = self.signal_strength(pkt)
            # if packet has 802.11 layer
            if pkt.type == 0:
                data.update(
                    {
                        'bssid': pkt.addr3
                    }
                )
                if pkt.haslayer(Dot11Beacon):
                    data.update(self.process_beacon(pkt))
                    encryption = self._determine_crypto(pkt)
                    data.update(
                        {
                            'encryption': encryption,
                        }
                    )
                    self.update_stats(data)
                if pkt.haslayer(Dot11Auth):
                    print('')
                if pkt.haslayer(Dot11AssoReq) or pkt.haslayer(Dot11AssoResp) or pkt.haslayer(Dot11ReassoResp):
                    print('')
                if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11ProbeReq):
                    data.update(self._process_probe_request(pkt))

            if pkt.type == 1:
                pass

            if pkt.type == 2:
                client_addr = pkt.addr2
                if pkt.addr2 == pkt.addr3:
                    client_addr = pkt.addr1
                data.update(
                    {
                        'bssid': pkt.addr3,
                        'clients': [client_addr],
                    }
                )
                if pkt.haslayer(EAPOL):
                    if pkt.addr3 not in self.wpa_handshake_bssids:
                        self.redis_server.hincrby('session_stats', '4way')
                    self.wpa_handshake_bssids.add(pkt.addr3)
                    #data.update(self.process_authentication_packet(pkt))

            #if pkt.haslayer(Dot11WEP):
            #    self.process_wep(pkt)

            self.process_clients(data)
            clients = data.get('clients', [])
            for client_address in clients:
                client_data = {}
                client_data['client'] = client_address
                client_data['bssid'] = data['bssid']
                logger.debug(f'Found client {client_address}. bssid {data["bssid"]}')
                if not self.in_white_list(data['bssid']):
                    self._attack_bssid(client_data, data.get('channel', None))
            if 'bssid' in data:
                self.save_ap(data)

    def signal_strength(self, pkt):
        try:
            extra = pkt.notdecoded
        except:
            extra = None
        signal_strength = None
        if extra:
            signal_strength = -(256 - ord(extra[-4:-3]))
        logger.debug('Signal Strength {0}'.format(signal_strength))
        return signal_strength

    def process_beacon(self, pkt):
        return {
            'ssid': pkt.info
        }

    def _process_probe_request(self, packet):
        network_name = 'Hidden SSID'
        # detect if it was a hidden SSID
        if b'\x00' not in packet.info:
            try:
                network_name = packet.info.decode('utf8')
            except UnicodeDecodeError:
                logger.info('Unicode error not fixed: please see issue 2')
                return
        logger.debug(u'Found new probe request {0} on interface {1}'.format(network_name, self.iface))
        # bssid is always broadcast sin this is a probe request
        self.process_probe_requests([network_name], packet.addr2, packet.addr3)
        return {}

    def _determine_crypto(self, packet):
        elt = packet[Dot11Elt]
        while isinstance(elt, Dot11Elt):
            if elt.ID == 48:
                return 'wpa2'
            elif elt.ID == 221 and elt.info.startswith(b'\x00P\xf2\x01\x01\x00'):
                return 'wpa'
            elt = elt.payload
        capability = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                                        {Dot11ProbeResp:%Dot11ProbeResp.cap%}").strip()
        if 'privacy' in capability:
            return 'wep'
        else:
            return 'open'

    def _determine_ap_channel(self, pkt):
        try:
            # Thanks to airoscapy for below
            ap_channel = str(ord(pkt[Dot11Elt:3].info))
            logger.debug('Detected ap channel {0}'.format(ap_channel))
            return ap_channel
        except IndexError:
            logger.debug('Could not detect ap channel')
        except TypeError:
            logger.debug('Could not detect ap channel')
        except Exception as e:
            logger.exception(e)
            return

    def stop(self, pkt):
        if self.stop_process:
            logger.info('Stopping Packet analyzer process')
            return True
        return False

    def process_authentication_packet(self, pkt):
        logger.info('Auth packet captured! for AP {0}'.format(pkt.addr3))
        self.authentication_packets[pkt.addr3].append(pkt)

    def process_wep(self, pkt):
        logger.debug('Processing WEP packet')
        client_addr = pkt.addr1
        if client_addr == pkt.addr3:
            client_addr = pkt.addr2
        data = {'client_addr': client_addr, 'bssid': pkt.addr3}
        self.redis_server.publish('wep_found', json.dumps(data))
        if pkt.haslayer(ARP) and pkt.getlayer(ARP).op == 1:
            # arp request
            data = json.dumps({'bssid': pkt.addr3, 'addr1': pkt.getlayer(Dot11).addr2, 'arp': True})
            self.redis_server.publish('wep_found', data)


class OfflineAnalyzer(ScapyAnalyzer):

    def __init__(self, redis_server, dump_directory, offline_pcap):
        super(OfflineAnalyzer, self).__init__()
        self.redis_server = redis_server
        self.offline_pcap = offline_pcap
        self.directory = dump_directory
        self.authentication_packets = defaultdict(list)
        self.world = True
        self.nro_iter = 0
        self.has_possible_handshakes = False
        self.iface = None
        logger.info('Reading file {0}'.format(offline_pcap))

    def run(self):
        if not os.path.isdir(self.offline_pcap):
            try:
                sniff(offline=self.offline_pcap, prn=self.analize_packet, store=0)
                if self.has_possible_handshakes:
                    logger.info('Copying capture file with possible 4-way handshake')
                    filename = ntpath.basename(self.offline_pcap)
                    filepath = os.path.join(HANDSHAKE_DUMP, filename)
                    logger.info('Src {0} dest {1}'.format(self.offline_pcap, filepath))
                    if os.path.isfile(filepath):
                        filepath = incremental_filename(HANDSHAKE_DUMP, filename)
                    copyfile(self.offline_pcap, filepath)
            except Scapy_Exception as ex:
                logger.exception(ex)

    def process_authentication_packet(self, pkt):
        self.authentication_packets[pkt.addr3].append(pkt)
        self.has_possible_handshakes = True
        logger.info('4-way handshake captured! for AP {0}'.format(pkt.addr3))
