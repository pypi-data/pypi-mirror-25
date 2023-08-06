import os
from scapy.all import conf

# set scapy to use pcap
conf.use_pcap = True
ROOT_DIR = os.path.expanduser("~")
DUMP_DIRECTORY = os.path.join(ROOT_DIR, 'store')
OFFLINE_DUMP_DIRECTORY = os.path.join(ROOT_DIR, '/store', 'offline')
DOT11_NRO_SAVE_PACKETS = 50
NRO_SAVE_PACKETS = 5000
RESULTS_DIRECTORY = ''
LOGGING_LEVEL='INFO'
AP_RATES='\x0c\x12\x18\x24\x30\x48\x60\x6c'
RSN='\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac\x01\x28\x00'
DEFAULT_DNS = '8.8.8.8'
LOG_FILENAME = os.path.join(ROOT_DIR, 'store', 'wifi_tools.log')
IW_COMMAND_PATH='/sbin/iw'
IWCONFIG_COMMAND_PATH='/sbin/iwconfig'
IWLIST_COMMAND_PATH='/sbin/iwlist'
REDIS_URI = 'localhost'
AIRPORT_COMMAND_PATH='/usr/local/bin/airport'
NETWORK_SETUP_COMMAND_PATH='/usr/sbin/networksetup'
ATTACK_THRESHOLD = 5
CLIENT_SEEN_LOG = os.path.join(ROOT_DIR, 'store', 'clients_seen.log')
CHANGE_CHANNEL_THRESHOLD = 50  # in seconds
AIREPLAY_LOG = os.path.join(ROOT_DIR, 'store', 'aireplay.log')
AIREPLAY_ERROR_LOG = os.path.join(ROOT_DIR, 'store',' aireplay-err.log')
HANDSHAKE_DUMP= os.path.join(ROOT_DIR, 'store', 'handshakes')

