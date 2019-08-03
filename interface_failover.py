# Allow self-signed certs
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Actual script

import argparse
from jsonrpclib import Server
import sys
import syslog
import time

# Pull in interface pair and vlans to configure file from command line argument
parser = argparse.ArgumentParser(description='Enable Backup Interface')
required_arg = parser.add_argument_group('Required Arguments')
required_arg.add_argument('-b', '--backup', dest='backup', required=True,
                          help='Backup Switchport to enable', type=str)
args = parser.parse_args()
backup_port = args.backup

# Open syslog for log creation
syslog.openlog('InterfaceFailover', 0, syslog.LOG_LOCAL4)

# Define URL for local eAPI connection. Uses Unix Socket
local_switch_req = Server("unix:/var/run/command-api.sock")

def enable_backup_port(switchport):
    syslog.syslog("%%IntFail-6-LOG: Enabling backup interface " + switchport + "...")
    local_switch_req.runCmds(1, ["enable", "configure", "interface " + switchport, 
                                 "no shutdown", "end"])
    ospf_neighbors = []
    while not ospf_neighbors:
        syslog.syslog("%%IntFail-6-LOG: Waiting for OSPF Adjacency to come up...")
        ospf_status = local_switch_req.runCmds(1, ["show ip ospf neighbor"])
        ospf_neighbors = ospf_status[0]["vrfs"]["default"]["instList"]["100"]["ospfNeighborEntries"]
        time.sleep(2)
    syslog.syslog("%%IntFail-6-LOG: OSPF Adjacency on backup interface " + switchport + " established")

def main():
    # Determine model of device for chassis / fixed classification
    try:
        device_info = local_switch_req.runCmds(1, ["show hostname"])
    except:
        syslog.syslog("%%IntFail-6-LOG: Unable to connect to local eAPI. No changes made")
        sys.exit()
    try:
        enable_backup_port(backup_port)
    except:
        syslog.syslog("%%PeerInt-6-LOG: No changes made")
        sys.exit()

if __name__ == '__main__':
    main()