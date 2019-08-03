import pyeapi
import time

# Load Config File
pyeapi.load_config('nodes.conf')

# Connect to vEOS Node
node = pyeapi.connect_to("python-eos1")

# Basic Show Commands
mlag_resp = node.enable("show mlag")
mlag_domain = mlag_resp[0]["result"]["domainId"]

print "MLAG Domain-ID is " + mlag_domain
print ""

# Configure Static Route
node.api('staticroute').create(ip_dest="99.99.99.0/24", next_hop="10.204.0.66")
time.sleep(2)
route_entry = node.enable("show ip route 99.99.99.1")[0]["result"]
route = route_entry["vrfs"]["default"]["routes"].keys()[0]
next_hop = route_entry["vrfs"]["default"]["routes"][route]["vias"][0]["nexthopAddr"]
next_hop_int = route_entry["vrfs"]["default"]["routes"][route]["vias"][0]["interface"]
print "Route for %s programmed with next-hop of %s on interface %s" % (route, next_hop, next_hop_int)
print ""

# Parse Running Config
print "Matching Config Line"
runnning_config = node.get_config("running-config")
for line in runnning_config:
    if line.startswith("ip route " + route):
        print line