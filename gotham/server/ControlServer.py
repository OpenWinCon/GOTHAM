# encoding: utf-8

from gotham.util.net import UDPServer, UDPClient

__author__ = 'BetaS'

PORT = 9061


class ControlServer(UDPServer):
    def __init__(self):
        super().__init__(b"bat0", PORT)

    def onDataReceive(self, addr, data):
        if data == b'netscan-request':
            sender = UDPClient(addr[0], PORT)
            sender.send("ack")
        elif data == b'netscan-result':
            pass

        print(data)
