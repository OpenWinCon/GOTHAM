# encoding; utf-8

from enum import Enum

__author__ = 'BetaS'


class NodeStatus(Enum):
    STATUS_INIT = 0x00
    STATUS_NORMAL = 0x01
    STATUS_UPDATE = 0x02


class GothamFrameType(Enum):
    TYPE_NONE   = 0x00
    TYPE_ALIVE  = 0x01
    TYPE_UPDATE = 0x02

    TYPE_INFO   = 0x10