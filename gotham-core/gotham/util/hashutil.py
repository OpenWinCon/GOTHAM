# encoding: utf-8

from hashlib import md5
import zlib
import json

__author__ = 'BetaS'


def dict_hash(d):
    return md5(json.dumps(d, sort_keys=True).encode()).digest()


def hash_to_hex(bs):
    res = ""
    for b in bs:
        res += "%02x" % b
    return res


def crc32(data):
    return zlib.crc32(data) & 0xFFFFFFFF
