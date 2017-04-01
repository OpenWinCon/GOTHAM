# encoding: utf-8

import struct
from ..hashutil import crc32
from .HMAC import HMAC

__author__ = 'BetaS'


class EthernetFrame:
    src = HMAC(0)
    dst = HMAC(0)
    type = 0
    payload = bytes()

    @classmethod
    def build(cls, src, dst, type, payload):
        packet = bytes()

        packet += struct.pack("6s", bytes(dst))
        packet += struct.pack("6s", bytes(src))
        packet += struct.pack(">H", type)
        packet += payload
        packet += struct.pack(">I", crc32(payload))

        return packet

    @classmethod
    def parse(cls, p):
        data = EthernetFrame()

        data.dst = HMAC(struct.unpack("6p", p[0:6])[0])
        data.src = HMAC(struct.unpack("6p", p[6:12])[0])
        data.type = struct.unpack(">H", p[12:14])[0]
        data.payload = p[14:-4]
        crc = struct.unpack(">I", p[-4:])[0]

        if crc == crc32(data.payload):
            return data
        else:
            return None
