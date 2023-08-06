from multiprocessing import Process

from raspjack import RaspJack


class NRF24Sniffer(Process):

    def __init__(self, redis):
        super().__init__()
        self.redis = redis
        self.timeout = 0.4

    def _log_packet(self, packet):
        payload = ' '.join(['%02x'%c for c in packet.payload])
        logger.info('%02d | %s | %s' % (packet.channel, packet.address, payload))

    def run(self):
        sniffer = RaspJack()
        while True:
            try:
                for scan_packet in sniffer.scan(self.timeout):
                    self._log_packet(packet)
                    self.redis_server.hincrby('session_stats', 'nrf24')
                    for packet in sniffer.sniff(scan_packet.address):
                        self._log_packet(packet)
            except Exception as ex:
                logger.exception(ex)


if __name__ == '__main__':
    from redis import StrictRedis
    redis = StrictRedis()
    nrf24_sniffer = NRF24Sniffer(redis)
    nrf24_sniffer.start()
