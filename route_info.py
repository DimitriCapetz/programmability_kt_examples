# Allow self-signed certs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Actual script

from jsonrpclib import Server

switch1 = Server("https://admin:arista@127.0.0.1:23443/command-api")
switch2 = Server("https://admin:arista@127.0.0.1:24443/command-api")

dest_ip = raw_input("What IP are you trying to find? ")

hostname1 = switch1.runCmds(1, ["show hostname"])[0]["hostname"]
hostname2 = switch2.runCmds(1, ["show hostname"])[0]["hostname"]

switch1_route = switch1.runCmds(1, ["show ip route " + dest_ip])

if switch1_route[0]["vrfs"]["default"]["routes"][dest_ip + "/32"]["directlyConnected"]:
    interface = switch1_route[0]["vrfs"]["default"]["routes"][dest_ip + "/32"]["vias"][0]["interface"]
    print "%s is directly connected on %s %s" % (dest_ip, hostname1, interface)
else:
    route_type = switch1_route[0]["vrfs"]["default"]["routes"][dest_ip + "/32"]["routeType"]
    nexthop_addr = ""
    for nexthop in switch1_route[0]["vrfs"]["default"]["routes"][dest_ip + "/32"]["vias"]:
        nexthop_addr+=nexthop["nexthopAddr"] + " "
    print "%s was learned via %s with next-hops %s" % (dest_ip, route_type, nexthop_addr)
    print "Checking %s..." % (hostname2)
    switch2_route = switch2.runCmds(1, ["show ip route " + dest_ip])
    interface = switch2_route[0]["vrfs"]["default"]["routes"][dest_ip + "/32"]["vias"][0]["interface"]
    print "%s is directly connected on %s %s" % (dest_ip, hostname2, interface)