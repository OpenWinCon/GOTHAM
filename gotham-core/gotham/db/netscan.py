#encoding: utf-8

from . import _db
import enum
import time
import logging


LOGGER = logging.getLogger(__name__)

__author__ = 'BetaS'


class NodeStatus(enum.Enum):
    STATUS_UNCONSCIOUS = 0x00
    STATUS_ALIVE = 0x01


class ConnectionStatus(enum.Enum):
    STATUS_LOST = 0x00
    STATUS_OLD  = 0x01
    STATUS_FRESH = 0x02


def update_node(ip, hostname, status, request_time, response_time):
    db = _db.netscan_node

    data = db.find_one({"name": hostname})

    node_info = {
        "ip": ip,
        "name": hostname,
        "status": status.value,
        "request_time": request_time,
        "response_time": response_time
    }

    # 이미 정보 있는지 여부 체크
    if data:
        # 요청 시기가 최신인 경우에만
        if data["request_time"] <= request_time:
            # 직접 들어온것인지 간접으로 들어온것인지 확인
            if status == NodeStatus.STATUS_ALIVE:
                # 직접 응답인경우 노드 시간 체크후 최신인 경우만 정보 업데이트
                if data["response_time"] <= response_time:
                    db.update({"name": hostname}, {"$set": node_info})

                    LOGGER.info("receive update request (node: %s)" % hostname)
                else:
                    LOGGER.debug("drop update request (node: %s, cause: old response time)" % hostname)
        else:
            LOGGER.debug("drop update request (node: %s, cause: old request time)" % hostname)
    else:
        # 정보 없으므로 신규 등록
        db.insert(node_info)

        LOGGER.info("receive insert request (node: %s)" % hostname)


def update_connection(origin, target, request_time, response_time):
    db = _db.netscan_conn

    src = {"src": origin, "dst": target}
    data = db.find_one(src)

    # 이미 정보 있는지 여부 체크
    if data:
        # 요청 시기가 최신인 경우에만
        if data["request_time"] <= request_time:
            # 노드 시간 최신인 경우만 정보 업데이트
            if data["response_time"] <= response_time:
                data = {
                    "request_time": request_time,
                    "response_time": response_time,
                    "update_time": time.time()
                }

                db.update(src, {"$set": data})

                LOGGER.info("connection update (%s -> %s)" % (origin, target))

            else:
                LOGGER.debug("drop connection update (%s -> %s, cause: old response time)" % (origin, target))
        else:
            LOGGER.debug("drop update request (%s -> %s, cause: old request time)" % (origin, target))
    else:
        # 정보 없으므로 신규 등록
        data = {
            "request_time": request_time,
            "response_time": response_time,
            "update_time": time.time()
        }
        data.update(src)

        db.insert(data)

        LOGGER.info("connection update (%s -> %s)" % (origin, target))


def update_data(result):
    origin = result.nodes[0]
    nodes = list()
    if len(result.nodes) > 1:
        nodes = result.nodes[1:]

    request_time = result.timestamp
    response_time = result.node_time

    # 응답자 소스 정보 업데이트
    update_node(str(origin["ip"]), origin["name"].decode("utf-8"), NodeStatus.STATUS_ALIVE, request_time, response_time)

    for node in nodes:
        # 응답자 인접 노드 정보 추가
        update_node(str(node["ip"]), node["name"].decode("utf-8"), NodeStatus.STATUS_UNCONSCIOUS, request_time, 0)

        # 연결정보 추가
        update_connection(origin["name"].decode("utf-8"), node["name"].decode("utf-8"), request_time, response_time)
