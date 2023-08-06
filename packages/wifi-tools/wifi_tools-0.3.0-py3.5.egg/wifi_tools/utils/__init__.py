import os
import sys
import struct
import logging
from time import sleep
from random import randint
from subprocess import Popen, PIPE
from signal import SIGINT

from pythonwifi.iwlibs import Wireless
from spoofmac.interface import (
    find_interface,
    set_interface_mac,
)

from wifi_tools import (
    R,
    W,
    DN,
)
from wifi_tools.settings import IW_COMMAND_PATH, AIRPORT_COMMAND_PATH
logger = logging.getLogger(__name__)


def random_mac_address(vendor=None):
    # TODO implement vendors
    part_0 = "%02x" % randint(0x00, 0x7f)
    part_1 = "%02x" % randint(0x00, 0x7f)
    part_2 = "%02x" % randint(0x00, 0x7f)
    return '00:20:91:{0}:{1}:{2}'.format(part_0, part_1, part_2)


def change_mac_address(iface):
    mac_address = random_mac_address()
    logger.info('Changing MAC address of {0} to {1}'.format(iface, mac_address))
    result = find_interface(iface)
    if result is None:
        logger.info('- couldn\'t find the device for {target}'.format(
            target=iface
        ))
        return False

    port, device, address, current_address = result
    target_mac = mac_address
    if int(target_mac[1], 16) % 2:
        logger.warn('Warning: The address you supplied is a multicast address and thus can not be used as a host address.')
    if address is None:
        logger.info('- {target} missing hardware MAC'.format(
            target=iface
        ))
        return False
    target_mac = address
    set_interface_mac(device, target_mac, port)
    return True


def switch_channel(mon_iface, mon_channel, sleep_time):
    iw_process_found = False
    airport_process_found = False
    try:
        logger.debug('Setting channel {0} to iface {1}'.format(mon_channel, mon_iface))
        proc = Popen([IW_COMMAND_PATH, 'dev', mon_iface, 'set', 'channel', mon_channel], stdout=DN, stderr=PIPE)
        sleep(sleep_time)
        logger.debug('Active channel {0} on interface {1}'.format(mon_channel, mon_iface))
        iw_process_found = True
    except OSError as ex:
        logger.debug('Setting channel {0} to iface {1}'.format(mon_channel, mon_iface))
        proc = Popen([AIRPORT_COMMAND_PATH, mon_iface, 'sniff', mon_channel], stdout=DN, stderr=PIPE)
        sleep(sleep_time)
        Popen("kill -HUP %s" % proc.pid, shell=True)
        logger.debug('Active channel {0} on interface {1}'.format(mon_channel, mon_iface))
        airport_process_found = True
    except OSError as ex:
        logger.exception(ex)
        logging.error('[{0}-{1}] Could not execute \"iw\"'.format(R, W))
        os.kill(os.getpid(), SIGINT)
        sys.exit(1)

    for line in proc.communicate()[1].decode('utf-8').split('\n'):
        if iw_process_found and len(line) > 2:  # iw dev shouldnt display output unless there's an error
            logger.error('[{0}-{1}] Channel hopping failed: {0} {2} {1}'.format(R, W, line))
        if airport_process_found and 'Capturing' not in line:
            logger.error('[{0}-{1}] Channel hopping failed: {0} {2} {1}'.format(R, W, line))


def switch_mode(iface, mode):
    mon_iface = 'mon0'
    try:
        logger.debug('Setting mode {0} to iface {1}'.format(mode, mon_iface))
        proc = Popen([IW_COMMAND_PATH, 'dev', iface, 'interface', 'add', mon_iface, 'type', mode], stdout=DN, stderr=PIPE)
        logger.debug('Active channel {0} on interface {1}'.format(mode, mon_iface))
    except OSError as ex:
        logger.exception(ex)
        logger.error('[{0}-{1}] Could not execute "iw"'.format(R, W))
        os.kill(os.getpid(), SIGINT)
        sys.exit(1)

    for line in proc.communicate()[1].split('\n'):
        if len(line) > 2:  # iw dev shouldnt display output unless there's an error
            logger.error('[{0}-{1}] failed: {0} {2} {1}'.format(R, W, line))

    return mon_iface


def channel_to_frequency(channel):
    if channel == 14:
        freq = 2484
    else:
        freq = 2407 + (channel * 5)

    freq_string = struct.pack("<h", freq)

    return freq_string


def join_wifi(iface, bssid, ssid, mode, key=None):
    wifi_client = Wireless(iface)
    wifi_client.setAPaddr(bssid)
    wifi_client.setEssid(ssid)
    if key:
        wifi_client.setKey(key.encode('hex'))
    wifi_client.setEncryption(mode)  # OPEN, RESTRICTED, OFF
    return wifi_client.commit()
