import time
import random

def generate_sess_id():
    id = ""
    for i in range(32):
        j = random.randrange(26+26+10)
        if j < 10:
            id += str(j)
        elif j < 10+26:
            id += chr(ord('A')+(j-10))
        elif j < 10+26+26:
            id += chr(ord('a')+(j-10-26))
    return id

SESSION_TIMEOUT = 1*60*60 # 1 hour

class HTTPSessionItem:
    def __init__(self, ip, sess_id):
        self.id = sess_id
        self.ip = ip
        self.timeout = time.time()
        self.data = {}

    def check_available(self, ip):
        if(time.time() - self.timeout) >= SESSION_TIMEOUT:
            return False
        elif(self.ip != ip):
            return False

        self.timeout = time.time()
        return True

    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)

    def __getitem__(self, item):
        return self.data.__getitem__(item)


class HTTPSession:
    def __init__(self):
        self.sess = {}

    def create_session(self, ip, sess_id):
        item = HTTPSessionItem(ip, sess_id)
        self.sess[sess_id] = item
        return item

    def get_session(self, ip, sess_id=""):
        if len(sess_id) == 0:
            # checking uniqueness
            while True:
                sess_id = generate_sess_id()
                if not sess_id in self.sess:
                    break

        if sess_id in self.sess:
            if self.sess[sess_id].check_available(ip):
                return self.sess[sess_id]
            else:
                return self.create_session(ip, sess_id)
        else:
            return self.create_session(ip, sess_id)
