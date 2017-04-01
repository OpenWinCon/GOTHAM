# encoding: utf-8

from gotham.util import deviceutil, AsyncTimer, Thread
from gotham.util.net import L2Socket
from gotham.net import GothamFrame, AliveFrame
from gotham.model.NodeInfo import *
from gotham.Storage import Storage
from queue import Queue

__author__ = 'BetaS'


class BaseServer(Thread):
    """
    BaseServer
    1. listen l2 frames for updating neighbor nodes info
    2. periodically (10 secs) sends broadcast frame for notify itself
    """

    GOTHAM_VER = 1

    def __init__(self, dev):
        super().__init__()

        self._q = Queue()
        self._sock = L2Socket(dev, self._q, 0xFF01)
        self._broadcast_timer = AsyncTimer(5)
        self._node_info = Storage.nodes()

        self.dev = dev
        self.status = 1

    def is_running(self):
        return self._thread.is_alive()

    def _update_node(self, node, result):
        node.update(result)
        node.status = NodeStatus.STATUS_NORMAL

    def _receive_broadcast(self, src, packet):
        if not src in self._node_info:
            self._node_info[src] = NodeInfo(packet)
        else:
            self._node_info[src].update(packet)

    def _send_broadcast(self):
        # Send Broadcast
        iface = deviceutil.iface()

        if self.dev in iface:
            i = iface[self.dev]
            if "bridge" in i and "avahi" in i["bridge"]:
                ip = i["bridge"]["avahi"]["ipv4"]
            else:
                ip = i["ipv4"]

            node_hash = b'0000000000000000'#hashutil.dict_hash(iface)

            payload = AliveFrame.build(ip, self.GOTHAM_VER, self.status, node_hash)
            self._sock.broadcast(payload)

    def onStart(self):
        self._sock.listen_start()

    def onStop(self):
        self._sock.listen_stop()

    def onUpdate(self):
        if not self._q.empty():
            src, data = self._q.get_nowait()
            data = GothamFrame.parse(data)
            if data and data.type == GothamFrame.Type.TYPE_ALIVE:
                self._receive_broadcast(src, AliveFrame.parse(data.payload))

        if self._broadcast_timer.check():
            self._send_broadcast()
