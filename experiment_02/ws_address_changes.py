import pyshark
from datetime import datetime
from pathlib import Path
import time


def process(file):
    print(f"## PROCESSING {file} ##")
    def monitor_destination_address(pcapng_file):
        # Open the pcapng file without a filter to capture all packets
        # capture = pyshark.FileCapture(pcapng_file, display_filter='wlan.fc.type_subtype == 11')  # Adjust as needed
        # capture = pyshark.FileCapture(pcapng_file, display_filter='(((udp) && (udp.dstport == 5201)) && (udp.length == 1468)) && (wlan.ta == 00:c0:ca:b2:bc:1a)')  # Adjust as needed
        # capture = pyshark.FileCapture(pcapng_file, display_filter='(((((udp) && (udp.srcport == 5201))) && (data.len == 625)) && (wlan.ra == 00:c0:ca:b2:bc:1a)) && !(wlan.fcs.status == "Bad")')  # Adjust as needed
        capture = pyshark.FileCapture(pcapng_file)  # Adjust as needed
        
        prev_dest_address = None
        prev_time = None
        changes = []
        # # # print(capture[20].pretty_print())
        # # # # print(capture[20].timestamp)
        # # # exit()
        
        try:
            # Iterate over the packets in the capture
            for packet in capture:
                # Extract the destination address (Layer 2)
                # print(packet)

                # if int(packet.number) % 10000 == 0:
                #     print(f"{int(packet.number)} -> {datetime.now()}")

                dest_address = packet.wlan.ta
                current_time = packet.sniff_time  # Timestamp of the current packet

                # If this is the first packet, set the initial address and time
                if prev_dest_address is None:
                    prev_dest_address = dest_address
                    prev_time = current_time

                # Check if the destination address has changed
                if dest_address != prev_dest_address:
                    # print("CHANGE! " + str(prev_time) + " - " + str(current_time))
                    # print(" " + str(current_time - prev_time))
                    # Calculate the time difference between the two packets
                    time_diff = (current_time - prev_time).total_seconds()

                    # Record the change with the timestamp and time difference
                    changes.append((current_time, prev_dest_address, dest_address, time_diff, packet.number))

                # Update the previous address and time to the current packet
                prev_dest_address = dest_address
                prev_time = current_time
        
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"TShark crashed: {e}")
            capture.close()
            return changes
            # pass
        finally:
            capture.close()
        
        return changes

    # Example usage
    # pcapng_file = '/home/oem/master/tfm/000_experiments/exp_04/Alfa1/07.pcapng'
    # pcapng_file = '/home/oem/master/tfm/000_experiments/exp_final/results/wireshark/data_alfa1_mon_intel_01_filtered.pcapng'
    # changes = monitor_destination_address(pcapng_file)

    start_time = time.time()
    changes = monitor_destination_address(file)
    end_time = time.time()

    print("Monitoring destination address changes with elapsed time:")
    if changes:
        for change_time, old_address, new_address, time_diff, number in changes:
            print(f"{number} -- At {change_time}, destination address changed from {old_address} to {new_address}. Time elapsed: {time_diff} seconds.")
    else:
        print("No changes in destination address detected.")
    
    execution_time = end_time - start_time
    print(f"---------\nFile processing time: {execution_time:.2f}")




directory_path = Path('/home/oem/master/tfm/000_experiments/exp_final/results/wireshark')
# Create a list of matching file paths
filtered_files = sorted(directory_path.glob('*_filtered.pcapng'), key=lambda f: f.name)

# Print sorted filenames
for filepath in filtered_files:
    process(filepath)
    # process('/home/oem/master/tfm/000_experiments/exp_final/results/wireshark/FOR_TESTS_data_alfa1_mon_intel_05_filtered.pcapng')
    print("\n")
    print("\n")
    # exit(-1)

print("** FINISH **")