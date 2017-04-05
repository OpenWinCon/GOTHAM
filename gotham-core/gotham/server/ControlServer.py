# encoding: utf-8

from gotham.net import UDPControlFrame
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
                sender.send("ack")
            elif frame.type == UDPControlFrame.MessageType.TYPE_RESULT:
                pass

        print(data)
