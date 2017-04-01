# encoding; utf-8

from enum import Enum
import struct

from gotham.util.net import IPv4

__author__ = 'BetaS'

GOTHAM_PACKET_VER = 1


class GothamFrame:
    class Type(Enum):
        TYPE_NONE   = 0x0000
        TYPE_ALIVE  = 0x0001
        TYPE_UPDATE = 0x0002

        TYPE_INFO   = 0x0010

    type = 0
    ver = 0
    payload = bytes()

    @classmethod
    def build(cls, type, payload):
        packet = bytes()

        packet += struct.pack(">I", 0xAABCDEFF)
        packet += struct.pack(">h", type.value)
        packet += struct.pack(">h", GOTHAM_PACKET_VER)
        packet += struct.pack(">h", len(payload))
        packet += payload

        return packet

    @classmethod
    def parse(cls, p):
        data = GothamFrame()

        magic = struct.unpack(">I", p[0:4])[0]
        if magic == 0xAABCDEFF:
            data.type = GothamFrame.Type(struct.unpack(">h", p[4:6])[0])
            data.ver = struct.unpack(">h", p[6:8])[0]
            l = struct.unpack(">h", p[8:10])[0]
            data.payload = p[10:10 + l]

            return data
        else:
            return None


class AliveFrame:
    class Status(Enum):
        STATUS_INIT     = 0x00
        STATUS_NORMAL   = 0x01
        STATUS_UPDATE   = 0x02

    @classmethod
    def build(self, ip, core_ver, status, pkg_hash):
        packet = bytes()

        if type(ip) == str:
            ip = IPv4(ip)

        if len(pkg_hash) != 16:
            raise TypeError("pkg_hash's length should be 16 bytes.")

        packet += struct.pack(">I", int(ip))
        packet += struct.pack(">h", core_ver)
        packet += struct.pack(">h", status)
        packet += struct.pack("16p", pkg_hash)

        return GothamFrame.build(GothamFrame.Type.TYPE_ALIVE, packet)

    @classmethod
    def parse(cls, p):
        data = GothamFrame()

        data.ip = IPv4(struct.unpack(">I", p[0:4])[0])
        data.core_ver = struct.unpack(">h", p[4:6])[0]
        data.status = AliveFrame.Status(struct.unpack(">h", p[6:8])[0])
        data.pkg_hash = struct.unpack("16p", p[8:24])[0]

        return data
