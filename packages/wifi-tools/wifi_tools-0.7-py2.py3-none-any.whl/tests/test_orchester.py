#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wifi_tools
----------------------------------

Tests for `wifi_tools` module.
"""
from tempfile import gettempdir
import fakeredis
import unittest
from mock import patch
from wifi_tools.execution import ScapyOrchester

redis_mock = fakeredis.FakeStrictRedis()
TEMP_DUMP_DIRECTORY = gettempdir()


class TestGenericAttack(unittest.TestCase):

    def tearDown(self):
        redis_mock.flushall()

    @patch('wifi_tools.execution.StrictRedis')
    def test_init(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        redis_mock.sadd('last_seen_access_points_1', 'ff:ff:ff:ff:ff:ff')
        self.assertEquals(redis_mock.get('current_attack'), None)
        self.assertEquals(redis_mock.get('current_channel'), None)
        self.assertEquals(redis_mock.get('stop_analyzer'), None)
        self.assertEquals(redis_mock.smembers('last_seen_access_points_1'), set([b'ff:ff:ff:ff:ff:ff']))
        self.assertEquals(redis_mock.ttl('last_seen_access_points_1'), None)
        orchester = ScapyOrchester([], [], mon_ifaces=['wlan0'], dump_directory=TEMP_DUMP_DIRECTORY)
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'1')
        self.assertEquals(redis_mock.get('stop_analyzer'), b'False')
        self.assertEquals(redis_mock.smembers('last_seen_access_points_1'), set())
        orchester.shutdown()

    @patch('wifi_tools.execution.StrictRedis')
    def test_ttl_on_queues(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        # redis mock doest not support ttl and expire
        return
        ttl = redis_mock.ttl('last_seen_access_points_1')
        self.assertEquals(ttl, None)
        orchester = ScapyOrchester([], [], mon_ifaces=['wlan0'], dump_directory=TEMP_DUMP_DIRECTORY)
        redis_mock.expire('last_seen_access_points_1', 10)
        self.assertNotEquals(redis_mock.ttl('last_seen_access_points_1'), None)
        orchester.shutdown()

    @patch('wifi_tools.execution.StrictRedis')
    @patch('wifi_tools.execution.ProbeRequestFloodSniffer')
    @patch('wifi_tools.execution.Analyzer')
    def test_tick_change_attack_mode(self, analyzer_mock, probe_request_flooder_mock, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        orchester = ScapyOrchester([], [], mon_ifaces=['wlan0'], dump_directory=TEMP_DUMP_DIRECTORY)
        # by default the mode is generic
        self.assertEquals(redis_mock.get('current_attack'), b'generic_attack')
        orchester.tick()
        self.assertEquals(redis_mock.get('current_attack'), b'generic_attack')
        redis_mock.set('current_attack', 'beacon_flood')
        orchester.tick()
        self.assertEquals(redis_mock.get('stop_analyzer'), b'True')
        self.assertEquals(redis_mock.get('current_attack'), b'beacon_flood')
        redis_mock.set('current_attack', 'generic_attack')
        orchester.tick()
        self.assertEquals(redis_mock.get('stop_analyzer'), b'False')
        self.assertEquals(redis_mock.get('current_attack'), b'generic_attack')
        orchester.shutdown()

    @patch('wifi_tools.execution.StrictRedis')
    def test_init_redis_cleanup(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        redis_mock.sadd('last_seen_access_points_1', 'bb:ff:cc:ff:ff:aa')
        orchester = ScapyOrchester([], [], mon_ifaces=['wlan0'], dump_directory=TEMP_DUMP_DIRECTORY)
        self.assertEquals(redis_mock.smembers('last_seen_access_points_1'), set())
        orchester.shutdown()


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
