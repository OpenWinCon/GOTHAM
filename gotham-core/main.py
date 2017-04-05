# encoding: utf-8

from gotham.server.BaseServer import BaseServer

__author__ = 'BetaS'

server = BaseServer("bat0")


def start():
    print("[!] START")
    server.start()


def stop():
    print("[!] STOPPED")
    server.stop()


if __name__ == "__main__":
    while True:
        cmds = input("> ")
        if cmds == "start":
            start()
        elif cmds == "stop":
            stop()
        elif cmds == "quit":
            break