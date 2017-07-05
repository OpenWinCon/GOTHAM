# encoding: utf-8

import mimetypes
import http.server
import cgi
from urllib.parse import urlparse, parse_qsl
from gotham.util.threadutil import Coroutine

__author__ = 'BetaS'


def handler_factory(base_path, dynamic_res):
    _base_path = base_path
    _res = dict()
    _res["xhr"] = dynamic_res

    class HTTPHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query_components = dict(parse_qsl(urlparse(self.path).query, keep_blank_values=True, encoding='utf-8'))

            path = urlparse(self.path).path
            print(path, query_components)

            self.do_REQUEST(path, query_components)

        def do_POST(self):
            path = urlparse(self.path).path

            ctype, pdict = cgi.parse_header(self.headers['content-type'])

            if ctype == 'multipart/form-data':
                postvars = cgi.parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers['content-length'])
                postvars = dict(parse_qsl(self.rfile.read(length).decode('utf-8'), keep_blank_values=True, encoding='utf-8'))
            else:
                postvars = {}

            self.do_REQUEST(path, postvars)

        def do_REQUEST(self, path, query_components):
            # 먼저 요청이 xhr 리스트에 있는지 살펴봄
            if path in _res["xhr"]:
                if not _res["xhr"][path](self, query_components):
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Contents Not Found".encode('utf-8'))

                """
                result = _res["xhr"][path](query_components)
                
                if result:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    
                """
            else:
                # 그 다음으로 요청이 web-res에 있는지 살펴봄
                if path.endswith("/"):
                    path += "index.html"

                try:
                    with open(_base_path+path, 'rb') as f:
                        type = mimetypes.guess_type(path, False)[0]
                        if not type:
                            type = 'text/plain'

                        data = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', type)
                        self.end_headers()
                        self.wfile.write(data)
                except IOError as e:
                    print(e)
                    print("[+]", _base_path+path)
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write("Page Not Found".encode('utf-8'))

    return HTTPHandler

class HTTPServer(Coroutine):
    def __init__(self, ip, port, base_path, dynamic_res):
        super().__init__()

        self._server = http.server.HTTPServer((ip, port), handler_factory(base_path, dynamic_res))

    def onStart(self):
        self._server.serve_forever()

    def onStop(self):
        self._server.server_close()


