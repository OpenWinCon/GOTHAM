#encoding: utf-8

from . import _db

__author__ = 'BetaS'


def update_node(mac, ip, hostname, ver, status, t):
    node_info = {
        "src": str(mac),
        "ip": str(ip),
        "name": hostname,
        "ver": ver,
        "status": status.value,
        "last_seen": t
    }
    print(node_info)
    return _db.neighbor_nodes.update({"src": str(mac)}, {"$set": node_info}, upsert=True)


def get_node(limit_time):
    return _db.neighbor_nodes.find({"last_seen": {"$gte": limit_time}})
