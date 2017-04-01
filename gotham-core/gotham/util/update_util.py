# encoding; utf-8

import struct
import os

from gotham.util import crypt_util

__author__ = 'BetaS'

FRAME_SIZE = 1024


def get_framesize(package):
    size = os.path.getsize(package)

    max_frame = (size / FRAME_SIZE)
    if (size % FRAME_SIZE) > 0:
        max_frame += 1

    return max_frame


def get_metadata(package):
    data = ""

    z = open(package)
    data = z.read()
    z.close()

    size = len(data)
    key = crypt_util.sign(data)

    data = struct.pack(">Q", size)
    data += key

    return data


def parse_metadata(data):
    len = struct.unpack(">Q", data[0:8])[0]
    key = data[8:]
    return {"size": len, "hash": key}


def get_frame(frame, package):
    f = open(package)
    f.seek(frame*FRAME_SIZE)
    data = f.read(FRAME_SIZE)
    f.close()
    return data


def validate_data(data, hash):
    return crypt_util.verify(data, hash)
