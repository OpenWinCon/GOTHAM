# encoding: utf-8

from gotham.server.BaseServer import BaseServer
import gotham.server.ControlServer as control_server
from gotham.util.net.UDPClient import UDPClient
from gotham.net.cmd.netscan import *
import sys
import logging

logger = logging.getLogger("gotham")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

__author__ = 'BetaS'

server = None
client = UDPClient('169.254.255.255', 15961)


def start():
    print("[!] START")
    server.start()
    control_server.server_start()


def stop():
    print("[!] STOPPED")
    server.stop()
    control_server.server_stop()


if __name__ == "__main__":
    iface = "eth0"
    if len(sys.argv) > 1:
        iface = sys.argv[1]

    print("STARTING : ", iface)

    server = BaseServer(iface)
    start()

    while True:
        cmds = input("> ")
        if cmds == "start":
            start()
        elif cmds == "stop":
            stop()
        elif cmds == "quit":
            stop()
            break
        elif cmds == "netscan":
            payload = NetScanRequestFrame.build(NetScanRequestLevel.NORMAL)
            client.send(payload)
