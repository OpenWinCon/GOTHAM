# encoding; utf-8

from enum import Enum

__author__ = 'BetaS'


class MessageType(Enum):
    TYPE_NOREPLY = 0x0000
    TYPE_REQUEST = 0x8000
    TYPE_RESULT = 0xC000


class CommandType(Enum):
    NONE        = 0x0000
    CMD_NETSCAN = 0x0001


MASK_MESSAGE_TYPE = 0xC000
MASK_COMMAND_TYPE = 0x3FFF
