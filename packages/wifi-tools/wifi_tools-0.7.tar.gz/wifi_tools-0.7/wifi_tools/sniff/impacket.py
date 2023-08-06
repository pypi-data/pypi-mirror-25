

class ImpacketAnalyzer(Analyzer):

    def __init__(self, redis_server, iface, channel, sniffer=None):
        super(PcapAnalyzer, self).__init__()
        self.redis_server = redis_server
        logger.info(f'Initializing PcapAnalyzer on iface {iface}')
        self.sniffer = sniffer
        self.iface = iface
        self.activity_log = open(ACTIVITY_LOG, 'a')
        self.count = 0
        if not os.path.exists(DUMP_DIRECTORY):
            os.mkdir(DUMP_DIRECTORY)
        self.directory = new_directory(DUMP_DIRECTORY)
        self.channel = channel
        self.wpa_handshake_state = defaultdict(lambda : [0,0,0,0,0])

    def run(self):
        ticks = 0
        pcap_filename = join(self.directory, incremental_filename(self.directory, f'pcap_fixed_channel_{self.channel}_iface_{self.iface}.save'))
        pcap_file = open(pcap_filename, 'wb')
        pcapfile = dpkt.pcap.Writer(pcap_file)

        try:
            for timestamp, raw_packet in self.sniffer:
                start = datetime.now()
                try:
                    packet = None
                except dpkt.dpkt.UnpackError as ex:
                    logger.exception(ex)
                    continue
                self.tick(packet)
                pcapfile.writepkt(raw_packet, timestamp)
                end = datetime.now()
                delta = end - start
                total_time = delta.microseconds
                if ticks % 1000 == 0:
                    pcap_file.flush()
                    logger.info(f'Packets per microsecond processed {ticks/total_time}')
                ticks += 1

        except KeyboardInterrupt:
            return

    def tick(self, packet):
        pass
