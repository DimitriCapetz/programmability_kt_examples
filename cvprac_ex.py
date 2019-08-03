# Disable SSL Warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CVPRAC
import argparse
from cvprac.cvp_client import CvpClient
from pprint import pprint
import sys

def parseargs():
    parser = argparse.ArgumentParser(
        description="CVP reconcile configlet parsing for device")
    parser.add_argument("--cvp", dest="cvp", required=True,
                        action="store", help="IP Address of CVP")
    parser.add_argument("--user", dest="user", required=True,
                        action="store", help="User for CVP")
    parser.add_argument("--passw", dest="passw", required=True,
                        action="store", help="Password for CVP")
    parser.add_argument("--device", dest="device", required=True,
                        action="store",
                        help="FQDN of device to parse reconcile configlet")
    args = parser.parse_args()
    return args

options = parseargs()

# Make connection to CVP
client = CvpClient()
client.connect([options.cvp], options.user, options.passw)
resp = client.api.get_cvp_info()
if resp is None:
    print "Failed to get CVP info. Exiting"
    sys.exit(1)

# Get Device Info
dev_info = client.api.get_device_by_name(options.device)
if dev_info is None:
    print "Unable to find device %s. Exiting" % options.device
    sys.exit(1)
print "Device Found in CVP.  Getting assigned configlets..."
dev_configlets = client.api.get_configlets_by_device_id(dev_info["systemMacAddress"])
configlet_list = []
for configlet in dev_configlets:
    configlet_list.append(configlet["name"])
print "The following configlets are assigned:"
for configlet_name in configlet_list:
    print configlet_name