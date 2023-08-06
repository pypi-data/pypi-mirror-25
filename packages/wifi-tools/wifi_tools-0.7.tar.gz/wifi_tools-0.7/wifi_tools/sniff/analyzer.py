import json
import uuid
import logging
import calendar
from datetime import datetime
from multiprocessing import Process

from dateutil.parser import parse


from wifi_tools.utils import (
    byte_dict_to_str,
)
from wifi_tools.settings import (
    ATTACK_THRESHOLD,
)
logger = logging.getLogger(__name__)


class Analyzer(Process):

    def update_stats(self, data):
        added = self.redis_server.sadd('session_aps', data['bssid'])
        if added:
            encryption = data['encryption'].lower()
            if encryption == 'opn':
                encryption = 'open'
            self.redis_server.hincrby('session_stats', encryption)

    def tear_down(self):
        self.activity_log.close()

    def in_white_list(self, bssid):
        self.white_list = self.redis_server.smembers('bssid_white_list')
        access_point_bssid = bssid.upper().encode('utf8')
        if access_point_bssid in self.white_list:
            logger.debug('Access point {0} in white list, skipping.'.format(access_point_bssid))
            return True
        return False

    def stop_childs(self):
        raise NotImplementedError

    def _skip_attack(self, data):
        if data['bssid'] == 'ff:ff:ff:ff:ff:ff':
            return True
        last_attack_key = 'last_attack_{0}_{1}'.format(data['bssid'], data['client'])
        last_attack = self.redis_server.get(last_attack_key)
        now = datetime.now()
        if last_attack:
            last_attack = parse(last_attack)
            delta = now - last_attack
            if delta.seconds < ATTACK_THRESHOLD:
                logger.debug('Skipping attack to {0} bssid. Last attack was {1} seconds ago.'.format(data['bssid'], delta.seconds))
                return True
        return False

    def _prepare_attack_data(self, data, channel):
        last_attack_key = 'last_attack_{0}_{1}'.format(data['bssid'], data['client'])
        now = datetime.now()
        self.redis_server.set(last_attack_key, now)
        attack_id = str(uuid.uuid4())
        attack_data = {
            'client_addr': data['client'],
            'bssid': data['bssid'],
            'ssid': data.get('ssid', None),
            'channel': channel,
            'power': data.get('power', None),
            'date': str(datetime.utcnow()),
            'attack_id': attack_id
        }
        return attack_data

    def _attack_bssid(self, data, channel):
        if self._skip_attack(data):
            return
        attack_data = self._prepare_attack_data(data, channel)
        self.redis_server.lpush('client_attack_queue_{0}'.format(self.iface), json.dumps(attack_data))
        logger.debug('Attack sent')

    def save_ap(self, data):
        if data['bssid'] in [self.redis_server.get('own_ap_bssid'), 'ff:ff:ff:ff:ff:ff']:
            logger.debug('Detected own AP. skipping')
            return
        bssid = data['bssid'].lower()
        access_point = self.redis_server.hgetall('access_point_{0}'.format(bssid))
        if access_point.get('target') == '1':
            data = {'bssid': bssid, 'channel': data['channel']}
            self.redis_server.publish('target_found', json.dumps(data))

        if not access_point:
            logger.info(u'Detected NEW Access Point with SSID {0}, BSSID {1}. Channel {2}'.format(data.get('ssid'), bssid, data.get('channel')))
            access_point = {
                'bssid': bssid,
            }
        position = self.redis_server.hgetall('position')
        if position:
            if 'strength' in data:
                position['strength'] = data['strength']
            self.redis_server.sadd('access_point_position_{data["bssid"]', position)
            logger.info(f'Position for ap {bssid} from gps detected {position}')
            if 'strength' in access_point and 'strength' in data:
                if access_point['strength'] < data['strength']:
                    logger.info('More strength position found!')
                    access_point.update(position)
            else:
                access_point.update(position)

        logger.debug(f'Detected Access Point with SSID {data.get("ssid")} on channel {data.get("channel")}')
        if 'ssid' in data:
            access_point['ssid'] = data['ssid']
        if 'Authentication' in data:
            access_point['authentication'] = data.get('Authentication')
        if 'Cypher' in data:
            access_point['cipher'] = data.get('Cipher')
        if 'wep' == data.get('encription', ''):
            data = {'bssid': bssid, 'channel': data['channel']}
            self.redis_server.publish('wep_found', json.dumps(data))
        if 'channel' in data:
            access_point['channel'] = data['channel']
            self.redis_server.sadd('access_points_iface_{0}_channel_{1}'.format(self.iface, data['channel']), bssid)
        for client_address in data.get('clients', []):
            logger.debug('Found client {client_address} for ap {bssid}'.format(client_address=client_address, bssid=bssid))
            self.redis_server.sadd('clients_{0}'.format(bssid), client_address)
            now = datetime.utcnow()
            now_in_unixtime = calendar.timegm(now.utctimetuple())
            self.activity_log.write('{0},{1},{2}\n'.format(now_in_unixtime, bssid, client_address))

        self.activity_log.flush()
        access_point.pop('clients', None)
        self.redis_server.hmset(f'access_point_{bssid}', access_point)

    def process_probe_requests(self, probes, station_mac, bssid):
        for probe in probes:
            if not probe:
                continue
            if type(probe) == bytes:
                try:
                    probe = probe.decode('utf8')
                except Exception as ex:
                    logger.exception(ex)
                    continue
            logger.debug('Found probe request {0} on interface {1}'.format(probe, self.iface))
            position = self.redis_server.hgetall('position')
            try:
                probe_ssid = {
                    'ssid': probe,
                    'client': station_mac,
                    'bssid': bssid
                }
            except UnicodeDecodeError as ex:
                logger.exception(ex)
                return
            if position:
                probe_ssid.update(byte_dict_to_str(position))
            try:
                added = self.redis_server.sadd(f'probe_request_{probe_ssid["ssid"]}', json.dumps(probe_ssid))
            except Exception as ex:
                print(ex)
            if added:
                self.redis_server.zincrby('probe_requests', probe_ssid['ssid'])
            added = self.redis_server.sadd(f'session_probe_request_{probe_ssid["ssid"]}', json.dumps(probe_ssid))
            if added:
                self.redis_server.zincrby('session_probe_requests', probe_ssid['ssid'])

    def process_clients(self, data):
        for client in data.get('clients', []):
            station_mac = client
            bssid = data['bssid'].lower()
            last_time_seen = datetime.utcnow()

            position = self.redis_server.hgetall('position')
            if position:
                if 'strength' in data:
                    position['strength'] = data['strength']
                    position['station_mac'] = station_mac
                self.redis_server.sadd(f'client_positions_{bssid}', json.dumps(position))
            self.redis_server.sadd('access_point_{0}_client_{1}_last_time_seen'.format(bssid, station_mac), last_time_seen)
            self.redis_server.sadd('clients_{0}'.format(bssid), station_mac)
