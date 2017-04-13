# encoding; utf-8

from .. import *
from .defines import *
from gotham.net import *

__author__ = 'BetaS'


class NetScanRequestFrame:
    level = NetScanRequestLevel.NONE
    timestamp = time.time()

    @classmethod
    def build(cls, level):
        payload = bytes()
        payload += struct.pack(">B", level.value)
        payload += struct.pack(">f", time.time())
        return ControlFrame.build(CommandType.CMD_NETSCAN, MessageType.TYPE_REQUEST, 1, payload)

    @classmethod
    def parse(cls, p):
        data = NetScanRequestFrame()
        data.level = NetScanRequestLevel(struct.unpack(">B", p[0:1])[0])
        data.timestamp = struct.unpack(">f", p[1:5])[0]
        return data

    def reply(self, nodes):
        return NetScanResultFrame.build(self.level, self.timestamp, nodes)


class NetScanResultFrame:
    level = 0
    timestamp = time.time()
    node_time = time.time()
    node_cnt = 0
    nodes = list()

    @classmethod
    def build(cls, level, timestamp, nodes):
        payload = bytes()

        payload += struct.pack(">B", level.value)
        payload += struct.pack(">f", timestamp)
        payload += struct.pack(">f", time.time())
        payload += struct.pack(">B", len(nodes)+1)
        payload += struct.pack(">I", int(PacketPreference.NODE_IP))
        payload += PacketPreference.NODE_NAME.encode()
        payload += b'\x00'
        for node in nodes:
            payload += struct.pack(">I", int(node["ip"]))
            payload += node["name"].encode()
            payload += b'\x00'

        return ControlFrame.build(CommandType.CMD_NETSCAN, MessageType.TYPE_RESULT, 1, payload)

    @classmethod
    def parse(cls, p):
        data = NetScanResultFrame()
        data.nodes = list()

        data.level = struct.unpack(">B", p[0:1])[0]
        data.timestamp = struct.unpack(">f", p[1:5])[0]
        data.node_time = struct.unpack(">f", p[5:9])[0]
        data.node_cnt = struct.unpack(">B", p[9:10])[0]

        i = 10
        while i < len(p):
            node = dict()
            node['ip'] = IPv4(struct.unpack(">I", p[i+0:i+4])[0])

            z = 0
            while p[i+4+z] != 0x00:
                z += 1
            node['name'] = p[i+4:i+4+z]

            data.nodes.append(node)
            i = i+4+z+1

        return data
