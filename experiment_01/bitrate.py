import time

def get_network_data(interface):
    with open('/proc/net/dev') as f:
        data = f.readlines()

    for line in data:
        if interface in line:
            stats = line.split()
            rx_bytes = int(stats[1])
            tx_bytes = int(stats[9])
            return rx_bytes, tx_bytes

    return None, None

def calculate_bit_rate(interval, interface='eth0'):
    rx_bytes_old, tx_bytes_old = get_network_data(interface)
    time.sleep(interval)
    rx_bytes_new, tx_bytes_new = get_network_data(interface)

    rx_rate = (rx_bytes_new - rx_bytes_old) * 8 / interval  # bits per second
    tx_rate = (tx_bytes_new - tx_bytes_old) * 8 / interval  # bits per second

    return rx_rate, tx_rate

interval = 1  # seconds
interface = 'wlp0s20f3'  # replace with your network interface

while True:
    rx_rate, tx_rate = calculate_bit_rate(interval, interface)
    print(f"Receiving: {rx_rate*(10**-6)} Mbps, Sending: {tx_rate*(10**-6)} Mbps")
    # print(f"{10**-2}")