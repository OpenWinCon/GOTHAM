# encoding; utf-8

__author__ = "BetaS"


class HMAC(object):
    def __init__(self, val):
        self.__val = val

    def __str__(self):
        a = (self.__val>>40)&0xFF
        b = (self.__val>>32)&0xFF
        c = (self.__val>>24)&0xFF
        d = (self.__val>>16)&0xFF
        e = (self.__val>>8)&0xFF
        f = self.__val&0xFF

        return "%02x:%02x:%02x:%02x:%02x:%02x" % (a, b, c, d, e, f)

    def __bytes__(self):
        a = (self.__val>>40)&0xFF
        b = (self.__val>>32)&0xFF
        c = (self.__val>>24)&0xFF
        d = (self.__val>>16)&0xFF
        e = (self.__val>>8)&0xFF
        f = self.__val&0xFF

        return bytes([a,b,c,d,e,f])

    @classmethod
    def parse(cls, str=""):
        data = HMAC(0)
        s = str.split(":")

        if len(s) != 6:
            raise ValueError("invalid mac address format "+s)

        for i in s:
            i = int(i, base=16)
            if not 0 <= i <= 255:
                raise ValueError("invalid octet for %d" % i)
            data.__val <<= 8
            data.__val += i

        return data