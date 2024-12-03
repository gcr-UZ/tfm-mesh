import re
import matplotlib.pyplot as plt

# # # # card = 'Intel (Intel Wi-Fi 6 AX201)'
# # # # dir_memoria = 'ax201-img/memoria/'
# # # # dir = 'ax201/2n_noR_0'
# # # # # dir = 'ax201/2n_siR_siI_0'
# # # # main_title = f'{card}\n\nNodos y RSSI a lo largo del tiempo'
# # # # # dir = 'ax201/2n_siR_siI_0'
# # # # # main_title = f'{card}. Scenario 3'

card = 'Alfa1 (Alfa AWUS036ACHM)'
dir_memoria = 'awus-img/memoria/'
dir = 'awus/2n_noR_0'
# dir = 'awus/2n_siR_siI_0'
main_title = f'{card}\n\nNodos y RSSI a lo largo del tiempo'
# dir = 'awus/2n_siR_siI_0'
# main_title = f'{card}. Scenario 3'

# card = 'Alfa 2 (Alfa AWUS036AXML)'
# dir_memoria = 'awusAXML-img/memoria/'
# dir = 'awusAXML/2n_noR_0'
# # dir = 'awusAXML/2n_siR_siI_0'
# main_title = f'{card}\n\nNodos y RSSI a lo largo del tiempo'
# # dir = 'awusAXML/2n_siR_siI_0'
# # main_title = f'{card}. Scenario 3'

iter = '2'

# title = f'RSSI and nodes over time'
title = f''

# # # # # # # def iperf3_data():
# # # # # # #     with open(f'./{dir}{iter}_iperf', 'r') as file:
# # # # # # #         data = file.read()
# # # # # # #         return data

# with open('./ax201/2n_noR_01.txt', 'r') as file:
with open(f'./{dir}{iter}.txt', 'r') as file:
    data = file.read()

# # # # # # iperf_data = iperf3_data()
# # # # # # # print(iperf_data)
# # # # # # # exit()
# # # # # # # Regex to capture Bitrate values (including bits/sec and Mbits/sec)
# # # # # # bitrate_pattern = re.compile(r'(\d+\.\d+|\d+) (Mbits/sec|bits/sec)')

# # # # # # # Find all matches
# # # # # # bitrate_matches = bitrate_pattern.findall(iperf_data)
# # # # # # print(bitrate_matches)

# # # # # # # Convert all bitrates to Mbits/sec
# # # # # # bitrate_values = []
# # # # # # for value, unit in bitrate_matches:
# # # # # #     value = float(value)
# # # # # #     if unit == "bits/sec":
# # # # # #         value /= 1e6  # Convert bits/sec to Mbits/sec
# # # # # #     bitrate_values.append(value)

# # # # # # print(bitrate_values)
# # # # # # bitrate_values = bitrate_values[:-2]
# # # # # # print(bitrate_values)
# # # # # # # last_index_00 = len(bitrate_values) - 1 - bitrate_values[::-1].index(0.0)
# # # # # # # last_index_00 = (len(bitrate_values) - 1 - bitrate_values[::-1].index(0.0)) + 1
# # # # # # last_index_00 = (len(bitrate_values) - 1 - bitrate_values[::-1].index(0.0)) - 2
# # # # # # print(last_index_00)
# # # # # # # print(bitrate_values[41])


# Initialize lists to hold the extracted data
timestamps = []
rssi_values = []
nodes = []
numeric_nodes = []

rssi_min = 0
rssi_min_i = 0

rssi_max = -300
rssi_max_i = 0

# Regular expression patterns to match lines of interest
rssi_pattern = re.compile(r"RSSI=(-?\d+) dBm")
node_pattern = re.compile(r"node=(\w+)")

# Split data into blocks
blocks = data.strip().split("---------------------------")

# Parse each block
for i, block in enumerate(blocks):
    # Extract RSSI
    rssi_match = rssi_pattern.search(block)
    if rssi_match:
        rssi_value = int(rssi_match.group(1))
        rssi_values.append(rssi_value)
        if rssi_value < rssi_min:
            rssi_min = rssi_value
            rssi_min_i = i
        if rssi_value > rssi_max:
            rssi_max = rssi_value
            rssi_max_i = i
    else:
        rssi_values.append(None)  # In case RSSI is not found

    # Extract Node
    node_match = node_pattern.search(block)
    if node_match:
        nodes.append(node_match.group(1))
        numeric_nodes.append(int(node_match.group(1)[-1]))

    else:
        nodes.append(None)  # In case node is not found
        numeric_nodes.append(None)

    # Generate a simple timestamp for each entry
    timestamps.append(i)

# print("Timestamps:", timestamps)
# print("RSSI Values:", rssi_values)
# print("Nodes:", nodes)

rssi_values_no_none = [i for i in rssi_values if i is not None]
rssi_average = sum(rssi_values_no_none) / len(rssi_values_no_none)
# rssi_average = sum(rssi_values) / len(rssi_values)

unique_nodes = list(set(nodes))
node_map = {node: i+1 for i, node in enumerate(unique_nodes)}
transform_nodes = []
dict = {}
print("## NODES ##")
print(numeric_nodes)
index_Node_2 = numeric_nodes.index(2)
print(index_Node_2)

# # # # # # # if last_index_00 < index_Node_2:
# # # # # # #     bitrate_values = [bitrate_values[0]] * (index_Node_2-last_index_00) + bitrate_values
# # # # # # # elif last_index_00 > index_Node_2:
# # # # # # #     bitrate_values = bitrate_values[:-(last_index_00 - index_Node_2)]
# # # # # # # print(bitrate_values)


for x in numeric_nodes:
    if x == 1:
        transform_nodes.append(rssi_average)
        dict[rssi_average] = x
    elif x == 2:
        transform_nodes.append(rssi_average - 5)
        dict[rssi_average - 5] = x
    elif x == 3:
        transform_nodes.append(rssi_average - 10)
        dict[rssi_average - 10] = x

# Create a time series for x-axis
time_series = list(range(1, len(rssi_values) + 1))

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(time_series, rssi_values, color='blue', label='RSSI (dBm)', zorder=1)
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('RSSI (dBm)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# # # # # # # # # # # # Create a secondary y-axis for Ptx values
# # # # # # # # # # # if len(time_series) > len(bitrate_values):
# # # # # # # # # # #     bitrate_values = bitrate_values + [0.0] * (len(time_series)-len(bitrate_values))
# # # # # # # # # # # elif len(time_series) < len(bitrate_values):
# # # # # # # # # # #     bitrate_values = bitrate_values[:-(len(bitrate_values)-len(time_series))]
# # # # # # # # # # # ax2 = ax1.twinx()
# # # # # # # # # # # ax2.plot(time_series, bitrate_values, color='red', label='Bitrate (Mbps)')
# # # # # # # # # # # ax2.set_ylabel('Bitrate (Mbps)', color='red')
# # # # # # # # # # # ax2.tick_params(axis='y', labelcolor='red')

# show min rssi
ax1.scatter(rssi_min_i+1, rssi_min, c='red', marker='o', s=100, zorder=2)
ax1.annotate(f'{rssi_min} dBm', 
                        xy=(rssi_min_i+1, rssi_min), 
                        xytext=(rssi_min_i+1 - 1.4, rssi_min - 3),
                        textcoords='data',
                        fontsize=12,
                        color='red')

# plt.gca().set_ylim([ min(rssi_values_no_none) - 10, max(rssi_values_no_none) + 10])
ax1.set_ylim([ min(rssi_values_no_none) - 10, max(rssi_values_no_none) + 10])
# plt.gca().set_ylim([ min(rssi_values) - 10, max(rssi_values) + 10])

# Annotate the nodes
for i in range(len(transform_nodes)):
    if i == 0 or transform_nodes[i] != transform_nodes[i - 1]:
        if dict[transform_nodes[i]] == 3:
            continue
        ax1.annotate(f'nodo {dict[transform_nodes[i]]}', 
        # ax1.annotate(f'node {numeric_nodes[i]}', 
                        xy=(time_series[i], transform_nodes[i]), 
                        xytext=(time_series[i], rssi_max + 3),
                        # xytext=(time_series[i] + 2, -40),
                        # xytext=(time_series[i] + 2, transform_nodes[i] + 0.1),
                        textcoords='data',
                        fontsize=18,
                        fontweight='bold',
                        color='black')
        
        ax1.axvline(x=time_series[i], color='black', linestyle='--', alpha=0.5)

# Add a legend
ax1.legend(loc='best')
# # # # # # lines, labels = ax1.get_legend_handles_labels()
# # # # # # lines2, labels2 = ax2.get_legend_handles_labels()
# # # # # # ax1.legend(lines + lines2, labels + labels2, loc='best')

# Customize the plot
plt.title(title)
plt.suptitle(main_title, fontweight='bold')
plt.grid(True)
plt.savefig(f'{dir_memoria}plot.png', format='png', bbox_inches='tight')
plt.show()