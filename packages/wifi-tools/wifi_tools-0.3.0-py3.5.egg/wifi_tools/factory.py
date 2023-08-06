from scapy.all import Dot11Elt, Dot11Beacon, RadioTap, Dot11, Dot11ProbeReq, ARP, Dot11ProbeResp
# http://blog.packetheader.net/2014/01/sending-80211-packets-with-scapy.html
# http://www.packetstan.com/2011/03/extracting-ap-names-from-packet.html
# https://gist.github.com/securitytube/5291959
RATES = '\x03\x12\x96\x18\x24\x30\x48\x60'


def beacon_factory(ssid, source, bssid, count=10, dst='ff:ff:ff:ff:ff:ff'):
    beacon = Dot11Beacon(cap=0x2104)
    essid = Dot11Elt(ID='SSID', info=ssid)
    rates = Dot11Elt(ID='Rates', info=RATES)
    dsset = Dot11Elt(ID='DSset', info='\x01')
    tim = Dot11Elt(ID='TIM', info='\x00\x01\x00\x00')
    return RadioTap()\
            /Dot11(type=0, subtype=8, addr1=dst, addr2=source, addr3=bssid)\
            /beacon / essid / rates / dsset / tim


def probe_request_factory(ssid, source, destination, bssid):
    param = Dot11ProbeReq()

    essid = Dot11Elt(ID='SSID', info=ssid)
    rates = Dot11Elt(ID='Rates', info=RATES)
    dsset = Dot11Elt(ID='DSset', info='\x01')
    return RadioTap()\
        / Dot11(addr1=source, addr2=destination, addr3=bssid)\
        / param / essid / rates / dsset


def probe_response_factory(ssid, destination, bssid):
    param = Dot11ProbeResp()
    essid = Dot11Elt(ID='SSID', info=ssid)
    rates = Dot11Elt(ID='Rates', info=RATES)
    dsset = Dot11Elt(ID='DSset', info='\x01')
    return RadioTap()\
        / Dot11(addr1=bssid, addr2=destination, addr3=bssid)\
        / param / essid / rates / dsset


def wep_arp_probe_request(bssid, source, destination, ip):
    return RadioTap() /\
        Dot11(type=0, subtype=12, addr1=source, addr2=destination, addr3=bssid) / ARP(op=ARP.who_has, psrc="192.168.5.51", pdst=ip)
