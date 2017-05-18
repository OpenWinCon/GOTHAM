# encoding: utf-8

from gotham.server.BaseServer import BaseServer
import gotham.server.ControlServer as control_server
from gotham.util.net.UDPClient import UDPClient
from gotham.net.cmd.netscan import *
import boot
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


def start():
    print("[!] START")
    server.start()
    control_server.server_start()


def stop():
    print("[!] STOPPED")
    server.stop()
    control_server.server_stop()


if __name__ == "__main__":
    path = "gotham.json"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    nic_list = boot.boot(path)

    server = BaseServer(nic_list["adhoc"][0])
    control_server.server_init()
    start()

    test_client = UDPClient('169.254.255.255', 15961)

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
            test_client.send(payload)
