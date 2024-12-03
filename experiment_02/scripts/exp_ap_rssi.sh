#!/bin/bash

# Ensure the script is run with an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {intel|alfa1|alfa2}"
    exit 1
fi

# Name of interfaces
INTEL_NAME="wlp0s20f3"
ALFA1_NAME="wlx00c0cab2bc2c"
#ALFA1_NAME="wlx00c0cab2bc1a"
ALFA2_NAME="wlx00c0cab3c2de"

# Argument received
ARG="$1"

# Perform actions based on the argument
case "$ARG" in
    intel)
        INAME=${INTEL_NAME}
        ;;
    alfa1)
        INAME=${ALFA1_NAME}
        ;;
    alfa2)
        INAME=${ALFA2_NAME}
        ;;
    *)
        echo "Invalid argument. Use 'intel', 'alfa1', or 'alfa2'."
        exit 1
        ;;
esac

while true; do
    iwconfig $INAME | awk '/Access Point/ {ap=$6} /Signal level/ {signal=$4} END {print "Access Point:", ap, "- Signal level:", signal}' | ts '%Y%m%d-%H:%M:%.S'
    sleep 0.04
done


