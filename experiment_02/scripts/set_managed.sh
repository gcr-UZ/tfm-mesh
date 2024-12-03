#!/bin/bash

# Ensure the script is run with an argument
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 {intel|alfa1|alfa2} <channel> <width>"
    exit 1
fi

# Name of interfaces
INTEL_NAME="wlp0s20f3"
#ALFA1_NAME="wlx00c0cab2bc1a"
ALFA1_NAME="wlx00c0cab2bc2c"
ALFA2_NAME="wlx00c0cab3c2de"

# Path to the NetworkManager.conf file
CONF_FILE="/etc/NetworkManager/NetworkManager.conf"

# Argument received
ARG="$1"
CHANNEL="$2"
WIDTH="$3"


# Define the lines to be modified
LINE1="unmanaged-devices=interface-name:${ALFA1_NAME};${ALFA2_NAME}"
LINE2="unmanaged-devices=interface-name:${INTEL_NAME};${ALFA2_NAME}"
LINE3="unmanaged-devices=interface-name:${INTEL_NAME};${ALFA1_NAME}"

# Helper function to comment out a line
comment_out_line() {
    local line="$1"
    sed -i "s/^${line}/#${line}/" "$CONF_FILE"
}

# Helper function to uncomment a line
uncomment_line() {
    local line="$1"
    sed -i "s/^#${line}/${line}/" "$CONF_FILE"
}

# Perform actions based on the argument
case "$ARG" in
    intel)
        uncomment_line "$LINE1"
        comment_out_line "$LINE2"
        comment_out_line "$LINE3"
        INAME=${INTEL_NAME}
        sudo ifconfig $INAME down; sudo iwconfig $INAME mode managed; sudo ifconfig $INAME up;
        ;;
    alfa1)
        uncomment_line "$LINE2"
        comment_out_line "$LINE1"
        comment_out_line "$LINE3"
        INAME=${ALFA1_NAME}
        sudo ifconfig $INAME down; sudo iwconfig $INAME mode managed; sudo ifconfig $INAME up;

        ;;
    alfa2)
        uncomment_line "$LINE3"
        comment_out_line "$LINE1"
        comment_out_line "$LINE2"
        INAME=${ALFA2_NAME}
        sudo ifconfig $INAME down; sudo iwconfig $INAME mode managed; sudo ifconfig $INAME up;

        ;;
    *)
        echo "Invalid argument. Use 'intel', 'alfa1', or 'alfa2'."
        exit 1
        ;;
esac

# Restar NetworkManager
sudo systemctl restart NetworkManager


# Set monitor mode and channel
iw dev | awk '/phy#/{phy=substr($1, 5); next} /Interface/{print "phy" phy, $2}' | while read -r phy_iface; do
    phy=$(echo $phy_iface | awk '{print $1}')
    iface=$(echo $phy_iface | awk '{print $2}')
    if [ "$iface" != "$INAME" ]; then
        echo "Setting channel for $iface"
        sudo ifconfig $iface down; sudo iwconfig $iface mode monitor; sudo ifconfig $iface up; sudo iw $phy set channel "$CHANNEL" "$WIDTH"
    fi
done

echo "$ARG is now in managed mode."
