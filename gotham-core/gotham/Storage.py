# encoding: utf-8
import pymongo
import time

__author__ = 'BetaS'


class Storage:
    _db = pymongo.MongoClient('/tmp/mongodb-27017.sock').gotham

    @classmethod
    def node(cls, src):
        return NodeSelector(cls._db.nodes, src)

    @classmethod
    def nodes(cls):
        return cls._db.nodes

    @classmethod
    def update_neighbor_node(cls, mac, ip, hostname, ver, status, t):
        node_info = {
            "src": mac,
            "ip": ip,
            "name": hostname,
            "ver": ver,
            "status": status,
            "last_seen": t
        }

        return cls._db.neighbor_nodes.update(node_info, {"src": mac}, upsert=True)

    @classmethod
    def get_neighbor_node(cls, limit_time):
        return cls._db.neighbor_nodes.find({"last_seen": {"$gte": limit_time}})

    @classmethod
    def node_add(cls, src, ip, hash):
        cls._db.nodes.insert({"src": src, "ip": ip, "hash": hash})

    @classmethod
    def get_node_ip(cls):
        return cls._rds.get("ip")

    @classmethod
    def get_gotham_ver(cls):
        return 1


class NodeSelector:
    def __init__(self, db, src):
        self._db = db
        self.src = src

    def update(self):
        self._db.update_one({"src": self.src}, {'$set': {'last_seen': time.time()}})

    def request_update(self):
        pass
