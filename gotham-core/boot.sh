#!/bin/bash

modprobe batman-adv
service network-manager stop

sleep 5

python boot.py