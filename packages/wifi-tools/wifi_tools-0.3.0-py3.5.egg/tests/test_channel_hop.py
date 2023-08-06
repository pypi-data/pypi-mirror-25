#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_wifi_tools
----------------------------------

Tests for `wifi_tools` module.
"""
import unittest
from mock import patch

import fakeredis
from wifi_tools.channel_hop import RoundRobinChannelHop, FrequencyChannelHop

redis_mock = fakeredis.FakeStrictRedis()


class TestChannelHop(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        redis_mock.flushall()

    @patch('time.sleep')
    @patch('wifi_tools.channel_hop.StrictRedis')
    def test_channel_hop_iterates_over_all_channels(self, mock_strict_redis, mock):
        mock_strict_redis.return_value = redis_mock
        self.assertEquals(redis_mock.get('current_channel_wlan0'), None)

        channel_hop = RoundRobinChannelHop('wlan0')
        channel_hop._pre_run_loop()
        for channel_no in range(1, 12):
            with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
                channel_hop.tick()
                self.assertEquals(redis_mock.get('current_channel_wlan0').decode('utf8'), str(channel_no))
                switch_channel_mock.assert_called_with('wlan0', str(channel_no), 0.05)
            # switch_channel_mock.assert_called_with('wlan0', str(channel_no))
        channel_hop.tick()
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'1')
        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', '2', 0.05)
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'2')

    @patch('time.sleep')
    @patch('wifi_tools.channel_hop.StrictRedis')
    def test_force_channel(self, mock_strict_redis, mock):
        mock_strict_redis.return_value = redis_mock
        redis_mock.set('force_channel_wlan0', 4)
        channel_hop = RoundRobinChannelHop('wlan0')
        channel_hop._pre_run_loop()
        # default channel is 1 after initialization
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'1')
        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', '4', 1)
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'4')
        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', '4', 1)
        self.assertEquals(redis_mock.get('current_channel_wlan0'), b'4')


class TestFrequencyChannelHop(unittest.TestCase):

    @patch('wifi_tools.channel_hop.StrictRedis')
    def test_without_information_round_robin_is_used(self, mock_strict_redis):
        mock_strict_redis.return_value = redis_mock
        channel_hop = FrequencyChannelHop('wlan0')
        channel_hop._pre_run_loop()
        for channel in range(1, 13):
            redis_mock.set('channel_count_{0}'.format(channel), 0)

        for channel_no in range(1, 12):
            with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
                channel_hop.tick()
                switch_channel_mock.assert_called_with('wlan0', str(channel_no), 0.05)

        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', str(1), 0.05)

    @patch('time.sleep')
    @patch('wifi_tools.channel_hop.StrictRedis')
    def test_channels_6_and_11_has_all_the_access_points(self, mock_strict_redis, mock):
        mock_strict_redis.return_value = redis_mock
        channel_hop = FrequencyChannelHop('wlan0')
        channel_hop._pre_run_loop()
        for channel in range(1, 13):
            amount = 0
            if channel == 6:
                amount = 20
            if channel == 11:
                amount = 50
            redis_mock.set('channel_count_{0}'.format(channel), amount)

        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', str(11), 2.7142857142857144)

        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', str(6), 2.2857142857142857)

        for channel in [1, 2, 3, 4, 5, 7, 8, 9, 10]:
            with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
                channel_hop.tick()
                switch_channel_mock.assert_called_with('wlan0', str(channel), 0.05)

        with patch('wifi_tools.channel_hop.switch_channel') as switch_channel_mock:
            channel_hop.tick()
            switch_channel_mock.assert_called_with('wlan0', str(11), 2.7142857142857143)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
