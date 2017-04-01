# encoding: utf-8

from gotham.util.net import HTTPServer
import json

__author__ = 'BetaS'


def node_info(param):
    data = {}
    return json.dumps(data)


WEB_RES = {
    "/": "index.html",
    "/login": "login.html",
}
XHR_RES = {
    "/node_info": node_info,
}

server = HTTPServer("0.0.0.0", 5000, "web-res/", WEB_RES, XHR_RES)
