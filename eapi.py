# Allow self-signed certs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Actual script

from jsonrpclib import Server
from pprint import pprint

switch = Server("https://admin:arista@127.0.0.1:23443/command-api")

response = switch.runCmds(1, ["show version"])

pprint(response)

#system_mac = response[0]["systemMacAddress"]

#print system_mac