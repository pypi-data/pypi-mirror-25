import os

import dpkt
import pytest
import fakeredis

from wifi_tools.sniff.dpkt import PcapAnalyzer

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def auth_and_activating_wpa_packets():
    """
        Description: 802.11 capture of a new client joining the network, authenticating and activating WPA ciphering
    """
    res = []
    with open(os.path.join(CURRENT_PATH, 'data', 'Network_Join_Nokia_Mobile.pcap'), 'rb') as network_join_file:
        for ts, buf in dpkt.pcap.Reader(network_join_file):
            try:
                packet = dpkt.radiotap.Radiotap(buf)
            except Exception as ex:
                continue
            res.append((ts, packet))

    return res


def test_pcap_analyzer_tick(auth_and_activating_wpa_packets):
    redis_server = fakeredis.FakeStrictRedis(decode_responses=True)
    analyzer = PcapAnalyzer(redis_server, 'wlan0', 11)
    count = 0
    for ts, packet in auth_and_activating_wpa_packets:
        analyzer.tick(packet)
        count +=1
    assert redis_server.hgetall('access_point_00:01:e3:41:bd:6e') == {'bssid': '00:01:e3:41:bd:6e',
                                                                      'ssid': 'martinet3',
                                                                      'channel': '11'}
    assert redis_server.hgetall('session_stats') == {'wpa2': 1,
                                                     'wep': 1,
                                                     'open': 1}
    assert redis_server.smembers('clients_00:01:e3:41:bd:6e') == {'00:16:bc:3d:aa:57',
                                                                  '00:01:e3:42:9e:2b'}
    # we store on session aps if encryption was detected
    assert redis_server.smembers('session_aps') == {'cf:03:ae:4a:00:2e',
                                                    '00:01:e3:41:bd:6e',
                                                    '58:1a:4c:0d:d8:29'}


def execute_all_pcap(analyzer, auth_and_activating_wpa_packets):
    for ts, packet in auth_and_activating_wpa_packets:
        analyzer.tick(packet)


def test_tick_performance_dpkt(auth_and_activating_wpa_packets, benchmark):
    redis_server = fakeredis.FakeStrictRedis(decode_responses=True)
    analyzer = PcapAnalyzer(redis_server, 'wlan0', 11)
    benchmark(execute_all_pcap, analyzer, auth_and_activating_wpa_packets)
