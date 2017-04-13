from gotham.net.cmd.netscan import *
from gotham.net.preference import PacketPreference
import gotham.server.ControlServer as control_server
from gotham.util.net.UDPClient import UDPClient

PacketPreference.NODE_IP = IPv4("169.254.9.141")
PacketPreference.NODE_NAME = "BetaS-ubuntu"

"""
nodes = []
s = NetScanResultFrame.build(1, 148321563.851, nodes)
print(s)

p = UDPControlFrame.parse(s)
p = NetScanResultFrame.parse(p.payload)
print(p)
print(p.level)
print(p.nodes[0]['ip'])
"""

control_server.server_start()

print("opened")

client = UDPClient("255.255.255.255", 15961)

req = NetScanRequestFrame.build(NetScanRequestLevel.NORMAL)

client.send(req)
