import json


def redirect_to():
    pass

def response(http, data={}, cookies={}):
    http.send_response(200)
    http.send_header('Content-type', 'text/json')
    cookie_str = ""
    for c in cookies:
        cookie_str += c+"="+cookies[c]+";"

    if len(cookie_str) > 0:
        print("set cookie", cookie_str)
        http.send_header('Set-Cookie', cookie_str)

    http.end_headers()
    http.wfile.write(json.dumps(data).encode('utf-8'))

    return True

def error(http, code, msg, data={}):
    result = {
        "code": code,
        "message": msg,
        "data": data
    }

    http.send_response(500)
    http.send_header('Content-type', 'text/json')
    http.end_headers()
    http.wfile.write(json.dumps(result).encode('utf-8'))

    return True