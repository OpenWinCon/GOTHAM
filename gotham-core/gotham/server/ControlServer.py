# encoding: utf-8

from gotham.net.netscan import *
from gotham.Storage import Storage
from gotham.util.net import UDPServer, UDPClient

import time

__author__ = 'BetaS'

PORT = 15961


class ControlServer(UDPServer):
    NODE_TIMEOUT = 10*60

    def __init__(self):
        super().__init__(b"bat0", PORT)

    def onDataReceive(self, addr, data):
        frame = UDPControlFrame.parse(data)

        if frame.command == UDPCommandType.CMD_NETSCAN:
            if frame.type == UDPMessageType.TYPE_REQUEST:
                request = NetScanRequestFrame.parse(frame.payload)

                sender = UDPClient(addr[0], PORT)

                timeout = time.time() - self.NODE_TIMEOUT
                q = Storage.get_neighbor_node(timeout)
                nodes = []
                for data in q:
                    if request.level == NetScanRequestLevel.NORMAL:
                        pass

                result = request.reply(nodes)

                sender.send(result)
            elif frame.type == UDPMessageType.TYPE_RESULT:
                pass

        print(data)
