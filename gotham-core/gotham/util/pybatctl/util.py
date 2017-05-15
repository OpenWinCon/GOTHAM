#encoding: utf-8

__author__ = "BetaS"

import subprocess
import re

class RunCommandError(Exception):
    def __init__(self, full_command, errors):

        # Call the base class constructor with the parameters it needs
        super(RunCommandError, self).__init__({"cmd" : " ".join(full_command), "msg": errors})

    def __str__(self):
        return "(Command: \""+self.message["cmd"]+"\")\n\n"+self.message["msg"]

def run_command(cmd=[]):
    cmd = map(lambda x: str(x), cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = proc.stderr.read()
    if len(err) > 0:
        raise RunCommandError(cmd, err)

    return proc.stdout.readlines()

def mtu_get(dev="wlan0"):
    result = run_command(["ip", "link", "show", dev])
    if len(result) > 0:
        m = re.search(r"mtu\s(\d+?)\s", result[0], re.IGNORECASE)
        if m:
            mtu = int(m.group(1))
            return mtu
        else:
            return False

    return False

def mtu_set(dev="wlan0", mtu=1500):
    result = run_command(["ip", "link", "set", "mtu", mtu, dev])
    if len(result) == 0:
        return True
    return False

def nic_get_status(dev="wlan0"):
    result = run_command(["ip", "link", "show", dev])
    if len(result) > 0:
        m = re.search(r"state\s(.+?)\s", result[0], re.IGNORECASE)
        if m:
            if m.group(1).lower() == "up":
                return "UP"
            else:
                return "DOWN"
        else:
            return "ERR"

    return "NODEV"

def nic_set_status(dev="wlan0", up=True):
    if up == True: up = "up"
    else: up = "down"

    result = run_command(["ip", "link", "set", up, dev])
    if len(result) == 0:
        return True
    return False

def adhoc_broadcast(dev="wlan0", node_name="adhoc", channel=5):
    nic_set_status(dev, False)
    result = run_command(["iwconfig", dev, "mode", "ad-hoc", "essid", node_name, "channel", channel])
    nic_set_status(dev, True)

    if len(result) == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    print(adhoc_broadcast("wlan0"))

    #print nic_set_status("wlan0", False)
    #print nic_get_status("wlan0")