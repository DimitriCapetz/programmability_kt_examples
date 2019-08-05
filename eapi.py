# Allow self-signed certs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Actual script

from jsonrpclib import Server
from pprint import pprint

switch = Server("https://admin:arista@127.0.0.1:23443/command-api")

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