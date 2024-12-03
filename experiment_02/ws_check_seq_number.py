import pyshark

'''
NADA, este solo detecta cambios mayores a +1 en el numero de secuencia (Sequence number,
dentro del elemento IEEE 802.11 QoS Data), pero eso NO es lo que busco.
Seria mas fiable fijarse, creo, en el campo Identification del elemento
Internet Protocol Version 4, PERO VEO QUE SE REPITEN BASTANTES PAQUETES,
SI POR EJEMPLO PONES ip.id == 0x4fda en el FOR_TESTS_data_alfa1_mon_intel_02_filtered
'''

def check_sequence_numbers(pcapng_file):
    # Open the pcapng file without a filter to capture all packets
    # capture = pyshark.FileCapture(pcapng_file, display_filter='(((udp) && (udp.dstport == 5201)) && (udp.length == 1468)) && (wlan.ta == 00:c0:ca:b2:bc:1a)')
    capture = pyshark.FileCapture(pcapng_file)
    
    prev_seq_num = None
    issues = []
    
    try:
        # Iterate over the packets in the capture
        for packet in capture:
            # Extract the sequence number (Layer 2 - wlan.seq)
            if hasattr(packet.wlan, 'seq'):
                # print(int(packet.wlan.seq))
                print(int(packet.wlan.seq))
                current_seq_num = int(packet.wlan.seq)

                # Check if this is the first packet
                if prev_seq_num is not None:
                    # Check if the sequence number increment is not 1
                    if current_seq_num != prev_seq_num + 1:
                        # print(packet.number)
                        issues.append((packet.sniff_time, prev_seq_num, current_seq_num))

                # Update previous sequence number to the current one
                prev_seq_num = current_seq_num

    except KeyboardInterrupt:
        pass
    finally:
        capture.close()

    return issues

# Example usage
pcapng_file = '/home/oem/master/tfm/000_experiments/exp_final/results/wireshark/FOR_TESTS_data_alfa1_mon_intel_02_filtered.pcapng'
sequence_issues = check_sequence_numbers(pcapng_file)

print("Checking sequence number increments:")
if sequence_issues:
    for issue_time, old_seq, new_seq in sequence_issues:
        print(f"At {issue_time}, sequence number jumped from {old_seq} to {new_seq}.")
else:
    print("All sequence numbers incremented correctly.")