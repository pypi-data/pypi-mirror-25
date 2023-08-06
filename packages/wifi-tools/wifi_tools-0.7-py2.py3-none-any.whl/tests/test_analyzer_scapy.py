import os

import dpkt
import pytest
import fakeredis
from scapy.all import rdpcap

from wifi_tools.sniff.scapy import ScapyAnalyzer

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope="session")
def auth_and_activating_wpa_packets():
    """
        Description: 802.11 capture of a new client joining the network, authenticating and activating WPA ciphering
    """
    pcap_filename = os.path.join(CURRENT_PATH, 'data', 'Network_Join_Nokia_Mobile.pcap')
    return rdpcap(pcap_filename)


def test_wpa_handshake(auth_and_activating_wpa_packets):
    redis_server = fakeredis.FakeStrictRedis(decode_responses=True)
    analyzer = ScapyAnalyzer(redis_server, 'wlan0', 11)
    count = 0
    for packet in auth_and_activating_wpa_packets:
        analyzer.tick(packet)
        try:
            print(count, packet.data.type, packet.data.subtype)
        except:
            pass
        count +=1
    print('Total', count)
    assert redis_server.hgetall('access_point_00:01:e3:41:bd:6e') == {'bssid': '00:01:e3:41:bd:6e',
                                                                      'ssid': 'martinet3',
                                                                      'channel': '11'}
    assert redis_server.hgetall('session_stats') == {'wpa': 1,
                                                     '4way': 1
                                                     }
    assert redis_server.smembers('clients_00:01:e3:41:bd:6e') == {'00:16:bc:3d:aa:57'}
    # we store on session aps if encryption was detected
    assert redis_server.smembers('session_aps') == {'00:01:e3:41:bd:6e'}

def execute_all_pcap(analyzer, auth_and_activating_wpa_packets):
    for packet in auth_and_activating_wpa_packets:
        analyzer.tick(packet)


def test_tick_performance_scapy(auth_and_activating_wpa_packets, benchmark):
    redis_server = fakeredis.FakeStrictRedis(decode_responses=True)
    analyzer = ScapyAnalyzer(redis_server, 'wlan0', 11)
    benchmark(execute_all_pcap,analyzer, auth_and_activating_wpa_packets)
