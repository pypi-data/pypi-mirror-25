#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import glob
import logging
from multiprocessing import cpu_count

from redis import StrictRedis
from scapy.all import conf
from wifi_tools import (
    R,
    W,
    parse_args,
    init_logging,
)
from wifi_tools.settings import REDIS_URI
from wifi_tools.settings import DUMP_DIRECTORY, OFFLINE_DUMP_DIRECTORY
from wifi_tools.iface import (
    get_ifaces,
)
from wifi_tools.execution import Orchester
from wifi_tools.sniff.analyzer import OfflineAnalyzer

logger = logging.getLogger(__name__)


def main():
    init_logging()
    logger.info('Starting!')
    args = parse_args()
    force_channel = args.channel
    if os.geteuid() and (not args.offlinepcap and not args.directory):
        sys.exit('[{0}-{1}] Please run as root'.format(R, W))

    mon_ifaces = []
    if not args.offlinepcap and not args.directory:
        for mon_iface in get_ifaces(args):
            mon_ifaces.append(mon_iface)
        conf.iface = mon_ifaces[0]
    clients = set()
    access_points = set()
    orchester = None

    files = []
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
        orchester = Orchester(access_points, clients, mon_ifaces=mon_ifaces, dump_directory=DUMP_DIRECTORY, force_channel=force_channel)
        orchester.start()

    if files:
        redis_server = StrictRedis(REDIS_URI)
        processes = []
        for offline_pcap in files:
            logger.info('Starting analysis of file {0}'.format(offline_pcap))
            if redis_server.get('processed_{0}'.format(offline_pcap)) == b'1':
                print('Already processed')
                continue
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
