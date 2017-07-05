#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

echo "booting..."
modprobe batman-adv
service network-manager stop
service isc-dhcp-server stop

sleep 5

echo "starting..."
python3 main.py "gotham_iperf_test.json"