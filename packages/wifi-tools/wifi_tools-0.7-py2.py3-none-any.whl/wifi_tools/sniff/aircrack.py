import os
import logging
from time import sleep


from pyrcrack.scanning import Airodump
from lcubo_helpers import (
    new_directory,
    incremental_filename,
)

from wifi_tools.sniff.analyzer import Analyzer
from wifi_tools.settings import (
    DUMP_DIRECTORY,
    ACTIVITY_LOG
)

logger = logging.getLogger(__name__)


class AirodumpAnalyzer(Analyzer):

    def __init__(self, redis, iface, channel=None):
        self.redis_server = redis
        super(AirodumpAnalyzer, self).__init__()
        logger.info(f'Initializing AirodumpAnalyzer on iface {iface}')
        self.iface = iface
        self.channel = channel
        self.directory = new_directory(DUMP_DIRECTORY)
        self.activity_log = open(ACTIVITY_LOG, 'a')
        self.attack_enabled = True

    def run(self):
        self.redis_server.delete('client_attack')
        self.start_airodump()
        while True:
            try:
                self.tick()
            except KeyboardInterrupt:
                self.stop_childs()

    def tick(self):
        if not self.airodump_process:
            self.start_airodump()

        try:
            tree_data = self.process_tree()
            logger.debug(f'Processed {len(tree_data)} aps. on interface {self.iface}')
            for data in tree_data:
                clients = []
                bssid_clients = [client_info for client_info in self.airodump_process.clients if client_info['bssid'].lower() == data['bssid'].lower()]
                clients = {
                    'clients': map(lambda client_info: client_info['client'], bssid_clients),
                    'bssid': data['bssid']
                }
                if bssid_clients:
                    self.process_clients(clients)
                bssid = data['bssid']
                self.update_stats(data)
                if self.in_white_list(bssid):
                    # we don't attack aps in white list.
                    continue
                if 'password' in data:
                    pass
                if data['encryption'] not in ['WPA', 'WPA2', 'WPA2 WPA']:
                    # we don't support other encryption yet.
                    logger.debug('Encryption is not WPA or WPA2, skipping {0}'.format(data['ESSID']))
                    continue

                for client_data in bssid_clients:
                    client_address = client_data['client']
                    client_data['ssid'] = data['ESSID']
                    logger.debug(f'Found client {client_address} for bssid {bssid}')
                    if self.attack_enabled:
                        self._attack_bssid(client_data, data['channel'])

        except Exception as ex:
            logger.exception(ex)

        sleep(1.3)

    def stop_childs(self):
        print('Killing childs')
        self.airodump_process.stop()
        return True

    def process_tree(self):
        tree = self.airodump_process.tree
        res = []
        for bssid, data in tree.items():
            data['ssid'] = data['ESSID']
            self.save_ap(data)
            res.append(data)

        return res


class FixedChannelAirodumpAnalyzer(AirodumpAnalyzer):
    """
        To make wardriving more successulf it's better
        to have the interface listening to one channel always.
        For more coverage add more interfaces
    """

    def __str__(self):
        return f'FixedChannelAirodumpAnalyzer on iface {self.iface}'

    def start_airodump(self):
        self.capture_channel(self.channel)

    def capture_channel(self, channel):
        writepath = os.path.join(self.directory, incremental_filename(self.directory, 'airodump_fixed_channel_{0}_iface_{1}.save'.format(channel, self.iface)))
        logger.debug('Saving packets to file {0}'.format(writepath))
        # when we start we let airodump-ng do the channel hopping.

        self.kwargs = {
            'channel': str(channel),
            'output-format': 'pcap,csv',
            'write': writepath,
            'write-interval': '2',
        }
        self.airodump_process = Airodump(self.iface, **self.kwargs)
        self.airodump_process.start()

    def _set_airodump_attack_mode(self):
        pass


class AllChannelsAirodumpAnalyzer(AirodumpAnalyzer):
    """
        This is useful for normal wardriving
    """
    def start_airodump(self):
        self.capture_all_channels()

    def capture_all_channels(self):
        self.attack_enabled = False
        writepath = os.path.join(self.directory, incremental_filename(self.directory, 'airodump_all_{0}.save'.format(self.iface)))
        logger.debug('Saving packets to file {0}'.format(writepath))
        # when we start we let airodump-ng do the channel hopping.

        self.kwargs = {
            'output-format': 'pcap,csv',
            'write': writepath
        }
        self.airodump_process = Airodump(self.iface, **self.kwargs)
        self.airodump_process.start()
