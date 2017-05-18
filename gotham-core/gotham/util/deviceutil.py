# encoding: utf-8

import socket, psutil

__author__ = 'BetaS'


def iface():
    iface = psutil.net_if_addrs()
    data = {}
    for k in iface:
        name = k.split(":")

        d = {}
        for s in iface[k]:
            if s.family == socket.AF_INET:
                d["ipv4"] = s.address
            elif s.family == socket.AF_PACKET:
                d["hmac"] = s.address

        if len(name) > 1:
            if not name[0] in data:
                data[name[0]] = {}

            if not "bridge" in data[name[0]]:
                data[name[0]]["bridge"] = {}
            data[name[0]]["bridge"][name[1]] = d
        else:
            if not k in data:
                data[k] = d
            else:
                data[k].update(d)

    return data


if __name__ == "__main__":
    print(iface())