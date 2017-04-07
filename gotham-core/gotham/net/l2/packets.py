# encoding; utf-8

from .defines import *
from .. import *

from gotham.util.net import IPv4

__author__ = 'BetaS'


class GothamFrame:
    type = GothamFrameType()
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
            data.type = GothamFrameType(struct.unpack(">B", p[4:5])[0])
            data.ver = struct.unpack(">B", p[5:6])[0]
            l = struct.unpack(">H", p[6:8])[0]
            data.payload = p[8:8 + l]

            return data
        else:
            return None


class AliveFrame:
    ip = IPv4()
    core_ver = 0
    status = 0
    pkg_hash = ""
    hostname = ""

    @classmethod
    def build(cls, core_ver, status, pkg_hash):
        packet = bytes()

        if len(pkg_hash) != 16:
            raise TypeError("pkg_hash's length should be 16 bytes.")

        packet += struct.pack(">I", int(PacketPreference.NODE_IP))
        packet += struct.pack(">H", core_ver)
        packet += struct.pack(">H", status)
        packet += struct.pack("16p", pkg_hash)
        packet += PacketPreference.NODE_NAME.encode()
        packet += b'\x00'

        return GothamFrame.build(GothamFrameType.TYPE_ALIVE, 0x0001, packet)

    @classmethod
    def parse(cls, p):
        data = AliveFrame()

        data.ip = IPv4(struct.unpack(">I", p[0:4])[0])
        data.core_ver = struct.unpack(">H", p[4:6])[0]
        data.status = AliveFrame.Status(struct.unpack(">H", p[6:8])[0])
        data.pkg_hash = struct.unpack("16p", p[8:24])[0]
        data.hostname = p[24:-1]

        return data
