# encoding; utf-8

import psutil
from gotham.util.pybatctl.BATMAN import BATMAN


def check_hostname(target_name):
    import socket
    curr_name = socket.gethostname()

    if curr_name != target_name:
        print(curr_name)
        return False

    return True


def set_hostname(name):
    import subprocess
    subprocess.Popen(["hostnamectl", "set-hostname", name])


def load_json(filename="gotham.json"):
    import json
    with open(filename) as data_file:
        data = json.load(data_file)
        return data
    return None


def reboot():
    print("reboot!")

if __name__ == "__main__":
    try:
        json = load_json()
        # check hostname
        if not check_hostname(json["node_id"]):
            set_hostname(json["node_id"])
            raise RuntimeError("detect hostname difference...")

        # check nic status
        nic_list = {"adhoc": [], "ap": [], "gw": []}
        nic_dev = psutil.net_if_stats()

        for nic in json["nic"]:
            data = json["nic"][nic]

            if not nic in nic_dev:
                raise SystemError("There is no nic for '%s'" % nic)

            if data["type"] == "adhoc":
                nic_list["adhoc"].append(nic)
            elif data["type"] == "ap":
                nic_list["ap"].append(nic)
            elif data["type"] == "gw":
                nic_list["gw"].append(nic)
            else:
                raise SystemError("There is no nic type for '%s'" % data['type'])


        # configure batman-adv
        if len(nic_list["adhoc"]) <= 0:
            raise SystemError("must have 1 or more ad-hoc network interface cards.")

        bat0 = BATMAN("bat0")

        for nic in nic_list["adhoc"]:
            bat0.if_add(nic)

        # configure gw

        # configure ap

    except RuntimeError as e:
        print(e)
        reboot()
    except SystemError as e:
        print(e)