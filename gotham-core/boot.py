# encoding; utf-8

import psutil, subprocess, json, time, sys
from gotham.util.pybatctl.BATMAN import BATMAN
from gotham.util.hwutil.ifconfig import Interface
from gotham.util.ap import hostapd


def check_hostname(target_name):
    import socket
    curr_name = socket.gethostname()

    if curr_name != target_name:
        print(curr_name)
        return False

    return True


def set_hostname(name):
    subprocess.Popen(["hostnamectl", "set-hostname", name])


def set_nameserver(server):
    with open("/etc/resolv.conf", "w") as dns:
        lines = "nameserver "+server+"\nnameserver 127.0.1.1\n"
        dns.write(lines)


def load_json(filename="gotham.json"):
    with open(filename) as data_file:
        data = json.load(data_file)
        return data

    return None


def reboot():
    print("reboot!")
    exit(-1)


def boot(path):
    try:
        json = load_json(path)

        print("[+] loading config json :", path)
        if not json:
            print("[!] fail to load json :", path)
            exit(-1)

        print("[+] clearing cache")
        subprocess.call(['sysctl', '-w', 'net.ipv4.ip_forward=1'])
        subprocess.call(['iptables', '--flush'])
        subprocess.call(['iptables', '--table', 'nat', '--flush'])
        subprocess.call(['iptables', '--delete-chain'])
        subprocess.call(['iptables', '--table', 'nat', '--delete-chain'])
        """
        print("[+] check hostname")
        if not check_hostname(json["node_id"]):
            set_hostname(json["node_id"])
            raise RuntimeError("detect hostname difference...")
        """
        print("[+] setting nameserver")
        if json["nameserver"] and len(json["nameserver"]) > 0:
            print("    [+] nameserver :", json["nameserver"])
            set_nameserver(json["nameserver"])

        print("[+] check nic list")
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

        print("   ", nic_list)

        print("[+] clearing batman-adv's child interface")
        bat0 = BATMAN("bat0")
        bat0.if_clear()

        time.sleep(3)

        print("[+] configure adhoc interface")
        if len(nic_list["adhoc"]) <= 0:
            raise SystemError("must have 1 or more ad-hoc network interface cards.")

        if len(nic_list["adhoc"]) == 1:
            nic = nic_list["adhoc"][0]
            print("    [+] configure", nic)
            data = json["nic"][nic]["data"]
            Interface(nic).set_mtu(1527).down()
            Interface(nic).set_adhoc(data["ssid"], data["channel"]).up()

            bat0.if_add(nic)

        else:
            raise SystemError("adhoc interface should be unique.")

        print("[+] start avahi autoipd service")
        Interface("bat0").up().autoip()

        time.sleep(3)

        # configure gw
        if len(nic_list["gw"]) > 0:
            print("[+] configure gw")
            if len(nic_list["gw"]) == 1:
                nic = nic_list["gw"][0]
                data = json["nic"][nic]["data"]
                print("    [+] configure", nic)
                nic = Interface(nic)
                nic.set_ip(data["ip"], data["subnet"]).set_gw(data["gateway"])
                nic.set_masquerade("bat0")

            else:
                raise SystemError("gateway interface should be unique.")

        # configure ap
        if len(nic_list["ap"]) > 0:
            print("[+] configure ap")
            if len(nic_list["ap"]) == 1:
                nic = nic_list["ap"][0]
                data = json["nic"][nic]["data"]
                hostapd.start_hostapd(data["target"], nic, data["ssid"], data["channel"], data["dhcp"], "255.255.255.0")
            else:
                raise SystemError("ap interface should be unique.")

        print("[+] booting finish...")
        time.sleep(5)

        return nic_list


    except RuntimeError as e:
        print(e)
        reboot()
    except SystemError as e:
        print(e)


if __name__ == "__main__":
    boot("gotham.json")