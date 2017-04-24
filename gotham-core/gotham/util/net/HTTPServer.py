# encoding: utf-8

import http.server
from urllib.parse import urlparse, parse_qs
from gotham.util.threadutil import Coroutine

__author__ = 'BetaS'


def handler_factory(base_path, static_res, dynamic_res):
    _base_path = base_path
    _res = dict()
    _res["web"] = static_res
    _res["xhr"] = dynamic_res

    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            path = ""
            if self.path in _res["web"]:
                path = _res["web"][self.path]

            if len(path) > 0:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(_base_path+path) as f:
                    self.wfile.write(f.read().encode())
            else:
                query_components = parse_qs(urlparse(self.path).query)

                self.path = urlparse(self.path).path
                print(self.path, query_components)
                if self.path in _res["xhr"]:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/json')
                    self.end_headers()
                    self.wfile.write(_res["xhr"][self.path](query_components))
                else:
                    self.send_response(403)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

    return HTTPHandler

class HTTPServer(Coroutine):
    def __init__(self, ip, port, base_path, static_res, dynamic_res):
        super().__init__()

        self._server = http.server.HTTPServer((ip, port), handler_factory(base_path, static_res, dynamic_res))

    def onStart(self):
        self._server.serve_forever()

    def onStop(self):
        self._server.server_close()


