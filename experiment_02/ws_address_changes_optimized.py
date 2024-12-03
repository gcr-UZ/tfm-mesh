import pyshark

def monitor_destination_address(pcapng_file):
    # Open the pcapng file without a filter to capture all packets
    # capture = pyshark.FileCapture(pcapng_file, display_filter='wlan.fc.type_subtype == 11')  # Adjust as needed
    # capture = pyshark.FileCapture(pcapng_file, display_filter='(((udp) && (udp.dstport == 5201)) && (udp.length == 1468)) && (wlan.ta == 00:c0:ca:b2:bc:1a)')  # Adjust as needed
    capture = pyshark.FileCapture(pcapng_file, display_filter='(((((udp) && (udp.srcport == 5201))) && (data.len == 625)) && (wlan.ra == 00:c0:ca:b2:bc:1a)) && !(wlan.fcs.status == "Bad")')  # Adjust as needed
    

    
    prev_dest_address = None
    prev_time = None
    changes = []
    
    try:
        # Iterate over the packets in the capture
        for packet in capture:
            last_packet = None  # To store the last packet

            # Sniff packets continuously, but store only the last one
            print("Capturing packets... Press Ctrl+C to stop.")
            
            for packet in capture:
                last_packet = packet  # Update the last packet with each iteration
            # Extract the destination address (Layer 2)
            # if hasattr(packet.wlan, 'ta'):
            #     print(capture)
            #     print('hola')
            #     exit()
            #     dest_address = packet.wlan.ta
            #     current_time = packet.sniff_time  # Timestamp of the current packet

            #     # If this is the first packet, set the initial address and time
            #     if prev_dest_address is None:
            #         prev_dest_address = dest_address
            #         prev_time = current_time

            #     # Check if the destination address has changed
            #     if dest_address != prev_dest_address:
            #         # Calculate the time difference between the two packets
            #         time_diff = (current_time - prev_time).total_seconds()

            #         # Record the change with the timestamp and time difference
            #         changes.append((current_time, prev_dest_address, dest_address, time_diff, packet.number))

            #         # Update the previous address and time to the current packet
            #         prev_dest_address = dest_address
            #         prev_time = current_time
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"TShark crashed: {e}")
        capture.close()
        return changes
    finally:
        capture.close()
    
    return changes

# Example usage
# pcapng_file = '/home/oem/master/tfm/000_experiments/exp_04/Alfa1/07.pcapng'
pcapng_file = '/home/oem/master/tfm/000_experiments/exp_final/results/wireshark/data_alfa1_mon_intel_00.pcapng'
changes = monitor_destination_address(pcapng_file)

print("Monitoring destination address changes with elapsed time:")
if changes:
    for change_time, old_address, new_address, time_diff, number in changes:
        print(f"{number} -- At {change_time}, destination address changed from {old_address} to {new_address}. Time elapsed: {time_diff} seconds.")
else:
    print("No changes in destination address detected.")
