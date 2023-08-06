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
from mock import call, patch, Mock
from wifi_tools import DN
from wifi_tools.utils import (
    switch_channel,
)

redis_mock = fakeredis.FakeStrictRedis()
TEMP_DUMP_DIRECTORY = gettempdir()


class TestUtilsFunctions(unittest.TestCase):

    @patch('wifi_tools.utils.Popen')
    def test_switch_channel_linux_case(self, mock):
        mon_iface = 'wlan0'
        mon_channel = '1'
        switch_channel(mon_iface, mon_channel, 0.05)
        mock.assert_any_call(['/sbin/iw', 'dev', 'wlan0', 'set', 'channel', '1'], stderr=-1, stdout=DN)

    @patch('wifi_tools.utils.Popen')
    def test_switch_channel_osx_case(self, mock):
        def popen_side_effect(*args, **kwargs):
            sniff_output = b'Capturing 802.11 frames on en0.'
            proc = Mock()
            proc.pid = -10
            proc.communicate = Mock(return_value=['', sniff_output])
            if '/sbin/iw' in ''.join(args[0][0]):
                raise OSError('Command not found')
            if '/usr/local/bin/airport' in ''.join(args[0][0]):
                return proc
        mock.side_effect = popen_side_effect
        mon_iface = 'wlan0'
        mon_channel = '1'
        switch_channel(mon_iface, mon_channel, 0.05)
        expected = [
            call(['/sbin/iw', 'dev', 'wlan0', 'set', 'channel', '1'], stderr=-1, stdout=DN),
            call(['/usr/local/bin/airport', 'wlan0', 'sniff', '1'], stderr=-1, stdout=DN),
            call('kill -HUP -10', shell=True)
        ]
        mock.assert_has_calls(expected)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
