#!/bin/bash
set -e

# Set auth options
PASSWORD=$3
USERNAME='root@pam'

# Set VM ID
VMID=$1

# Set Node
# This must either be a DNS address or name of the node in the cluster
NODE="pve"

# Proxy equals node if node is a DNS address
# Otherwise, you need to set the IP address of the node here
PROXY=$2

echo USERNAME:$USERNAME PASSWORD:$PASSWORD IP:$PROXY VM:$VMID

#The rest of the script from Proxmox
NODE="${NODE%%\.*}"

DATA=$(curl -f -s -S -k --data-urlencode "username=$USERNAME" --data-urlencode "password=$PASSWORD" "https://$PROXY:8006/api2/json/access/ticket")
echo $DATA
echo "AUTH OK"

TICKET="${DATA//\"/}"
TICKET="${TICKET##*ticket:}"
TICKET="${TICKET%%,*}"
TICKET="${TICKET%%\}*}"

CSRF="${DATA//\"/}"
CSRF="${CSRF##*CSRFPreventionToken:}"
CSRF="${CSRF%%,*}"
CSRF="${CSRF%%\}*}"
echo "https://$PROXY:8006/api2/spiceconfig/nodes/$NODE/qemu/$VMID/spiceproxy"
echo "https://$PROXY:8006/api2/json/nodes/$NODE/qemu/$VMID/spiceproxy"
curl -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/spiceconfig/nodes/$NODE/qemu/$VMID/spiceproxy" -d "proxy=$PROXY" > spiceproxy
#curl -f -s -S -k -b "PVEAuthCookie=$TICKET" -H "CSRFPreventionToken: $CSRF" "https://$PROXY:8006/api2/json/nodes/$NODE/qemu/$VMID/spiceproxy" -d "proxy=$PROXY" > spiceproxy

#Launch remote-viewer with spiceproxy file, in kiosk mode, quit on disconnect
#The run loop will get a new ticket and launch us again if we disconnect

#exec remote-viewer -k --kiosk-quit on-disconnect spiceproxy
exec remote-viewer -f spiceproxy
