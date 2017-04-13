# encoding: utf-8

from gotham.util.threadutil import Thread, Coroutine
import socket

__author__ = 'BetaS'


class TCPServer(Thread):
    def __init__(self, dev, port, handler):
        super().__init__()

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE, dev)
        self._sock.settimeout(0)
        self._sock.bind(("0.0.0.0", port))
        self._sock.listen(10)

        self._handler = handler

    def onUpdate(self):
        try:
            sock, addr = self._sock.accept()
            handler = TCPHandler(sock, addr, self._handler)
            handler.start()
        except BlockingIOError:
            pass


class TCPHandler(Coroutine):
    def __init__(self, sock, addr, handler):
        super().__init__()

        self._sock = sock
        self._addr = addr
        self._handler = handler

    def onUpdate(self):
        data = bytes()
        while True:
            buff = self._sock.recv(1024)
            if not buff or len(buff) == 0:
                break
            data += buff

        result = self._handler(self._addr, data)

        if result and len(result) > 0:
            self._sock.send(result)

        self._sock.close()
