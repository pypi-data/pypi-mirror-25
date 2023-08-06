import re
import os
import sys
import fcntl
import struct
import socket
import random
import logging

from subprocess import Popen, PIPE
from wifi_tools import (
    DEV_NULL,
)
from wifi_tools.settings import (
    IWCONFIG_COMMAND_PATH,
    IWLIST_COMMAND_PATH,
    NETWORK_SETUP_COMMAND_PATH,
    IW_COMMAND_PATH
)

logger = logging.getLogger(__name__)


def iwconfig():
    monitors = []
    interfaces = {}
    iw_config_detected = False
    try:
        proc = Popen([IWCONFIG_COMMAND_PATH], stdout=PIPE, stderr=DEV_NULL)
        iw_config_detected = True
    except OSError as ex:
        proc = Popen([NETWORK_SETUP_COMMAND_PATH, '-listallhardwareports'], stdout=PIPE, stderr=DEV_NULL)
        osx_networksetup = True
    except OSError as ex:
        logging.exception(ex)
        raise UserWarning('Could not detect WiFi interfaces, OS not supported')

    if iw_config_detected:
        return process_iwconfig(proc, interfaces, monitors)
    if osx_networksetup:
        return process_osx_networksetup(proc, interfaces, monitors)


def process_osx_networksetup(proc, interfaces, monitors):
    interface_type = None
    device_name = None
    ethernet_address = None
    for line in proc.communicate()[0].decode('utf8').split('\n'):
        if line:
            if 'Hardware Port:' in line:
                interface_type = line.split(':')[1].strip()
            if 'Device:' in line:
                device_name = line.split(':')[1].strip()
            if 'Ethernet Address:' in line:
                ethernet_address = line.split(':')[1].strip()

            if interface_type and device_name and ethernet_address:
                if interface_type == 'Wi-Fi':
                    monitors.append(device_name)
                    interfaces[device_name] = ethernet_address
                interface_type = None
                device_name = None
                ethernet_address = None
    return monitors, interfaces


def process_iwconfig(proc, interfaces, monitors):
    for line in proc.communicate()[0].decode('utf-8').split('\n'):
        if len(line) == 0:
            continue  # Isn't an empty string
        if line[0] != ' ':  # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search:  # Isn't wired
                iface = line[:line.find(' ')]  # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                if 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    return monitors, interfaces


def get_iface(interfaces):
    scanned_aps = []

    if len(interfaces) < 1:
        logger.info('No wireless interfaces found, bring one up and try again')
        raise UserWarning('No wireless interfaces found, bring one up and try again')
    if len(interfaces) == 1:
        for interface in interfaces:
            yield interface
    # Find most powerful interface
    for iface in interfaces:
        count = 0
        proc = Popen([IWLIST_COMMAND_PATH, iface, 'scan'], stdout=PIPE, stderr=DEV_NULL)
        for line in proc.communicate()[0].decode('utf8').split('\n'):
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
    logger.info('Starting monitor mode on {0}'.format(interface))
    try:
        os.system('ifconfig %s down' % interface)
        change_mac(interface)
        os.system('{0} {1} mode monitor'.format(IWCONFIG_COMMAND_PATH, interface))
        os.system('ifconfig %s up' % interface)
        return interface
    except Exception as ex:
        print(ex)
        raise UserWarning('Could not start monitor mode')


def set_channel(interface, channel):
    logger.info(f'Changing to channel {channel} on interface {interface}')
    try:
        os.system('{0} {1} set channel {2}'.format(IW_COMMAND_PATH, interface, channel))
        return True
    except Exception as ex:
        logger.exception(ex)
        return False


def remove_mon_iface(mon_iface):
    logger.info('Removing mon interface {0}'.format(0))
    os.system('ifconfig %s down' % mon_iface)
    os.system('{0} {1} mode managed'.format(IWCONFIG_COMMAND_PATH, mon_iface))
    os.system('ifconfig %s up' % mon_iface)


def get_ifaces(args):
    try:
        monitors, interfaces = iwconfig()
    except UserWarning as ex:
        logger.info(ex)
        logger.info('Assume user provided interface is in monitor mode and a WiFi interface')
        monitors = [args.interface]
        interfaces = [args.interface]
    mon_iface = None
    if args.interface:
        mon_iface = args.interface

    if mon_iface:
        logger.info('User provided mon interfaces {0}'.format(mon_iface))
        monitors = [mon_iface]

    # Start monitor mode on a wireless interface
    logger.info('Finding the most powerful interface...')
    available_interfaces = list(filter(lambda interface: interfaces[interface] == 0, interfaces.keys()))
    interfaces = [interface for interface in get_iface(available_interfaces)]
    monmode = list(map(lambda interface: start_mon_mode(interface), available_interfaces))
    logger.info('Interfaces enabled in monitor mode: {0}'.format(monmode))
    return monmode


def mon_mac(mon_iface):
    '''
    http://stackoverflow.com/questions/159137/getting-mac-address
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytearray(mon_iface[:15], 'utf8')))
        mac = ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
    except IOError:
        _, interfaces = iwconfig()
        mac = interfaces[mon_iface]
    logger.info('Monitor mode: {0}-{1}'.format(mon_iface, mac))
    return mac


def change_mac(iface):
    rand_mac = hex(random.randint(0, 16777215))[2:].upper()
    t = iter(rand_mac)
    right_part = ':'.join(a + b for a, b in zip(rand_mac[::2], rand_mac[1::2]))
    new_mac = '00:20:91:{0}'.format(right_part)
    logger.info('Changing mac of inferface {0} to {1}'.format(iface, new_mac))
    command = ['macchanger', '-m', new_mac, iface]
    Popen(command)
