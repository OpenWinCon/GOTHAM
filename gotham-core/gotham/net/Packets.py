# encoding; utf-8

from enum import Enum
import struct
import time

from gotham.util.net import IPv4

__author__ = 'BetaS'


class PacketPreference:
    NODE_IP = None
    NODE_NAME = None


class GothamFrame:
    class Type(Enum):
        TYPE_NONE   = 0x00
        TYPE_ALIVE  = 0x01
        TYPE_UPDATE = 0x02

        TYPE_INFO   = 0x10

    type = 0
    ver = 0
    payload = bytes()

    @classmethod
    def build(cls, type, ver, payload):
        packet = bytes()

        packet += struct.pack(">I", 0xF90DDA3F)
        packet += struct.pack(">B", type.value)
        packet += struct.pack(">B", ver)
        packet += struct.pack(">H", len(payload))
        packet += payload

        return packet

    @classmethod
    def parse(cls, p):
        data = GothamFrame()

        magic = struct.unpack(">I", p[0:4])[0]
        if magic == 0xAABCDEFF:
            data.type = GothamFrame.Type(struct.unpack(">B", p[4:5])[0])
            data.ver = struct.unpack(">B", p[5:6])[0]
            l = struct.unpack(">H", p[6:8])[0]
            data.payload = p[8:8 + l]

            return data
        else:
            return None


class AliveFrame:
    class Status(Enum):
        STATUS_INIT     = 0x00
        STATUS_NORMAL   = 0x01
        STATUS_UPDATE   = 0x02

    @classmethod
    def build(cls, core_ver, status, pkg_hash):
        packet = bytes()

        if type(ip) == str:
            ip = IPv4(ip)

        if len(pkg_hash) != 16:
            raise TypeError("pkg_hash's length should be 16 bytes.")

        packet += struct.pack(">I", int(PacketPreference.NODE_IP))
        packet += struct.pack(">H", core_ver)
        packet += struct.pack(">H", status)
        packet += struct.pack("16p", pkg_hash)
        packet += PacketPreference.NODE_NAME.encode()
        packet += b'\x00'

        return GothamFrame.build(GothamFrame.Type.TYPE_ALIVE, 0x0001, packet)

    @classmethod
    def parse(cls, p):
        data = AliveFrame()

        data.ip = IPv4(struct.unpack(">I", p[0:4])[0])
        data.core_ver = struct.unpack(">H", p[4:6])[0]
        data.status = AliveFrame.Status(struct.unpack(">H", p[6:8])[0])
        data.pkg_hash = struct.unpack("16p", p[8:24])[0]
        data.hostname = p[24:-1]

        return data


class UDPControlFrame:
    class MessageType(Enum):
        TYPE_NOREPLY = 0x0000
        TYPE_REQUEST = 0x8000
        TYPE_RESULT  = 0xC000

    class CommandType(Enum):
        CMD_NETSCAN = 0x0001

    MASK_MESSAGE_TYPE = 0xC000
    MASK_COMMAND_TYPE = 0x3FFF

    @classmethod
    def build(cls, command, type, ver, payload):
        packet = bytes()

        packet += struct.pack(">H", type.value | command.value)
        packet += struct.pack(">B", ver)
        packet += payload

        return packet

    @classmethod
    def parse(cls, p):
        data = UDPControlFrame()

        cmd = struct.unpack(">H", p[0:2])[0]

        data.command = UDPControlFrame.CommandType(cmd & cls.MASK_COMMAND_TYPE)
        data.type = UDPControlFrame.MessageType(cmd & cls.MASK_MESSAGE_TYPE)
        data.ver = struct.unpack(">B", p[2:3])[0]
        data.payload = p[3:]

        return data


class NetScanRequestFrame:
    @classmethod
    def build(cls, level):
        payload = bytes()
        payload += struct.pack(">B", level)
        payload += struct.pack(">f", time.time())
        return UDPControlFrame.build(UDPControlFrame.CommandType.CMD_NETSCAN, UDPControlFrame.MessageType.TYPE_REQUEST, 1, payload)

    @classmethod
    def parse(cls, p):
        data = NetScanRequestFrame()
        data.level = struct.unpack(">B", p[0:1])[0]
        data.time = struct.unpack(">f", p[1:5])[0]
        return data

    def reply(self, nodes):
        NetScanResultFrame(self.level, self.time, nodes)


class NetScanResultFrame:
    @classmethod
    def build(cls, level, t, nodes):
        payload = bytes()

        payload += struct.pack(">B", level)
        payload += struct.pack(">f", t)
        payload += struct.pack(">f", time.time())
        payload += struct.pack(">B", len(nodes)+1)
        payload += struct.pack(">I", int(PacketPreference.NODE_IP))
        payload += PacketPreference.NODE_NAME.encode()
        payload += b'\x00'
        for node in nodes:
            payload += struct.pack(">I", int(node.ip))
            payload += node.name.encode()
            payload += b'\x00'

        return UDPControlFrame.build(UDPControlFrame.CommandType.CMD_NETSCAN, UDPControlFrame.MessageType.TYPE_RESULT, 1, payload)

    @classmethod
    def parse(cls, p):
        data = NetScanResultFrame()
        data.nodes = list()

        data.level = struct.unpack(">B", p[0:1])[0]
        data.original_time = struct.unpack(">f", p[1:5])[0]
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
