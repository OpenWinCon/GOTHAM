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
    mac = None
    ip = None
    hostname = None
    ver = 0
    status = NodeStatus.STATUS_INIT
    last_seen = time.time()
    hash = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def __init__(self, src, packet):
        self.mac = src
        self.update(packet)
        self._request_update()

    def update(self, packet):
        self.ip = packet.ip
        self.hostname = packet.hostname
        self.ver = packet.ver
        self.status = packet.status
        self.last_seen = time.time()

        neighbor.update_node(self.mac, self.ip, self.hostname, self.ver, self.status, self.last_seen)

        if self.status == NodeStatus.STATUS_NORMAL:
            if self.hash != packet.pkg_hash:
                self._request_update()

    def _request_update(self):
        self.status = NodeStatus.STATUS_WAIT_UPDATE
        RequestAPI.send("update " + self.ip, lambda x: self._update_info(x))

    def _update_info(self, info):
        self.status = NodeStatus.STATUS_NORMAL

