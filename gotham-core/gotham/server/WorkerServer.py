# encoding: utf-8

from gotham.util.net import MessageServer

__author__ = 'BetaS'


class WorkerServer(MessageServer):
    def __init__(self):
        super().__init__("gotham_rpc")

    def consume(self, body):
        print(body)
        return body[4:]
