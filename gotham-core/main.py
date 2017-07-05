# encoding: utf-8

from gotham.server.BaseServer import BaseServer
import gotham.server.ControlServer as control_server
import gotham.server.HttpServer as http_server
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

base_server = None

DEV = b"bat0"
PORT = 15961

def start():
    print("[!] START")
    base_server.start()
    control_server.server_start()
    http_server.start()


def stop():
    print("[!] STOPPED")
    base_server.stop()
    control_server.server_stop()
    http_server.stop()


if __name__ == "__main__":
    path = "gotham.json"

    if len(sys.argv) > 1:
        path = sys.argv[1]

    nic_list = boot.boot(path)

    base_server = BaseServer(nic_list["adhoc"][0])
    control_server.server_init(DEV, PORT)
    http_server.server_init(5000, PORT)

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
