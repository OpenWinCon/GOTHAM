# encoding: utf-8

from gotham.server import RequestAPI
import enum
import time

__author__ = 'BetaS'


class NodeStatus(enum.Enum):
    STATUS_INIT = 0x00,
    STATUS_NORMAL = 0x10,
    STATUS_WAIT_UPDATE = 0x11,


class NodeInfo:
    ip = None
    ver = 0
    status = NodeStatus.STATUS_INIT
    last_seen = time.time()
    hash = ""

    def __init__(self, packet):
        self.update(packet)
        self._request_update()

    def update(self, packet):
        self.ip = packet.ip
        self.ver = packet.ver
        self.last_seen = time.time()

        if self.status == NodeStatus.STATUS_NORMAL:
            if self.hash != packet.pkg_hash:
                self._request_update()

    def _request_update(self):
        self.status = NodeStatus.STATUS_WAIT_UPDATE
        RequestAPI.send("update " + self.ip, lambda x: self._update_info(x))

    def _update_info(self, info):
        self.status = NodeStatus.STATUS_NORMAL

