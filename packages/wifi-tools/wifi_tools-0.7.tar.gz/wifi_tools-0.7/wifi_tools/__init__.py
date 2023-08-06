# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import argparse
from multiprocessing import Process
from logging.handlers import RotatingFileHandler

import redis
from dateutil import parser
import multiprocessing_logging

from wifi_tools.settings import LOGGING_LEVEL, LOG_FILENAME

FREQUENCY_CHANNEL_MAP = {
    "2.412GHz": 1,
    "2.417GHz": 2,
    "2.422GHz": 3,
    "2.427GHz": 4,
    "2.432GHz": 5,
    "2.437GHz": 6,
    "2.442GHz": 7,
    "2.447GHz": 8,
    "2.452GHz": 9,
    "2.457GHz": 10,
    "2.462GHz": 11,
    "2.467GHz": 12,
    "2.472GHz": 13,
    "2.484GHz": 14,
    "5.180GHz": 36,
    "5.200GHz": 40,
    "5.220GHZ": 44,
    "5.240GHz": 48,
    "5.260GHz": 52,
    "5.280GHz": 56,
    "5.300GHz": 60,
    "5.320GHz": 64,
    "5.500GHz": 100,
    "5.520GHz": 104,
    "5.540GHz": 108,
    "5.560GHz": 112,
    "5.580GHz": 116,
    "5.600GHz": 120,
    "5.620GHz": 124,
    "5.640GHz": 128,
    "5.660GHz": 132,
    "5.680GHz": 136,
    "5.700GHz": 140,
    "5.735GHz": 147,
    "5.755GHz": 151,
    "5.775GHz": 155,
    "5.795GHz": 159,
    "5.815GHz": 163,
    "5.835GHz": 167,
    "5.785GHz": 171
}

DEV_NULL = open(os.devnull)
DN = DEV_NULL

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING'  : YELLOW,
    'INFO'     : WHITE,
    'DEBUG'    : BLUE,
    'CRITICAL' : YELLOW,
    'ERROR'    : RED,
    'RED'      : RED,
    'GREEN'    : GREEN,
    'YELLOW'   : YELLOW,
    'BLUE'     : BLUE,
    'MAGENTA'  : MAGENTA,
    'CYAN'     : CYAN,
    'WHITE'    : WHITE,
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ  = "\033[1m"

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)

redis_server = redis.StrictRedis("localhost")
pubsub = redis_server.pubsub()


def init_logging(verbose=False):
    log_format = "$BOLD%(asctime)s - %(name)s - %(levelname)s$RESET:[$BOLD%(filename)s:%(lineno)s - %(funcName)20s() $RESET] %(message)s"
    color_format = formatter_message(log_format, True)
    logging.getLogger('').handlers = []
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
    color_formatter = ColoredFormatter(color_format)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(color_formatter)
    ch.setFormatter(color_formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    if verbose:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(LOGGING_LEVEL)
        formatter = logging.Formatter(log_format)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    multiprocessing_logging.install_mp_handler()


def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--strategy", help="Which orchester strategy to use. default is attack", default="wardriving")
    parser.add_argument("-i", "--interface", help="Choose monitor mode interface. By default script will find the most powerful interface and starts monitor mode on it. Example: -i mon5")
    parser.add_argument("-c", "--channel", help="Listen on and deauth only clients on the specified channel. Example: -c 6", type=int)
    parser.add_argument("-m", "--maximum", help="Choose the maximum number of clients to deauth. List of clients will be emptied and repopulated after hitting the limit. Example: -m 5")
    parser.add_argument("-n", "--noupdate", help="Do not clear the deauth list when the maximum (-m) number of client/AP combos is reached. Must be used in conjunction with -m. Example: -m 10 -n", action='store_true')
    parser.add_argument("-t", "--timeinterval", help="Choose the time interval between packets being sent. Default is as fast as possible. If you see scapy errors like 'no buffer space' try: -t .00001")
    parser.add_argument("-p", "--packets", help="Choose the number of packets to send in each deauth burst. Default value is 1; 1 packet to the client and 1 packet to the AP. Send 2 deauth packets to the client and 2 deauth packets to the AP: -p 2")
    parser.add_argument("-d", "--directory", help="Specify a directory with pcap files for offline analysis")
    parser.add_argument("-a", "--accesspoint", help="Enter the MAC address of a specific access point to target")
    parser.add_argument("--world", help="N. American standard is 11 channels but the rest of the world it's 13 so this options enables the scanning of 13 channels", action="store_true")
    parser.add_argument("-o", "--offlinepcap", help="Offline mode for parsing pcap files", nargs='+')
    parser.add_argument("-g", "--genericattack", help="Use only generic attack", action="store_true")
    parser.add_argument("-v", "--verbose", help="Verbose mode that will print in stdout", action='store_true')
    parser.add_argument("-w", "--white_bssids", help="File with bssids to add to white list")

    return parser.parse_args()


logger = logging.getLogger(__name__)


class WiFiProcess(Process):

    def _pre_run_loop(self):
        return

    def run(self):
        self._pre_run_loop()
        try:
            while True:
                self.tick()
        except KeyboardInterrupt:
            for mon_iface in getattr(self, 'mon_ifaces', []):
                from wifi_tools.iface import remove_mon_iface
                remove_mon_iface(mon_iface)
            logger.info('\n[{0}!{1}] Closing'.format(COLOR_SEQ % RED, COLOR_SEQ % YELLOW))
            if getattr(self, 'shutdown', None):
                self.shutdown()
            sys.exit(0)

            logger.info('User sent keyboard interrupt. Stopping process')
