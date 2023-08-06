#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import glob
import logging
from time import sleep
from subprocess import Popen, PIPE
from multiprocessing import cpu_count

import redis
from redis import StrictRedis
from scapy.all import conf
from wifi_tools import (
    RED,
    YELLOW,
    parse_args,
    init_logging,
)
from wifi_tools.lcd import LCDMonitor
from wifi_tools.settings import REDIS_URI
from wifi_tools.settings import DUMP_DIRECTORY, OFFLINE_DUMP_DIRECTORY
from wifi_tools.iface import (
    get_ifaces,
)
from wifi_tools.execution import (
    AttackOrchester,
    ConferenceStrategy,
    WarDrivingOrchester
)
from wifi_tools.sniff.scapy_sniffer import OfflineAnalyzer

logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    redis_server = StrictRedis(REDIS_URI, decode_responses=True, charset="utf-8")
    redis_ready = False
    while not redis_ready:
        try:
            redis_server.hgetall('position')
            redis_ready = True
        except redis.exceptions.ConnectionError:
            logger.info('Redis connection error. Retrying')
            sleep(2)
    lcd = LCDMonitor(redis_server)
    init_logging(verbose=args.verbose)
    logger.info('Starting!')
    command = ['stty', '-F', '/dev/ttyAMA0', '-echo']
    process = Popen(command, shell=True, stdout=PIPE)
    process.wait()

    command = ['gpsd', '/dev/ttyAMA0', '-nb']
    process = Popen(command, shell=True, stdout=PIPE)
    process.wait()
    force_channel = args.channel
    if os.geteuid() and (not args.offlinepcap and not args.directory):
        sys.exit('[{0}-{1}] Please run as root'.format(RED, YELLOW))

    mon_ifaces = []
    if not args.offlinepcap and not args.directory:
        try:
            for mon_iface in get_ifaces(args):
                mon_ifaces.append(mon_iface)
            conf.iface = mon_ifaces[0]
        except UserWarning as ex:
            lcd.show_message('Error!')
    clients = set()
    access_points = set()
    orchester = None

    files = []
    if args.white_bssids:
        # Imports a list of bssid to add to the white list.
        redis_server = StrictRedis(REDIS_URI)
        with open(args.white_bssids, 'r') as white_bssids_file:
            for bssid in white_bssids_file:
                bssid = bssid.upper().strip('\n').strip().encode('utf8')
                if bssid not in redis_server.smembers('bssid_white_list'):
                    print('New bssid {0} in white list.'.format(bssid))
                    redis_server.sadd('bssid_white_list', bssid)
        return
    if args.offlinepcap:
        files = args.offlinepcap
    elif args.directory:
        logger.info('Using directory {0}'.format(args.directory))
        for filename in glob.iglob('{0}/**/*.pcap'.format(args.directory)):
            files.append(filename)
        for filename in glob.iglob('{0}/**/*.cap'.format(args.directory)):
            files.append(filename)
        for filename in glob.iglob('{0}/*.pcap'.format(args.directory)):
            files.append(filename)
        for filename in glob.iglob('{0}/*.cap'.format(args.directory)):
            files.append(filename)
    else:
        logger.info('Starting realtime analysis')
        strategies = {
            'attack': AttackOrchester,
            'conference': ConferenceStrategy,
            'wardriving': WarDrivingOrchester
        }
        klass = strategies[args.strategy.lower()]

        orchester = klass(
            redis_server,
            access_points,
            clients,
            mon_ifaces=mon_ifaces,
            dump_directory=DUMP_DIRECTORY,
            force_channel=force_channel)
        lcd.start()
        orchester.start()

    if files:
        redis_server = StrictRedis(REDIS_URI)
        processes = []
        for offline_pcap in files:
            logger.info('Starting analysis of file {0}'.format(offline_pcap))
            # if redis_server.get('processed_{0}'.format(offline_pcap)) == b'1':
            print('Already processed {0}'.format(offline_pcap))
            #    continue
            redis_server.set('processed_{0}'.format(offline_pcap), '1')
            logger.info('Starting to process file {0}'.format(offline_pcap))
            if len(processes) >= cpu_count() * 2:
                for process in processes:
                    if process:
                        process.join()
                    processes.remove(process)
            analyzer = OfflineAnalyzer(redis_server=redis_server, dump_directory=OFFLINE_DUMP_DIRECTORY, offline_pcap=offline_pcap)
            analyzer.start()
            processes.append(analyzer)


if __name__ == '__main__':
    main()
