# encoding: utf-8

from gotham.util import deviceutil, AsyncTimer, Thread
from gotham.util.net import L2Socket
from gotham.net.l2 import *
from gotham.db import neighbor
from queue import Queue
import time

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
        self._sock = L2Socket(dev, self._q, 0xff01)
        self._broadcast_timer = AsyncTimer(5)

        self.dev = dev
        self.status = 1

        self._update_network_info()

    def is_running(self):
        return self._thread.is_alive()

    @staticmethod
    def _receive_broadcast(src, packet):
        ip = packet.ip
        hostname = packet.hostname
        core_ver = packet.core_ver
        status = packet.status

        neighbor.update_node(src, ip, hostname, core_ver, status, time.time())

    def _update_network_info(self):
        iface = deviceutil.iface()

        if self.dev in iface:
            i = iface["bat0"]
            if "bridge" in i and "avahi" in i["bridge"]:
                ip = i["bridge"]["avahi"]["ipv4"]
            else:
                ip = i["ipv4"]

            PacketPreference.NODE_IP = IPv4(ip)
            PacketPreference.NODE_NAME = self._sock.get_hostname()

            return True
        else:
            print("[!] ERROR can't find nic")
            return False

    def _send_broadcast(self):
        if self._update_network_info():
            # Send Broadcast
            node_hash = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'#hashutil.dict_hash(iface)

            payload = AliveFrame.build(self.GOTHAM_VER, self.status, node_hash)
            self._sock.broadcast(payload)

    def onStart(self):
        self._sock.listen_start()

    def onStop(self):
        self._sock.listen_stop()

    def onUpdate(self):
        if not self._q.empty():
            src, data = self._q.get_nowait()
            data = GothamFrame.parse(data)

            if data and data.type == GothamFrameType.TYPE_ALIVE:
                self._receive_broadcast(src, AliveFrame.parse(data.payload))

        if self._broadcast_timer.check():
            self._send_broadcast()
