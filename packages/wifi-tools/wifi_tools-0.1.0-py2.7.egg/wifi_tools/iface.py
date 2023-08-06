import re
import os
import sys
import fcntl
import struct
import socket
import logging

from subprocess import Popen, PIPE
from wifi_tools import (
    DN,
)

logger = logging.getLogger(__name__)


def iwconfig():
    monitors = []
    interfaces = {}
    try:
        proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
    except OSError as ex:
        logging.exception(ex)
        sys.exit('Could not execute "iwconfig"')
    for line in proc.communicate()[0].split('\n'):
        if len(line) == 0:
            continue  # Isn't an empty string
        if line[0] != ' ':  # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search:  # Isn't wired
                iface = line[:line.find(' ')]  # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    return monitors, interfaces


def get_iface(interfaces):
    scanned_aps = []

    if len(interfaces) < 1:
        logger.info('No wireless interfaces found, bring one up and try again')
        sys.exit('No wireless interfaces found, bring one up and try again')
    if len(interfaces) == 1:
        for interface in interfaces:
            yield interface

    # Find most powerful interface
    for iface in interfaces:
        count = 0
        proc = Popen(['iwlist', iface, 'scan'], stdout=PIPE, stderr=DN)
        for line in proc.communicate()[0].split('\n'):
            if ' - Address:' in line:  # first line in iwlist scan for a new AP
                count+= 1
        scanned_aps.append((count, iface))
        logger.info('Networks discovered by {0}:{1}'.format(iface, count))
    try:
        interface = max(scanned_aps)[1]
        yield interface
    except Exception as e:
        logging.exception(e)
        for iface in interfaces:
            interface = iface
            logger.info('Minor error: {0}'.format(e))
            logger.info('Starting monitor mode on {0}'.format(interface))
            yield interface


def start_mon_mode(interface):
    logger.info('Starting monitor mode off {0}'.format(interface))
    try:
        os.system('ifconfig %s down' % interface)
        os.system('iwconfig %s mode monitor' % interface)
        os.system('ifconfig %s up' % interface)
        return interface
    except Exception:
        sys.exit('Could not start monitor mode')


def remove_mon_iface(mon_iface):
    logger.info('Removing mon interface {0}'.format(0))
    os.system('ifconfig %s down' % mon_iface)
    os.system('iwconfig %s mode managed' % mon_iface)
    os.system('ifconfig %s up' % mon_iface)


def get_ifaces(args):
    monitors, interfaces = iwconfig()
    mon_iface = None
    if args.interface:
        mon_iface = args.interface

    if mon_iface and mon_iface in monitors:
        logger.info('User provided mon interfaces {0}'.format(mon_iface))
        # if mon_iface not in monitors:
        #    raise Exception('Interface {0} not enabled as monitor'.format(mon_iface))
        return [mon_iface]

    if len(monitors) > 0:
        logger.info('Detected {0} interfaces in monitor mode'.format(len(monitors)))
        if not mon_iface:
            logger.info('Detected one interface for monitoring')
            mon_iface = monitors[0]

        return monitors

    else:
        # Start monitor mode on a wireless interface
        logger.info('Finding the most powerful interface...')
        interfaces = [interface for interface in get_iface(interfaces)]
        monmode = map(lambda interface: start_mon_mode(interface), interfaces)
        logger.info('Interfaces enabled in monitor mode: {0}'.format(monmode))
        return monmode


def mon_mac(mon_iface):
    '''
    http://stackoverflow.com/questions/159137/getting-mac-address
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', mon_iface[:15]))
    mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    logger.info('Monitor mode: {0}-{1}'.format(mon_iface, mac))
    return mac
