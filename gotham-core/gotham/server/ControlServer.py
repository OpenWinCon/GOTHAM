# encoding: utf-8

from gotham.net import UDPControlFrame, NetScanRequestFrame, NetScanResultFrame
from gotham.Storage import Storage
from gotham.util.net import UDPServer, UDPClient

__author__ = 'BetaS'

PORT = 15961


class ControlServer(UDPServer):
    def __init__(self):
        super().__init__(b"bat0", PORT)

    def onDataReceive(self, addr, data):
        frame = UDPControlFrame.parse(data)

        if frame.command == UDPControlFrame.CommandType.CMD_NETSCAN:
            if frame.type == UDPControlFrame.MessageType.TYPE_REQUEST:
                sender = UDPClient(addr[0], PORT)

                nodes = Storage.get_neighbor_nodes()

                request = NetScanRequestFrame.parse(frame.payload)
                result = request.reply(nodes)

                sender.send(result)
            elif frame.type == UDPControlFrame.MessageType.TYPE_RESULT:
                pass

        print(data)
