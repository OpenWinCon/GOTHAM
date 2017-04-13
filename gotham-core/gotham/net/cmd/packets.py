# encoding; utf-8

import time
from .defines import *
from gotham.net import *

__author__ = 'BetaS'


class ControlFrame:
    command = MessageType.TYPE_NOREPLY
    type = CommandType.NONE
    ver = 0
    payload = bytes()

    @classmethod
    def build(cls, command, type, ver, payload):
        packet = bytes()

        packet += struct.pack(">H", type.value | command.value)
        packet += struct.pack(">B", ver)
        packet += payload

        return packet

    @classmethod
    def parse(cls, p):
        data = ControlFrame()

        cmd = struct.unpack(">H", p[0:2])[0]

        data.command = CommandType(cmd & MASK_COMMAND_TYPE)
        data.type = MessageType(cmd & MASK_MESSAGE_TYPE)
        data.ver = struct.unpack(">B", p[2:3])[0]
        data.payload = p[3:]

        return data
