# encoding: utf-8

from socket import *
import threading

from .Packets import EthernetFrame
from .HMAC import HMAC

__author__ = 'BetaS'


class L2Socket:
    def __init__(self, dev, queue=None, ether_type=0x0801, mtu=1527):
        self.alive = True
        self.dev = dev
        self.ether_type = ether_type
        self.mtu = mtu

        self.sock = socket(PF_PACKET, SOCK_RAW, htons(ether_type))
        self.sock.setblocking(False)
        self.sock.bind((dev, 0))

        self.hw_addr = self.get_hw_addr()

        self.queue = queue
        self.receiver = threading.Thread(target=L2Socket.recv, args=[self])

    def get_hw_addr(self):
        import fcntl, struct
        info = fcntl.ioctl(self.sock.fileno(), 0x8927, struct.pack('256s', self.dev[:15].encode()))
        return HMAC.parse(':'.join(['%02X' % char for char in info[18:24]]))

    def send(self, target, payload):
        if type(target) == str:
            target = HMAC.parse(target)

        ether_frame = EthernetFrame.build(self.hw_addr, target, self.ether_type, payload)
        self.sock.send(ether_frame)

        return True

    def broadcast(self, payload):
        return self.send("ff:ff:ff:ff:ff:ff", payload)

    def recv(self):
        print("[!] ether_sock : WAITING...")
        while self.alive:
            try:
                buff = self.sock.recv(self.mtu)
                if len(buff) > 18:              # minimum header(14) + crc32(4)
                    p = EthernetFrame.parse(buff)
                    if p:
                        if self.queue:
                            self.queue.put((p.src, p.payload))
                    else:
                        print("[!] ether_sock : CRC INVALID")
            except:
                pass

    def listen_start(self):
        if not self.receiver.is_alive():
            self.alive = True
            self.receiver.start()

    def listen_stop(self):
        if self.receiver.is_alive():
            self.alive = False
            self.receiver.join()

    def is_listen(self):
        return self.alive
