import os
import logging
from datetime import datetime

from collections import defaultdict

import dpkt
from lcubo_helpers import (
    new_directory,
    incremental_filename,
)
from wifi_tools.iface import set_channel
from wifi_tools.utils import (
    mac_addr,
)
from wifi_tools.sniff.analyzer import Analyzer
from wifi_tools.settings import (
    DUMP_DIRECTORY,
    ACTIVITY_LOG
)


logger = logging.getLogger(__name__)


class PcapAnalyzer(Analyzer):
    def __init__(self, redis_server, iface, channel, sniffer):
        super(PcapAnalyzer, self).__init__()
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

    def run(self):
        ticks = 0
        pcap_filename = os.path.join(self.directory, incremental_filename(self.directory, f'pcap_fixed_channel_{self.channel}_iface_{self.iface}.save'))
        pcap_file = open(pcap_filename, 'wb')
        pcapfile = dpkt.pcap.Writer(pcap_file)

        try:
            for timestamp, raw_packet in self.sniffer:
                start = datetime.now()
                try:
                    packet = dpkt.radiotap.Radiotap(raw_packet)
                except dpkt.dpkt.UnpackError as ex:
                    logger.exception(ex)
                    continue
                self.tick(packet)
                pcapfile.writepkt(raw_packet, timestamp)
                end = datetime.now()
                delta = end - start
                total_time = delta.microseconds
                if ticks % 1000 == 0:
                    pcap_file.flush()
                    logger.info(f'Packets per microsecond processed {ticks/total_time}')
                ticks += 1

        except KeyboardInterrupt:
            return

    def process_ies(self, frame):
        encryption_opts = set()
        for ie in frame.ies:
            if ie.id == 221 and ie.data.startswith(b'\x00P\xf2\x01\x01\x00'):
                encryption_opts.add('wpa2')
            if ie.id == 48:
                encryption_opts.add('wpa')
        if frame.capability.privacy:
            encryption = 'wep'
        else:
            encryption = 'open'
        if 'wpa2' in encryption_opts:
            encryption = 'wpa2'
        if 'wpa' in encryption_opts:
            encryption = 'wpa'
        if 'wpa2' and 'wpa' in encryption_opts:
            encryption = 'wpa2 wpa'

        return {
            'encryption': encryption
        }

    def process_beacon_frame(self, packet):
        res = {
        }
        if getattr(packet.data, 'ds', None) is not None:
            res.update({'channel': packet.data.ds.ch})
        res.update(self.process_ies(packet.data))
        if getattr(packet.data, 'ssid', None):
            ssid = packet.data.ssid.data.decode('utf-8')
            res.update({'ssid': ssid})
        return res

    def process_mgmt_frame(self, packet):
        frame = packet.data.mgmt
        dst = mac_addr(frame.dst)
        bssid = mac_addr(frame.bssid)
        src = mac_addr(frame.src)
        return {
            'bssid': bssid,
        }

    def check_client_address(self, dst, src, bssid):
        candidate_client_adr_1 = None
        candidate_client_adr_2 = None
        if dst != 'ff:ff:ff:ff:ff:ff' and dst != bssid:
            candidate_client_adr_1 = [dst]
        if src != bssid:
            candidate_client_adr_2 = [src]

        return candidate_client_adr_1 or candidate_client_adr_2 or []

    def process_data_frame(self, packet):
        frame = packet.data.data_frame
        if not getattr(frame, 'bssid', None):
            return {}
        dst = mac_addr(frame.dst)
        bssid = mac_addr(frame.bssid)
        src = mac_addr(frame.src)

        return {
            'bssid': bssid,
            'clients': self.check_client_address(dst, src, bssid)
        }

    def process_probe_request(self, packet):
        for ie in packet.data.ies:
            probe_name = ie.data
            break
        return [probe_name]

    def tick(self, packet):
        try:
            logger.debug(f'Processing packet on interface {self.iface}')
            data = {}
            if getattr(packet.data,'type', None) is None:
                return
            if packet.data.type == 0:
                data.update(self.process_mgmt_frame(packet))
                if packet.data.subtype == 0:
                    # Association request
                    self.wpa_handshake_state[data['bssid']][3] = 1
                if packet.data.subtype == 1:
                    # Association response
                    logger.info(f'Association response! bssid {data["bssid"]}')
                    self.wpa_handshake_state[data['bssid']][4] = 1
                if packet.data.subtype == 8:
                    data.update(self.process_beacon_frame(packet))
                if packet.data.subtype in [4]:
                    probes = self.process_probe_request(packet)
                    self.process_probe_requests(probes, mac_addr(packet.data.mgmt.src), data['bssid'])
                    return
                if packet.data.subtype in [5]:
                    # probe response. someone is trying to connect and the ap answered
                    self.wpa_handshake_state[data['bssid']][0] = 1
                if packet.data.subtype == 11:
                    # Someone tries to Auth
                    logger.info(f'Auth packet found! {data["bssid"]}')
                    self.wpa_handshake_state[data['bssid']][1] = 1
                if packet.data.subtype == 13:
                    # ACK
                    self.wpa_handshake_state[data['bssid']][2] += 1

            if packet.data.type == 1:
                pass
            if packet.data.type == 2:
                data.update(self.process_data_frame(packet))
                if packet.data.subtype == 0:
                    pass
            if 'bssid' not in data:
                return
            old_data = self.redis_server.hgetall(f'access_point_{data["bssid"]}')
            old_data.update(data)
            data = old_data

            if 'encryption' not in data:
                logger.debug('Could not detect wifi encryption')
            else:
                self.update_stats(data)

            self.process_clients(data)

            clients = data.get('clients', [])
            for client_address in clients:
                client_data = {}
                client_data['client'] = client_address
                client_data['bssid'] = data['bssid']
                logger.debug(f'Found client {client_address}. bssid {data["bssid"]}')
                if not self.in_white_list(data['bssid']):
                    self._attack_bssid(client_data, data.get('channel', None))
            self.save_ap(data)

        except Exception as ex:
            logger.exception(ex)
