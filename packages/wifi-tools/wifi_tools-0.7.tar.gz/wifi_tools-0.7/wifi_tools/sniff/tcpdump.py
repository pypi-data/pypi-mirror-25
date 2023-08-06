from multiprocessing import Process
from subprocess import Popen


class TCPDump(Process):
    """
        This class starts tcpdump command for saving packets.
        It was added to make sure tcpdump is running
    """
    def __init__(self, interface):
        super().__init__()
        self.interface = interface

    def run(self):
        command = ['/usr/sbin/tcpdump', self.interface]
        tcpdump_process = Popen(command)
        tcpdump_process.wait()
