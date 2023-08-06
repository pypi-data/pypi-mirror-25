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
from mock import Mock, patch
import pytest
from wifi_tools.settings import IWCONFIG_COMMAND_PATH
from wifi_tools.iface import (
    process_osx_networksetup,
    start_mon_mode,
    remove_mon_iface,
    mon_mac,
    iwconfig,
    get_iface
)

redis_mock = fakeredis.FakeStrictRedis()
TEMP_DUMP_DIRECTORY = gettempdir()


class TestGenericAttack(unittest.TestCase):

    @patch('wifi_tools.iface.Popen')
    def test_iwconfig_parser_with_two_interfaces(self, mock):
        iwconfig_output = b"""
wlan3     IEEE 802.11bg  ESSID:off/any
          Mode:Managed  Access Point: Not-Associated   Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:off

eth0      no wireless extensions.

wlan0     IEEE 802.11bgn  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off

eth1      no wireless extensions.

lo        no wireless extensions.
        """
        mocked_subprocess = Mock()
        mocked_subprocess.communicate = Mock(return_value=[iwconfig_output])
        mock.return_value = mocked_subprocess
        monitors, interfaces = iwconfig()
        assert ['wlan0'] == monitors
        assert interfaces == {'wlan3': 0, 'wlan0': 0}

    @patch('os.system')
    def test_start_mon_mode(self, mock):
        start_mon_mode('wlan0')
        self.assertEquals(mock.call_count, 3)
        self.assertEquals(mock.call_args_list[0][0][0], 'ifconfig wlan0 down')
        self.assertEquals(mock.call_args_list[1][0][0], '{0} wlan0 mode monitor'.format(IWCONFIG_COMMAND_PATH))
        self.assertEquals(mock.call_args_list[2][0][0], 'ifconfig wlan0 up')

    @patch('os.system')
    def test_remove_mon_iface(self, mock):
        remove_mon_iface('wlan0')
        self.assertEquals(mock.call_count, 3)
        self.assertEquals(mock.call_args_list[0][0][0], 'ifconfig wlan0 down')
        self.assertEquals(mock.call_args_list[1][0][0], '{0} wlan0 mode managed'.format(IWCONFIG_COMMAND_PATH))
        self.assertEquals(mock.call_args_list[2][0][0], 'ifconfig wlan0 up')

    @patch('socket.socket')
    @patch('wifi_tools.iface.fcntl')
    def test_retrieve_monitor_mac_address(self, mocked_fcntl, mock):
        mocked_socket = Mock()
        mocked_socket.fileno.return_value = 1
        mock.return_value = mocked_socket

        mocked_ioctl = Mock()
        mocked_ioctl.return_value = 'wlan0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        mocked_fcntl.ioctl = mocked_ioctl
        mac = mon_mac('wlan0')
        self.assertEquals(mac, '00:ff:ff:00:00:00')

    @patch('wifi_tools.iface.Popen')
    def test_iwconfig_returns_monitors_and_interfaces(self, mock):
        iwconfig_output = b"""wlan0     IEEE 802.11bgn  Mode:Monitor  Frequency:2.417 GHz  Tx-Power=20 dBm
                  Retry short limit:7   RTS thr:off   Fragment thr:off
                  Power Management:off
                            """
        mocked_subprocess = Mock()
        mocked_subprocess.communicate = Mock(return_value=[iwconfig_output])
        mock.return_value = mocked_subprocess
        monitors, interfaces = iwconfig()
        self.assertEquals(['wlan0'], ['wlan0'])

    @patch('wifi_tools.iface.Popen')
    def test_iwconfig_not_found(self, mock):
        mock.side_effect = OSError('Command not found')
        with pytest.raises(OSError):
            iwconfig()

    @patch('wifi_tools.iface.Popen')
    def test_get_ifaces_with_one_iface(self, mock):
        for algo in get_iface(['wlan0']):
            assert algo == 'wlan0'

    @patch('wifi_tools.iface.Popen')
    def test_get_ifaces_without_ifaces(self, mock):
        with pytest.raises(SystemExit):
            for algo in get_iface([]):
                pass

    def test_get_ifaces_finds_the_most_powerful_interface(self):
        return
        def interface_output(command, stdout, stderr):
            pass
        from wifi_tools.iface import Popen
        with mock.patch.object(Popen, '__init__', side_effect=interface_output):
            for algo in get_iface(['wlan0', 'wlan1']):
                assert algo == 'wlan1'

    def test_get_osx_network_setup(self):
        network_setup_output = b"""
        Hardware Port: Wi-Fi
        Device: en0
        Ethernet Address: ff:ff:ff:ff:ff:00

        Hardware Port: Bluetooth PAN
        Device: en3
        Ethernet Address: ff:ff:ff:ff:ff:01

        Hardware Port: Thunderbolt 1
        Device: en1
        Ethernet Address: ff:ff:ff:ff:ff:02

        Hardware Port: Thunderbolt 2
        Device: en2
        Ethernet Address: ff:ff:ff:ff:ff:03

        Hardware Port: Thunderbolt Bridge
        Device: bridge0
        Ethernet Address: ff:ff:ff:ff:ff:04

        VLAN Configurations
        ===================
        """
        proc = Mock()
        monitors = []
        interfaces = {}
        proc.communicate = Mock(return_value=[network_setup_output])
        process_osx_networksetup(proc, interfaces, monitors)
        assert monitors == ['en0']


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
