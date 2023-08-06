import re
import logging

from scapy.all import (
    IP
)


logger = logging.getLogger(__name__)


def cookie_catcher(pkt):
    raw = pkt.sprintf('%Raw.load%')
    cookie_info = re.findall('wordpress_[0-9a-fA-F]{32}', raw)
    if cookie_info and 'Set' in raw:
        ip_layer = pkt.getlayer(IP)
        logger.info('Found Cookie {0}->{1}'.format(ip_layer.src, ip_layer.dst))
        return ip_layer.dst, cookie_info[0]
