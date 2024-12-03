import pyshark

def count_association_requests(pcapng_file):
    # Open the pcapng file
    print(pcapng_file)
    capture = pyshark.FileCapture(pcapng_file, display_filter='wlan.fc.type_subtype == 11')
    
    count = 0
    prev_time = None
    time_diffs = []

    try:
        # Iterate over the packets in the capture
        for packet in capture:
            count += 1

            # Get the timestamp of the current packet
            current_time = float(packet.sniff_time.timestamp())
            
            # If this is not the first packet, calculate the time difference
            if prev_time is not None:
                time_diff = current_time - prev_time
                time_diffs.append(time_diff)

            # Update prev_time to the current packet's timestamp
            prev_time = current_time
    except KeyboardInterrupt:
        pass
    finally:
        capture.close()
    
    return count, time_diffs

# Example usage
pcapng_file = '/home/oem/master/tfm/000_experiments/exp_04/Alfa1/07.pcapng'
association_requests_count, time_diffs = count_association_requests(pcapng_file)

print(f"Number of 802.11 Authentication: {association_requests_count}")
print("Time differences between consecutive Authentication (in seconds):")
for i, diff in enumerate(time_diffs):
    print(f"Request {i + 1} to {i + 2}: {diff} seconds")
