import subprocess
from .. import deviceutil

class Interface:
    def __init__(self, name):
        self.name = name

    def call(self, *args):
        li = ["ifconfig", self.name]
        for idx, cmd in enumerate(args):
            li.append(str(cmd))

        subprocess.call(li)

    def up(self):
        self.call("up")
        return self

    def down(self):
        self.call("down")
        return self

    def set_mtu(self, mtu=1527):
        self.call("mtu", mtu)
        return self

    def get_ip(self):
        iface = deviceutil.iface()
        if self.name in iface:
            iface = iface[self.name]
            if "ipv4" in iface:
                return iface["ipv4"]
            elif "bridge" in iface and "ipv4" in iface["bridge"]["avahi"]:
                return iface["bridge"]["avahi"]["ipv4"]

        return None

    def set_ip(self, ip="0.0.0.0", subnet="255.255.255.0"):
        self.call(ip, "netmask", subnet)
        return self

    def set_gw(self, ip="0.0.0.0"):
        subprocess.call(["route", "del", "default", "dev", self.name])
        subprocess.call(["route", "add", "default", "gw", ip, "dev", self.name])
        return self

    def set_masquerade(self, from_dev):
        subprocess.call(["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", self.name, "-j", "SNAT", "--to", self.get_ip()])
        subprocess.call(["iptables", "-A", "FORWARD", "-i", from_dev, "-j", "ACCEPT"])

    def autoip(self):
        subprocess.Popen(["avahi-autoipd", self.name])
        return self

    def set_adhoc(self, ssid, channel):
        subprocess.call(["iwconfig", self.name, "mode", "ad-hoc", "essid", ssid, "channel", str(channel)])
        return self
