# encoding: utf-8

from socket import *

__author__ = 'BetaS'


class TCPClient:
    def __init__(self, ip, port):
        self._sock = socket(AF_INET, SOCK_STREAM)
        self._sock.setsockopt(SOL_SOCKET, SO_BINDTODEVICE, b'bat0')
        self._addr = (ip, port)

    def send(self, message):
        if type(message) == bytes:
            pass
        elif type(message) == str:
            message = message.encode()
        else:
            raise TypeError("message must be bytes or str")

        self._sock.connect(self._addr)
        self._sock.send(message)
        self._sock.close()
