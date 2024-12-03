#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {intel|alfa1|alfa2}"
    exit 1
fi

# Argument received
ARG="$1"

# Function to handle the cleanup on Ctrl+C
cleanup() {
  # echo "Ctrl+C pressed. Killing the new terminal."
  # pkill -P $$
  # kill "$new_terminal_pid"
  ps aux | grep exp_ | grep -v grep | awk '{print $2}' | while read pid; do
      echo "Killing process with PID: $pid"
      kill -9 "$pid"
  done
  exit 1
}

# Trap Ctrl+C and call the cleanup function
trap cleanup INT

new_rssi_file="./../results/${ARG}_rssi_00001.txt"
gnome-terminal -- bash -c "./exp_ap_rssi.sh $ARG | tee $new_rssi_file; exec bash"
new_terminal_pid=$!
# gnome-terminal -- bash -c "iperf3 -c 192.168.0.14 -u -b 11.68M -l 1460 -t 5 -i 0.1 --forceflush -R | ts '%Y%m%d-%H:%M:%.S' | tee ${new_iperf_file}; exec bash"

# Capture the PID of the new terminal
# new_terminal_pid=$!


sleep 120