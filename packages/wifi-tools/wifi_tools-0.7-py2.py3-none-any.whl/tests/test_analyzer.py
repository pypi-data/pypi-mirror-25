#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wifi_tools
----------------------------------

Tests for `wifi_tools` module.
"""
import os
import json
import unittest
from tempfile import gettempdir

import fakeredis
from scapy.all import rdpcap

from lcubo_helpers import load_json
from wifi_tools.sniff.analyzer import Analyzer
from wifi_tools.factory import beacon_factory, probe_request_factory, probe_response_factory

redis_mock = fakeredis.FakeStrictRedis()
TEMP_DUMP_DIRECTORY = gettempdir()
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class TestAnalyzer(unittest.TestCase):

    def tearDown(self):
        redis_mock.flushall()

    def test_init(self):
        Analyzer('wlan0', redis_mock, TEMP_DUMP_DIRECTORY)

    def test_load_pcap_scenario_1(self):
        pass

    def test_add_access_point_when_beacon_is_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = beacon_factory('WiFi Loca', '34:45:45:45:45:45', 'ff:bb:aa:cc:ff:ff')
        analyzer.add_access_point(packet)
        expected_access_point = {
            'capability': 'short-slot+ESS+short-preamble',
            'ssid': u'WiFi Loca',
            'crypto': 'OPN',
            'bssid': 'ff:bb:aa:cc:ff:ff',
            'channel': '1'
        }
        self.assertEquals(json.loads(redis_mock.get('access_point_ff:bb:aa:cc:ff:ff').decode('utf8')), expected_access_point)

    def test_add_client_when_beacon_is_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = beacon_factory('WiFi Loca', '34:45:45:45:45:45', 'ff:bb:aa:cc:ff:ff')
        analyzer.add_client(packet)
        self.assertEquals(redis_mock.smembers('clients_ff:bb:aa:cc:ff:ff'), set([b'34:45:45:45:45:45']))

    def test_add_client_dont_add_broadcast_in_last_seen_clients(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = beacon_factory(ssid='WiFi Loca', source='ff:ff:ff:ff:ff:ff', bssid='ff:bb:aa:cc:ff:ff')
        analyzer.add_client(packet)
        self.assertEquals(redis_mock.smembers('clients_ff:ff:ff:ff:ff:ff'), set())

    def test_add_client_dont_add_broadcast_as_bssid_in_last_seen_clients(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = beacon_factory(ssid='WiFi Loca', source='00:aa:aa:aa:aa:aa', bssid='ff:ff:ff:ff:ff:ff')
        analyzer.add_client(packet)
        self.assertEquals(redis_mock.smembers('clients_ff:ff:ff:ff:ff:ff'), set())

    def test_add_access_point_when_probe_request_is_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_request_factory('WiFi Secret', 'aa:aa:aa:bb:bb:bb', 'ff:ff:ff:cc:cc:cc', 'ff:ff:ff:cc:cc:cc')
        expected_access_point = {
            'capability': '',
            'ssid': u'WiFi Secret',
            'crypto': 'OPN',
            'bssid': 'ff:ff:ff:cc:cc:cc',
            'channel': '1'}

        analyzer.add_access_point(packet)
        self.assertEquals(json.loads(redis_mock.get('access_point_ff:ff:ff:cc:cc:cc').decode('utf8')), expected_access_point)

    def test_add_access_point_dont_add_broadcast_as_access_point_probe_request(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_request_factory(ssid='WiFi Secret', source='aa:aa:aa:bb:bb:bb', destination='ff:ff:ff:cc:cc:cc', bssid='ff:ff:ff:ff:ff:ff')
        analyzer.add_client(packet)
        self.assertEquals(redis_mock.smembers('clients_ff:ff:ff:ff:ff:ff'), set())

    def test_pause_analyzer(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        redis_mock.set('stop_analyzer', True)
        res = analyzer.analize_packet(None)
        assert analyzer.stop_process is True
        assert res is None

    def test_update_access_point_infomation_when_beacon_is_processed_twice(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        access_point = {
            'capability': 'short-slot+ESS+short-preamble',
            'ssid': u'WiFi Loca',
            'crypto': 'OPN',
            'bssid': 'ff:bb:aa:cc:ff:ff',
            'channel': '1',
            'target': 'True'
        }
        redis_mock.set('access_point_ff:bb:aa:cc:ff:ff', json.dumps(access_point))
        packet = beacon_factory('WiFi Loca', '34:45:45:45:45:45', 'ff:bb:aa:cc:ff:ff')
        analyzer.analize_packet(packet)
        ap_after_analyzer = json.loads(redis_mock.get('access_point_ff:bb:aa:cc:ff:ff').decode('utf-8'))
        assert ap_after_analyzer == access_point
        packet = beacon_factory('WiFi Loca New!', '34:45:45:45:45:45', 'ff:bb:aa:cc:ff:ff')
        access_point['ssid'] = 'WiFi Loca New!'
        analyzer.analize_packet(packet)
        ap_after_analyzer = json.loads(redis_mock.get('access_point_ff:bb:aa:cc:ff:ff').decode('utf-8'))
        assert ap_after_analyzer == access_point

    def test_target_is_found(self):

        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        target_access_point = {
            'capability': 'short-slot+ESS+short-preamble',
            'ssid': u'WiFi Loca',
            'crypto': 'OPN',
            'bssid': 'ff:bb:aa:cc:ff:ff',
            'channel': '1',
            'target': 'True'
        }
        redis_mock.set('access_point_ff:bb:aa:cc:ff:ff', json.dumps(target_access_point))
        packet = beacon_factory('WiFi Loca', '34:45:45:45:45:45', 'ff:bb:aa:cc:ff:ff')
        analyzer.analize_packet(packet)
        pubsub = redis_mock.pubsub()
        pubsub.subscribe('target')
        assert pubsub.get_message() is not None

    def test_probe_request_is_correctly_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_request_factory(ssid='WiFi Secret', source='aa:aa:aa:bb:bb:bb', destination='bb:bb:bb:aa:aa:aa', bssid='bb:bb:bb:aa:aa:aa')

        analyzer.process_probe_request(packet)

        expected = {
            'ssid': 'WiFi Secret',
            'client': 'aa:aa:aa:bb:bb:bb',
            'access_point': 'bb:bb:bb:aa:aa:aa',
        }
        res = load_json(redis_mock, 'ssid_{0}'.format('aa:aa:aa:bb:bb:bb'))
        last_seen = redis_mock.smembers('last_seen_probe_networks')
        assert res == expected
        assert last_seen == set([b'WiFi Secret'])

    def test_probe_request_with_hidden_ssid_is_correctly_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_request_factory(ssid='', source='aa:aa:aa:bb:bb:bb', destination='ff:ff:ff:cc:cc:cc', bssid='bb:bb:bb:aa:aa:aa')
        analyzer.process_probe_request(packet)

        expected = {
            'ssid': '',
            'client': 'aa:aa:aa:bb:bb:bb',
            'access_point': 'bb:bb:bb:aa:aa:aa',
        }
        expected_access_point = {u'capability': u'', u'bssid': u'bb:bb:bb:aa:aa:aa', u'ssid': u'', u'channel': u'1', u'crypto': u'OPN', 'hidden': True}

        res = load_json(redis_mock, 'ssid_{0}'.format('aa:aa:aa:bb:bb:bb'))
        access_point_res = load_json(redis_mock, 'access_point_{0}'.format('bb:bb:bb:aa:aa:aa'))
        assert access_point_res == expected_access_point
        assert res == expected

    def DISABLED_test_probe_request_with_spanish_ssid_is_correctly_processed(self):
        return
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_request_factory(ssid=u'canción', source='aa:aa:aa:bb:bb:bb', destination='ff:ff:ff:cc:cc:cc', bssid='bb:bb:bb:aa:aa:aa')
        analyzer.process_probe_request(packet)

        expected = {
            'ssid': 'canción',
            'client': 'aa:aa:aa:bb:bb:bb',
            'access_point': 'bb:bb:bb:aa:aa:aa',
        }
        expected_access_point = {u'capability': u'', u'bssid': u'bb:bb:bb:aa:aa:aa', u'ssid': u'', u'channel': u'1', u'crypto': u'OPN', 'hidden': True}

        res = load_json(redis_mock, 'ssid_{0}'.format('aa:aa:aa:bb:bb:bb'))
        access_point_res = load_json(redis_mock, 'access_point_{0}'.format('bb:bb:bb:aa:aa:aa'))
        assert access_point_res == expected_access_point
        assert res == expected

    def test_probe_rsponse_is_correctly_processed(self):
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        packet = probe_response_factory(ssid='WiFi Secret', destination='cc:cc:cc:aa:aa:aa', bssid='bb:bb:bb:aa:aa:aa')

        analyzer.process_probe_request(packet)

        expected = {
            'ssid': 'WiFi Secret',
            'client': 'cc:cc:cc:aa:aa:aa',
            'access_point': 'bb:bb:bb:aa:aa:aa',
        }
        res = load_json(redis_mock, 'ssid_{0}'.format('cc:cc:cc:aa:aa:aa'))
        last_seen = redis_mock.smembers('last_seen_probe_networks')
        assert res == expected
        assert last_seen == set([b'WiFi Secret'])


class TestAnalyzerWithPackets(unittest.TestCase):

    def tearDown(self):
        redis_mock.flushall()

    def test_init(self):
        Analyzer('wlan0', redis_mock, TEMP_DUMP_DIRECTORY)

    def test_chinese_ssid(self):
        """
            this test only check that analyzer don't crash.
            SSID with chinese chars is skipped for now
        """
        packets = rdpcap(os.path.join(CURRENT_PATH, 'data', 'Chinese-SSID-Name.pcap'))
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        for packet in packets:
            analyzer.analize_packet(packet)

    def test_wpa2_eapol_processing(self):
        packets = rdpcap(os.path.join(CURRENT_PATH, 'data', 'wpa2.eapol.cap'))
        analyzer = Analyzer('lo', redis_mock, TEMP_DUMP_DIRECTORY)
        for packet in packets:
            analyzer.analize_packet(packet)

        self.assertEquals(len(analyzer.authentication_packets['00:14:6c:7e:40:80']), 4)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
