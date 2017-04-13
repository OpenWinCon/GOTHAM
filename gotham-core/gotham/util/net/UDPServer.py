# encoding: utf-8

from gotham.util.threadutil import Thread, Coroutine
import socket

__author__ = 'BetaS'


class UDPServer(Thread):
    def __init__(self, dev, port, handler):
        super().__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, dev)
        self._sock.settimeout(0)
        self._sock.bind(("0.0.0.0", port))
        self._handler = handler

    def onUpdate(self):
        try:
            data, addr = self._sock.recvfrom(4068)
            handler = UDPHandler(self._sock, data, addr, self._handler)
            handler.start()
        except BlockingIOError:
            pass


class UDPHandler(Coroutine):
    def __init__(self, sock, data, addr, handler):
        super().__init__()

        self._sock = sock
        self._addr = addr
        self._data = data
        self._handler = handler

    def onUpdate(self):
        result = self._handler(self._addr, self._data)

        if result and len(result) > 0:
            self._sock.sendto(result, self._addr)
