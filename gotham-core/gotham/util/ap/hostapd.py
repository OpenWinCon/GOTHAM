# encoding: utf-8

import subprocess, time, sys
import ipaddress
from gotham.util.hwutil.ifconfig import Interface

__HOSTAPD_CONFIG__ = "hostapd.conf"
__DHCPD_CONFIG__ = "/etc/dhcp/dhcpd.conf"


def make_hostapd_config(dev, ssid, channel=6):
    write = [
        "interface="+dev,
        "driver=nl80211",
        "ssid="+ssid,
        "hw_mode=g",
        "channel="+str(channel),
        "ieee80211n=1",
        "wmm_enabled=1",
        "ht_capab=[HT40+][SHORT-GI-40][SHORT-GI-20]"
    ]

    with open(__HOSTAPD_CONFIG__, "w") as file:
        for s in write:
            file.write(s+"\n")


def make_dhcpd_config(ip, mask, dns_server):
    addr = ipaddress.ip_network(ip+"/"+mask, False)
    ip = str(list(addr.hosts())[0])
    network = str(addr.network_address)
    start = str(list(addr.hosts())[1])
    end = str(list(addr.hosts())[-1])
    bc = str(addr.broadcast_address)

    write = [
        'INTERFACES="eth0";'
        'ddns-update-style none;',
        'ignore client-updates;',
        'default-lease-time 600;',
        'option domain-name "subnet.gotham";',
        'option domain-name-servers '+ip+', '+dns_server+';',
        'log-facility local7;',
        'max-lease-time 7200;',
        'subnet '+network+' netmask '+mask+' {',
        '   option routers '+ip+';',
        '   option subnet-mask '+mask+';',
        '   option broadcast-address '+bc+';',
        '   option time-offset 0;',
        '   range '+start+' '+end+';',
        '}'
    ]

    with open(__DHCPD_CONFIG__, "w") as file:
        for s in write:
            file.write(s + "\n")


def start_hostapd(in_dev, out_dev, ssid, channel, ip="192.168.0.1", netmask="255.255.255.0", dns="163.180.96.54"):
    """
    Configs the IN interface, starts dhcpd, configs iptables, Starts Hostapd
    """
    internet = in_dev
    host = out_dev
    PUBLIC_IP = Interface(internet).get_ip()
    IP = ip
    NETMASK = netmask

    print("[+] public ip :", PUBLIC_IP)

    make_hostapd_config(out_dev, ssid, channel)
    make_dhcpd_config(ip, netmask, dns)

    try:
        with open(__HOSTAPD_CONFIG__) as f:
            pass
    except IOError as e:
        print('[ERROR] ' + __HOSTAPD_CONFIG__ + ' doesn\'t exist')
        exit(1)

    # Configure network interface
    print('configuring', host, '...')
    subprocess.call(['rfkill', 'unblock', 'all'])
    subprocess.call(['ifconfig', host, 'up', IP, 'netmask', NETMASK])
    time.sleep(1)
    dhcp_log = open('./dhcp.log', 'w')

    # Start dhcpd
    print('Starting dhcpd...')
    dhcp_proc = subprocess.Popen(['dhcpd', host, '-cf', __DHCPD_CONFIG__], stdout=dhcp_log, stderr=dhcp_log)
    time.sleep(1)
    dhcp_log.close()

    # Configure iptables
    print('Configuring iptables...')
    subprocess.call(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', internet, '-j', 'SNAT', '--to', PUBLIC_IP])
    subprocess.call(['iptables', '-A', 'FORWARD', '-i', host, '-j', 'ACCEPT'])

    # Start hostapd
    print('Starting Hostapd...')
    hostapd_proc = subprocess.Popen(['hostapd -t -dd ' + __HOSTAPD_CONFIG__ + ' >./hostapd.log'], shell=True)
    print('Done... (Hopefully!)')
    print()

def stop_hostapd():
    """
    Stops Hostapd and dhcpd
    """
    print()
    print('Killing Hostapd...')
    subprocess.call(['killall', 'hostapd'])
    print('Killing dhcpd...')
    subprocess.call(['killall', 'dhcpd'])
    print()


if __name__ == "__main__":
    subprocess.call(['iptables', '--flush'])
    subprocess.call(['iptables', '--table', 'nat', '--flush'])
    subprocess.call(['iptables', '--delete-chain'])
    subprocess.call(['iptables', '--table', 'nat', '--delete-chain'])

    start_hostapd("eth0", "wlan1", "gotham-test-ap", "172.31.1.1", "255.255.255.0")

    while True:
        pass