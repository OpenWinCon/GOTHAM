# encoding: utf-8

from gotham.util.threadutil import Thread
import socket

__author__ = 'BetaS'


class UDPServer(Thread):
    def __init__(self, dev, port):
        super().__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, dev)
        self._sock.settimeout(0)
        self._sock.bind(("0.0.0.0", port))

    def onUpdate(self):
        while self._running:
            try:
                data, addr = self._sock.recvfrom(4068)

                reply = self.onDataReceive(addr, data)
                if reply:
                    self._sock.sendto(reply, addr)
            except BlockingIOError:
                pass

    def onDataReceive(self, addr, data):
        pass