import os
import shutil
import configparser
from pathlib import Path

from scapy.all import conf
config = configparser.ConfigParser()

# set scapy to use pcap
conf.use_pcap = True
ROOT_DIR = os.path.expanduser("~")
config_filename = os.path.join(ROOT_DIR, 'wifi_tools.ini')
file_or_directory = Path(config_filename)
if not file_or_directory.exists():
    print('Config file not found. Creating a new config on $HOME/wifi_tools.ini')
    current_path = os.path.dirname(os.path.abspath(__file__))
    example_config = os.path.join(current_path, 'wifi_tools.ini')
    shutil.copyfile(example_config, os.path.join(ROOT_DIR, 'wifi_tools.ini'))
config.read(config_filename)

wifi_tools_config = config['wifi_tools']
DUMP_DIRECTORY = wifi_tools_config['dump_directory']
OFFLINE_DUMP_DIRECTORY = wifi_tools_config['offline_dump_directory']
DOT11_NRO_SAVE_PACKETS = wifi_tools_config['dot11_nro_save_packets']
NRO_SAVE_PACKETS = wifi_tools_config['nro_save_packets']
RESULTS_DIRECTORY = wifi_tools_config['results_directory']
LOGGING_LEVEL = wifi_tools_config['logging_level']
AP_RATES =wifi_tools_config['ap_rates']
RSN=wifi_tools_config['rsn']
DEFAULT_DNS = wifi_tools_config['default_dns']
LOG_FILENAME = wifi_tools_config['log_filename']
IW_COMMAND_PATH=wifi_tools_config['iw_command_path']
IWCONFIG_COMMAND_PATH=wifi_tools_config['iwconfig_command_path']
IWLIST_COMMAND_PATH=wifi_tools_config['iwlist_command_path']
REDIS_URI = wifi_tools_config['redis_uri']
AIRPORT_COMMAND_PATH=wifi_tools_config['airport_command_path']
NETWORK_SETUP_COMMAND_PATH=wifi_tools_config['network_setup_command_path']
ATTACK_THRESHOLD = wifi_tools_config['attack_threshold']
CLIENT_SEEN_LOG = wifi_tools_config['client_seen_log']
CHANGE_CHANNEL_THRESHOLD = wifi_tools_config['change_channel_threshold']
AIREPLAY_LOG = wifi_tools_config['aireplay_log']
AIREPLAY_ERROR_LOG = wifi_tools_config['aireplay_error_log']
HANDSHAKE_DUMP= wifi_tools_config['handshake_dump']
ATTACK_THRESHOLD = int(wifi_tools_config['attack_threshold'])
ACTIVITY_LOG = wifi_tools_config['activity_log']
MITMF_LOG = wifi_tools_config['mitmf_log']
HOSTAPD_LOG = wifi_tools_config['hostapd_log']
