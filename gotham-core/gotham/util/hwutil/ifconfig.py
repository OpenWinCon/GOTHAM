import subprocess

def autoip(nic):
    subprocess.Popen(["avahi-autoipd", nic, "&"])


class Interface:
    def __init__(self, name):
        self.name = name

    def call(self, *args):
        li = ["ifconfig", self.name]
        for idx, cmd in enumerate(args):
            li.append(cmd)
        subprocess.Popen(li)

    def up(self):
        self.call("up")
        return self

    def down(self):
        self.call("down")
        return self

    def set_mtu(self, mtu=1527):
        self.call("mtu", mtu)

    def set_ip(self, ip="0.0.0.0", subnet="255.255.255.0"):
        self.call(ip)
