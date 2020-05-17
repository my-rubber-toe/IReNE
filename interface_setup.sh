# Firewall: Trusted Network Interface Update Script
# Author: Roberto Y. Guzman - roberto.guzman3@upr.edu
# 
# When the system runs, it creates a network that must be added to the trusted zone
# of the operating system firewall. 
#
# Usage:
# 
# Run the command "ifconfig" and identify the network created by the containers. (All new docker networs start with prefix "br")
# 
# When you have identified the network run this file as such:
#
# "sudo ./interface_setup.sh <interface-name>"

if [ -z $1 ]
then
  echo Argument required. Please use a valid interface.
  exit 
fi

DEFAULT_DOCKER_IFACE="docker0"
FIREWALL_IFACES=$(firewall-cmd --zone=trusted --list-interfaces)

echo Removing old interfaces . . .  

for IFACE in $FIREWALL_IFACES
do
  if [ $IFACE != $DEFAULT_DOCKER_IFACE ] 
  then
    echo Remove interface: $IFACE
    firewall-cmd --permanent --zone=trusted --remove-interface=$IFACE
  fi
done

firewall-cmd --reload

echo Old interfaces removed.

echo Adding new interface . . .

AVAILABLE_IFACES=$(ls /sys/class/net/)

for IFACE in $AVAILABLE_IFACES
do
  if [ "$IFACE" == "$1" ]
  then
    firewall-cmd --permanent --zone=trusted --add-interface=$1
    firewall-cmd --reload
    echo Added interface: $1
    exit 0
  fi
done

echo Invalid: Interface not found.




