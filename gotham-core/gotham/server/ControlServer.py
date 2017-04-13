# encoding: utf-8

import time

from gotham.db import netscan, neighbor
from gotham.net.cmd.netscan import *
from gotham.util.net import UDPServer, TCPServer, TCPClient

__author__ = 'BetaS'

DEV = b"bat0"
PORT = 15961
NODE_TIMEOUT = 10*60


def __run(addr, data):
    frame = ControlFrame.parse(data)

    print("UDP Received")

    if frame.command == CommandType.CMD_NETSCAN:
        print("+ cmd: netscan")

        if frame.type == MessageType.TYPE_REQUEST:
            print("+ type: TYPE_REQUEST")

            request = NetScanRequestFrame.parse(frame.payload)

            sender = TCPClient(addr[0], PORT)

            timeout = time.time() - NODE_TIMEOUT
            q = neighbor.get_node(timeout)
            nodes = []
            for data in q:
                if request.level == NetScanRequestLevel.NORMAL:
                    nodes.append(data)

            result = request.reply(nodes)

            sender.send(result)
        elif frame.type == MessageType.TYPE_RESULT:
            print("+ type: TYPE_RESULT")

            result = NetScanResultFrame.parse(frame.payload)
            netscan.update_data(result)
    else:
        print("[ELSE]", data)

    print()


server = [
    UDPServer(DEV, PORT, __run),
    TCPServer(DEV, PORT, __run)
]


def server_start():
    for s in server:
        s.start()


def server_stop():
    for s in server:
        s.stop()
