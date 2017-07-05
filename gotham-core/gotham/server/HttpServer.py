# encoding: utf-8

import json

from gotham.net.cmd.netscan import *
from gotham.util.net import HTTPServer
from gotham.util.net.http.HTTPResponse import *

__author__ = 'BetaS'

api_client = None
server = None


def login_task(http, param):
    id = param['id']
    pw = param['pw']

    if(id == "gotham" and pw == "gotham"):
        return response(http, {}, cookies={"gotham_session": "123412341234"})
    else:
        return error(http, 1, "Login Error")


def node_info(param):
    data = {}
    return json


def update_netscan():
    payload = NetScanRequestFrame.build(NetScanRequestLevel.NORMAL)
    api_client.send(payload)

    data = {}

    return json


XHR_RES = {
    "/action/login": login_task,
    "/update_netscan": update_netscan,
    "/node_info": node_info,
}


def server_init(port, control_port):
    global api_client, server

    #api_client = UDPClient('169.254.255.255', control_port)
    server = HTTPServer("0.0.0.0", port, "./web-res", XHR_RES)


def start():
    server.start()

def stop():
    server.stop()


if __name__ == "__main__":
    server_init(5000, 15964)
    start()

    while True:
        pass