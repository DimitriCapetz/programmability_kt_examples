# Allow self-signed certs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Actual script

from jsonrpclib import Server
from pprint import pprint

switch = Server("https://eapi-user:eapi-password@10.100.100.1/command-api")

response = switch.runCmds(1, ["show version", "show hostname"])

pprint(response)

#system_mac = response[0]["systemMacAddress"]
#hostname = response[1]["hostname"]
#int_eth1 = response[3]["cmds"]["interface Ethernet1"]["cmds"]
#print system_mac
#print hostname
#print "Config Items for interface Ethernet1"
#for cmd in int_eth1:
#    print "   " + cmd


# FOR REFERENCE
# MY LOCAL MAC
# a483.e715.ee67

#mac = input('Which MAC would you like to find? ')
#
#mac_table = switch.runCmds(1, ["show mac address-table address {mac}".format(mac = mac)])
#pprint(mac_table)

#interface = mac_table[0]['unicastTable']['tableEntries'][0]['interface']
#print("MAC Address {mac} is located on interface {interface}".format(
#    mac = mac,
#    interface = interface
#))

