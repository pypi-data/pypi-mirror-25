#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wifi_tools
----------------------------------

Tests for `wifi_tools` module.
"""
import fakeredis
import unittest
from mock import Mock, patch
from scapy import all
from scapy.all import Dot11

from wifi_tools.attack import DeauthAttack
from lcubo_helpers import (
    save_json
)

redis_mock = fakeredis.FakeStrictRedis()


class TestDeauthAttack(unittest.TestCase):

    def setUp(self):
        access_point = {
            'ssid': 'test',
            'bssid': '88:33:dd:33:44:bb',
            'channel': 1,
        }
        save_json(redis_mock, 'access_point_88:33:dd:33:44:bb', access_point)

    def tearDown(self):
        redis_mock.flushall()

    @patch.object(all, 'send')
    @patch('wifi_tools.attack.StrictRedis')
    def test_scapy_send_packet_is_not_called(self, mock_strict_redis, mock):
        mock_strict_redis.return_value = redis_mock
        deauth_attack = DeauthAttack('wlan0')
        deauth_attack._process_startup()
        deauth_attack.send_packets([])
        mock.assert_not_called()

    @patch('wifi_tools.attack.StrictRedis')
    def test_attack_access_points_returns_packets_when_last_seen_list_is_not_empty(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        deauth_attack = DeauthAttack('wlan0')
        deauth_attack._process_startup()
        deauth_attack.current_channel = 1
        data = {'bssid': '88:33:dd:33:44:bb'}
        res = deauth_attack.attack_access_points(data)
        self.assertEquals(len(res), 1)
        packet = res[0]
        self.assertEquals(packet.haslayer(Dot11), True)
        self.assertEquals(packet.type, 0)
        self.assertEquals(packet.subtype, 12)
        self.assertEquals(packet.addr1, 'ff:ff:ff:ff:ff:ff')
        self.assertEquals(packet.addr2, '88:33:dd:33:44:bb')
        self.assertEquals(packet.addr3, '88:33:dd:33:44:bb')

    @patch('wifi_tools.attack.StrictRedis')
    def test_attack_access_point_clients_with_clients_returns_non_empty(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        deauth_attack = DeauthAttack('wlan0')
        deauth_attack._process_startup()

        data = {'bssid': '88:33:dd:33:44:bb'}
        redis_mock.sadd('clients_88:33:dd:33:44:bb', 'ff:33:dd:33:44:ff')
        res = deauth_attack.attack_clients(data)
        self.assertEquals(len(res), 2)
        packet1 = res[0]
        packet2 = res[1]
        bssid = '88:33:dd:33:44:bb'
        self.assertEquals(packet1.addr1, b'ff:33:dd:33:44:ff')
        self.assertEquals(packet1.addr2, bssid)
        self.assertEquals(packet1.addr3, bssid)

        self.assertEquals(packet2.addr1, bssid)
        self.assertEquals(packet2.addr2, b'ff:33:dd:33:44:ff')
        self.assertEquals(packet2.addr3, bssid)

    @patch('wifi_tools.attack.StrictRedis')
    def test_tick_generates_packets(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        redis_mock.set('current_channel', b'1')
        deauth_attack = DeauthAttack('wlan0')
        deauth_attack._process_startup()
        data = {'bssid': b'88:33:dd:33:44:bb', 'channel': b'1'}
        deauth_attack.attack_clients = Mock()
        deauth_attack.attack_access_points = Mock()
        deauth_attack.send_packets = Mock()
        deauth_attack.tick(data)
        assert deauth_attack.attack_clients.called
        assert deauth_attack.attack_access_points.called

    @patch('wifi_tools.attack.StrictRedis')
    def test_tick_dont_generates_packets_when_ap_is_on_different_channel(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        redis_mock.set('current_channel', '1')
        deauth_attack = DeauthAttack('wlan0')
        deauth_attack._process_startup()
        data = {'bssid': '88:33:dd:33:44:bb', 'channel': '11'}
        deauth_attack.attack_clients = Mock()
        deauth_attack.attack_access_points = Mock()
        deauth_attack.send_packets = Mock()
        deauth_attack.tick(data)
        assert not deauth_attack.attack_clients.called
        assert not deauth_attack.attack_access_points.called


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
