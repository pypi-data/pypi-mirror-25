import os
import json
import ntpath
import logging
from time import sleep
from os.path import join
from shutil import copyfile
from multiprocessing import Process
from collections import defaultdict

from redis import StrictRedis
from pyrcrack.scanning import Airodump
from scapy.error import Scapy_Exception
from scapy.all import (
    ARP,
    EAPOL,
    sniff,
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
)

from wifi_tools.iface import (
    mon_mac,
)
from lcubo_helpers import (
    new_directory,
    incremental_filename,
    load_json,
    save_json,
)
from wifi_tools.settings import REDIS_URI, DUMP_DIRECTORY, HANDSHAKE_DUMP
logger = logging.getLogger(__name__)


class ScapyAnalyzer(Process):

    def analize_packet(self, pkt):
        '''
        Look for dot11 packets that aren't to or from broadcast address,
        are type 1 or 2 (control, data), and append the addr1 and addr2
        to the list of deauth targets.
        '''

        # We're adding the AP and channel to the deauth list at time of creation rather
        # than updating on the fly in order to avoid costly for loops that require a lock
        stop = self.redis_server.get('stop_analyzer') == b'True'
        if stop:
            self.stop_process = True
            return

        if pkt.haslayer(Dot11):
            self.signal_strength(pkt)
            # if packet has 802.11 layer
            if pkt.addr1 and pkt.addr2:
                # Check if it's added to our AP list
                if pkt.haslayer(EAPOL) and pkt.type == 2:
                    self.process_authentication_packet(pkt)
                if pkt.haslayer(Dot11WEP):
                    self.process_wep(pkt)
                if pkt.haslayer(Dot11ATIM):
                    pass
                if pkt.haslayer(Dot11Auth):
                    self.process_authorization_request(pkt)
                if pkt.haslayer(Dot11AssoReq) or pkt.haslayer(Dot11AssoResp) or pkt.haslayer(Dot11ReassoResp):
                    self.process_association_request(pkt)
                if pkt.haslayer(Dot11Beacon):
                    self.process_beacon(pkt)
                if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11ProbeReq):
                    self.process_probe_request(pkt)

                # Management = 1, data = 2
                if pkt.type in [1, 2]:
                    self.add_client(pkt)

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

    def process_wep(self, pkt):
        return

    def process_authorization_request(self, pkt):
        return

    def process_association_request(self, pkt):
        return

    def process_beacon(self, pkt):
        access_point = self.add_access_point(pkt)
        self.add_client(pkt)
        if access_point and access_point.get('target', None) == 'True':
            logger.info('Found Target AP!')
            if access_point.get('password'):
                logger.info('Target AP found.')
                self.redis_server.publish('scan', access_point['bssid'])
            else:
                self.redis_server.publish('target', access_point['bssid'])

    def process_probe_request(self, packet):
        network_name = 'Hidden SSID'
        access_point = self.add_access_point(packet)
        if not access_point:
            return
        client = self.add_client(packet)
        # detect if it was a hidden SSID
        if b'\x00' not in packet.info:
            try:
                network_name = packet.info.decode('utf8')
                if access_point['ssid'] == '':
                    logger.debug('Found a hidden ssid {0}'.format(network_name))
                    access_point['ssid'] = network_name
                    access_point['hidden'] = True
                    # we save the access point in case it produces no beacons
                    save_json(self.redis_server, 'access_point_{0}'.format(access_point['bssid']), access_point)
            except UnicodeDecodeError:
                logger.info('Unicode error not fixed: please see issue 2')
                return
        logger.debug(u'Found new probe request {0} on interface {1}'.format(network_name, self.iface))
        probe_ssid = {
            'ssid': network_name,
            'client': client,
            'access_point': access_point['bssid'],
        }
        save_json(self.redis_server, 'ssid_{0}'.format(probe_ssid['client']), probe_ssid)
        self.redis_server.sadd('last_seen_probe_networks', network_name)

    def add_client(self, pkt):
        broadcast_mac = 'ff:ff:ff:ff:ff:ff'
        bssid = pkt.addr3  # bssid

        client_address = pkt.addr1
        if bssid == pkt.addr1 or pkt.addr1 == broadcast_mac:
            client_address = pkt.addr2

        if client_address == broadcast_mac or bssid == broadcast_mac:
            return

        access_point = load_json(self.redis_server, 'access_point_{0}'.format(bssid))
        ap_channel = self._determine_ap_channel(pkt)

        data = {'client_addr': client_address, 'bssid': pkt.addr3, 'channel': ap_channel}
        self.redis_server.publish('client_found', json.dumps(data))

        self.redis_server.sadd('clients_{0}'.format(bssid), client_address)
        ap_channel = ap_channel or access_point.get('channel', None)
        return client_address

    def _determine_crypto(self, packet, capability):
        pkt = packet[Dot11Elt]
        crypto = set()
        while isinstance(pkt, Dot11Elt):
            if pkt.ID == 48:
                crypto.add("WPA2")
            elif pkt.ID == 221 and pkt.info.startswith(b'\x00P\xf2\x01\x01\x00'):
                crypto.add("WPA")
            pkt = pkt.payload
        if not crypto:
            if 'privacy' in capability:
                crypto.add("WEP")
            else:
                crypto.add("OPN")

        return crypto

    def _determine_ap_channel(self, pkt):
        try:
            # Thanks to airoscapy for below
            ap_channel = str(ord(pkt[Dot11Elt:3].info))
            chans = range(1, 12)
            if self.world:
                chans = range(1, 14)
            if int(ap_channel) not in chans:
                logger.info('AP channel {0} not found in {1}. Skipping'.format(ap_channel, chans))
                return
            logger.debug('Detected ap channel {0}'.format(ap_channel))
            if self.iface:
                self.redis_server.incr('iface_{0}_channel_{1}_count'.format(self.iface, ap_channel))
            return ap_channel
        except IndexError:
            logger.debug('Could not detect ap channel')
        except TypeError:
            logger.debug('Could not detect ap channel')
        except Exception as e:
            logger.exception(e)
            return

    def add_access_point(self, pkt):
        # AGREGAR https://github.com/ivanlei/airodump-iv/blob/master/airoiv/airodump-iv.py#L116
        try:
            ssid = pkt[Dot11Elt].info.decode('utf-8')
        except UnicodeError as ex:
            logger.exception(ex)
            return
        logger.debug(u'Detected Access Point with SSID {0}'.format(ssid))
        bssid = pkt[Dot11].addr3
        client_addr = pkt[Dot11].addr1
        if bssid == client_addr:
            client_addr = pkt[Dot11].addr2
        capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                                {Dot11ProbeResp:%Dot11ProbeResp.cap%}").strip()

        crypto = self._determine_crypto(pkt, capability)
        crypto = ','.join(crypto)

        logger.debug('Crypto detected was {0}'.format(crypto))
        if crypto == 'OPN':
            logger.debug('OPEN AP found, broadcasting attack signal')
            self.redis_server.publish('scan_open', bssid)

        ap_channel = self._determine_ap_channel(pkt)
        access_point = load_json(self.redis_server, 'access_point_{0}'.format(bssid))
        data = {'client_addr': client_addr, 'bssid': bssid, 'channel': ap_channel}
        self.redis_server.publish('client_found', json.dumps(data))

        if not access_point:
            logger.debug(u'Detected new Access Point with SSID {0}'.format(ssid))
            access_point = dict(
                bssid=bssid,
            )
        access_point['ssid'] = ssid
        access_point['capability'] = capability
        access_point['crypto'] = crypto
        access_point['channel'] = ap_channel
        save_json(self.redis_server, 'access_point_{0}'.format(bssid), access_point)
        return access_point


class Analyzer(ScapyAnalyzer):

    def __init__(self, iface, redis_server, dump_directory):
        super(Analyzer, self).__init__()
        logger.info('Starting packet analyzer on interface {0}'.format(iface))
        self.redis_server = redis_server
        self.stop_process = False
        self.iface = iface
        self.access_point = None
        self.pkts = []
        self.authentication_packets = defaultdict(list)
        self.dot11_pkts = []
        self.nro_iter = 0
        self.dot11_nro_iter = 0
        self.pcapnum = 0
        self.ignore = ['ff:ff:ff:ff:ff:ff', '00:00:00:00:00:00', '33:33:00:', '33:33:ff:', '01:80:c2:00:00:00', '01:00:5e:']
        self.world = False
        self.redis_server.expire('last_seen_probe_networks', 30)

    def run(self):
        self.mon_MAC = mon_mac(self.iface)
        self.ignore.append(self.mon_MAC)

        sniff(self.iface, prn=self.analize_packet, store=0, stop_filter=self.stop)

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


class AirodumpAnalyzer(Process):

    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.directory = new_directory(DUMP_DIRECTORY)

    def run(self):
        self.redis_server = StrictRedis(REDIS_URI)
        writepath = join(self.directory, incremental_filename(self.directory, 'airodump.save'))
        logger.info('Saving packets to file {0}'.format(writepath))
        self.old_channel = self.redis_server.get('current_channel_{0}'.format(self.iface))

        kwargs = {
            'output-format': 'csv,pcap',
            'channel': self.old_channel,
            'write': writepath
        }
        self.airodump_process = Airodump(self.iface, **kwargs)
        self.airodump_process.start()
        while True:
            self.tick()

    def tick(self):
        new_channel = self.redis_server.get('current_channel_{0}'.format(self.iface))
        writepath = join(self.directory, incremental_filename(self.directory, 'airodump.save'))
        logger.debug('Saving packets to file {0}'.format(writepath))
        force_access_point = self.redis_server.get('force_access_point_{0}'.format(self.iface))

        if self.old_channel != new_channel or force_access_point:
            kwargs = {
                'output-format': 'csv,pcap',
                'channel': new_channel,
                'write': writepath
            }
            self.airodump_process.stop()
            self.airodump_process = Airodump(self.iface, **kwargs)
            self.airodump_process.start()
            self.old_channel = new_channel
        try:
            self.process_tree(self.airodump_process.tree)
            self.process_clients(self.airodump_process.clients)
        except Exception as ex:
            logger.exception(ex)
            logger.error(self.airodump_process.tree)
            logger.error(self.airodump_process.clients)

        sleep(0.5)

    def process_tree(self, tree):
        for bssid, data in tree.items():
            self.save_ap(bssid, data)

    def save_ap(self, bssid, data):
        if data['clients']:
            bssid = data['clients'][0]['BSSID']
        bssid = bssid.lower()
        access_point = load_json(self.redis_server, 'access_point_{0}'.format(bssid))
        if access_point.get('target') == '1':
            data = {'bssid': bssid, 'channel': data['channel']}
            self.redis_server.publish('target_found', json.dumps(data))

        if not access_point:
            logger.info(u'Detected new Access Point with SSID {0}'.format(data['ESSID']))
            access_point = dict(
                bssid=bssid,
            )
        access_point['ssid'] = data['ESSID']
        access_point['authentication'] = data['Authentication']
        access_point['cipher'] = data['Cipher']
        if 'WEP' in data['Cipher']:
            data = {'bssid': bssid, 'channel': data['channel']}
            self.redis_server.publish('wep_found', json.dumps(data))
        access_point['channel'] = data['channel']
        self.redis_server.sadd('access_points_iface_{0}_channel_{1}'.format(self.iface, data['channel']), bssid)
        for client_data in data.get('clients', []):
            client_address = client_data['Station MAC']
            self.redis_server.sadd('clients_{0}'.format(bssid), client_address)
            logger.debug('Publish client {0} info'.format(client_address))
            data = {'client_addr': client_address, 'bssid': bssid, 'channel': data['channel']}
            self.redis_server.publish('client_found', json.dumps(data))

        save_json(self.redis_server, 'access_point_{0}'.format(bssid), access_point)

    def process_clients(self, clients):
        for client in clients:
            station_mac = client[0]
            # first_time_seen = client[1]
            last_time_seen = client[2]
            # power = client[3]
            number_of_packets = client[4]
            bssid =client[5].lower()
            probes = client[6].split(',')
            for probe in probes:
                if not probe:
                    continue
                logger.info('Found probe request {0} on interface {1}'.format(probe, self.iface))
                probe_ssid = {
                    'ssid': probe,
                    'client': station_mac,
                    'access_point': bssid,
                }
                save_json(self.redis_server, 'ssid_{0}'.format(probe_ssid['client']), probe_ssid)
                self.redis_server.sadd('last_seen_probe_networks', probe)

            if bssid.strip() != "(not associated)":
                self.redis_server.sadd('access_point_{0}_client_{1}_last_time_seen'.format(bssid, station_mac), last_time_seen)
                self.redis_server.sadd('clients_{0}'.format(bssid), station_mac)
                self.redis_server.set('client_packets_{0}'.format(station_mac), number_of_packets)
                access_point = load_json(self.redis_server, 'access_point_{0}'.format(bssid))
                if 'channel' not in access_point:
                    logger.error('channel not in access point data')
                    logger.error(access_point)
                if access_point and 'channel' in access_point:
                    data = {'client_addr': station_mac, 'bssid': bssid, 'channel': access_point['channel']}
                    self.redis_server.publish('client_found', json.dumps(data))
