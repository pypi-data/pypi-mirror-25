# -*- coding: utf-8 -*-
import os
import time
import logging
import argparse
from multiprocessing import Process
from logging.handlers import RotatingFileHandler

import redis
from sqlalchemy.ext.declarative import declarative_base
from wifi_tools.settings import LOGGING_LEVEL, LOG_FILENAME
DN = open(os.devnull, 'w')

# Console colors
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray
T = '\033[93m'  # tan

redis_server = redis.Redis("localhost")
pubsub = redis_server.pubsub()
Base = declarative_base()


def init_logging():
    logging.getLogger('').handlers = []
    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="w",
        level=LOGGING_LEVEL)
    logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # Shut up Scapy
    need_roll = os.path.isfile(LOG_FILENAME)
    # create file handler which logs even debug messages
    fh = RotatingFileHandler(LOG_FILENAME, backupCount=50)
    if need_roll:
        # Add timestamp
        logger.info('\n---------\nLog closed on %s.\n---------\n' % time.asctime())

        # Roll over on application start
        fh.doRollover()
    fh.setLevel(LOGGING_LEVEL)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    # create formatter and add it to the handlers
    log_format = '"%(asctime)s - %(name)s - %(levelname)s:[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"'
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--skip", help="Skip deauthing this MAC address. Example: -s 00:11:BB:33:44:AA")
    parser.add_argument("-i", "--interface", help="Choose monitor mode interface. By default script will find the most powerful interface and starts monitor mode on it. Example: -i mon5")
    parser.add_argument("-c", "--channel", help="Listen on and deauth only clients on the specified channel. Example: -c 6")
    parser.add_argument("-m", "--maximum", help="Choose the maximum number of clients to deauth. List of clients will be emptied and repopulated after hitting the limit. Example: -m 5")
    parser.add_argument("-n", "--noupdate", help="Do not clear the deauth list when the maximum (-m) number of client/AP combos is reached. Must be used in conjunction with -m. Example: -m 10 -n", action='store_true')
    parser.add_argument("-t", "--timeinterval", help="Choose the time interval between packets being sent. Default is as fast as possible. If you see scapy errors like 'no buffer space' try: -t .00001")
    parser.add_argument("-p", "--packets", help="Choose the number of packets to send in each deauth burst. Default value is 1; 1 packet to the client and 1 packet to the AP. Send 2 deauth packets to the client and 2 deauth packets to the AP: -p 2")
    parser.add_argument("-d", "--directory", help="Specify a directory with pcap files for offline analysis")
    parser.add_argument("-a", "--accesspoint", help="Enter the MAC address of a specific access point to target")
    parser.add_argument("--world", help="N. American standard is 11 channels but the rest of the world it's 13 so this options enables the scanning of 13 channels", action="store_true")
    parser.add_argument("-o", "--offlinepcap", help="Offline mode for parsing pcap files", nargs='+')
    parser.add_argument("-g", "--genericattack", help="Use only generic attack", action="store_true")

    return parser.parse_args()


logger = logging.getLogger(__name__)


class WiFiProcess(Process):

    def run(self):
        try:
            while True:
                self.tick()
        except KeyboardInterrupt:
            logger.info('User sent keyboard interrupt. Stopping process')
