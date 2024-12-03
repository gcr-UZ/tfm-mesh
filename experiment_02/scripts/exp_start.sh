#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {intel|alfa1|alfa2}"
    exit 1
fi

# Argument received
ARG="$1"

# Check if the prefix is valid (e.g., 'intel' or 'alfa1')
if [[ "$ARG" != "intel" && "$ARG" != "alfa1" && "$ARG" != "alfa2" ]]; then
  echo "Invalid ARG. Valid ARGs are 'intel' or 'alfa1' or 'alfa2'."
  exit 1
fi

# Find all files matching the prefix and extract the numbers
files=$(ls ./../results/${ARG}_rssi_*.txt 2>/dev/null)
if [ -z "$files" ]; then
  highest=0
else
  highest=0
  for file in $files; do
    number=$(echo "$file" | grep -oP '\d+(?=\.txt)')
    if [ "$number" -gt "$highest" ]; then
      highest=$number
    fi
  done
fi


# Calculate the next number and create the new file
next_number=$((10#$highest + 1))
formatted_number=$(printf "%02d" "$next_number")
new_rssi_file="./../results/${ARG}_rssi_${formatted_number}.txt"
new_iperf_file="./../results/${ARG}_iperf_${formatted_number}.txt"

# Function to handle the cleanup on Ctrl+C
cleanup() {
  ps aux | grep 'iperf\|exp_' | grep -v grep | awk '{print $2}' | while read pid; do
      echo "Killing process with PID: $pid"
      kill -9 "$pid"
  done
  exit 1
}

# Trap Ctrl+C and call the cleanup function
trap cleanup INT

gnome-terminal -- bash -c "./exp_ap_rssi.sh $ARG | tee $new_rssi_file; exec bash"
gnome-terminal -- bash -c "iperf3 -c 192.168.68.101 -u -b 1M -l 125 -t 60 -i 0.1 --forceflush -R | ts '%Y%m%d-%H:%M:%.S' | tee ${new_iperf_file}; exec bash"
# gnome-terminal -- bash -c "iperf3 -c 192.168.68.101 -u -b 5M -l 625 -t 60 -i 0.1 --forceflush -R | ts '%Y%m%d-%H:%M:%.S' | tee ${new_iperf_file}; exec bash"
# gnome-terminal -- bash -c "iperf3 -c 192.168.68.101 -u -b 11.68M -l 1460 -t 60 -i 0.1 --forceflush -R | ts '%Y%m%d-%H:%M:%.S' | tee ${new_iperf_file}; exec bash"

sleep 62

cleanup
