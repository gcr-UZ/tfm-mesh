import pyshark

'''
NADA, este es solo un script para contar num paquetes en fichero wireshark
'''

def count_association_requests(pcapng_file):
    # Open the pcapng file
    # capture = pyshark.FileCapture(pcapng_file, display_filter='wlan.fc.type_subtype == 8')
    # capture = pyshark.FileCapture(pcapng_file, display_filter='((((udp) && (udp.dstport == 5201)) && (udp.length == 1468)) && (wlan.ta == 00:c0:ca:b2:bc:1a))')
    capture = pyshark.FileCapture(pcapng_file, display_filter='udp')
    
    count = 0
    try:
        # Iterate over the packets in the capture
        for packet in capture:
            count += 1
    except KeyboardInterrupt:
        pass
    finally:
        capture.close()
    
    return count

# Example usage
pcapng_file = '/home/oem/master/tfm/000_experiments/exp_final/results/wireshark/FOR_TESTS_data_alfa1_mon_intel_02_filtered.pcapng'
association_requests_count = count_association_requests(pcapng_file)
print(f"Number of 802.11 Association Requests: {association_requests_count}")
