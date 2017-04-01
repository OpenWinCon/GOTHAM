# encoding; utf-8

__author__ = "BetaS"


class IPv4:
    def __init__(self, val):
        if type(val) == int:
            self.__val = val
        elif type(val) == str:
            s = val.split(".")
            self.__val = 0

            if len(s) != 4:
                raise ValueError("invalid ip address format")

            for i in s:
                i = int(i)
                if not 0 <= i <= 255:
                    raise ValueError("invalid octet for %d" % i)
                self.__val <<= 8
                self.__val += i
        else:
            raise Exception()

    def __str__(self):
        a = (self.__val>>24)&0xFF
        b = (self.__val>>16)&0xFF
        c = (self.__val>>8)&0xFF
        d = self.__val&0xFF

        return "%d.%d.%d.%d"%(a,b,c,d)

    def __int__(self):
        return int(self.__val)
