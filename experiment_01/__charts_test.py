import re
import matplotlib.pyplot as plt

# # # # # Sample data as a multi-line string for this example
# # # # data = """
# # # # ESSID="GTE_MESH"   MAC_AP= 30:DE:4B:D2:69:7B    node=Node_1
# # # # Frequency=5.22 GHz  Vt=866.7 Mb/s
# # # # Ptx=22 dBm
# # # # Link Quality=70/70 RSSI=-37 dBm
# # # # ---------------------------
# # # # ESSID="GTE_MESH"   MAC_AP= 30:DE:4B:D2:69:7B    node=Node_1
# # # # Frequency=5.22 GHz  Vt=866.7 Mb/s
# # # # Ptx=22 dBm
# # # # Link Quality=66/70 RSSI=-44 dBm
# # # # ---------------------------
# # # # ESSID="GTE_MESH"   MAC_AP= 30:DE:4B:D2:69:7B    node=Node_1
# # # # Frequency=5.22 GHz  Vt=866.7 Mb/s
# # # # Ptx=22 dBm
# # # # Link Quality=66/70 RSSI=-44 dBm
# # # # ---------------------------
# # # # ESSID="GTE_MESH"   MAC_AP= 30:DE:4B:D2:69:7B    node=Node_1
# # # # Frequency=5.22 GHz  Vt=866.7 Mb/s
# # # # Ptx=22 dBm
# # # # Link Quality=68/70 RSSI=-42 dBm
# # # # """

with open('./ax201/01_2nodes_norouter.txt', 'r') as file:
    data = file.read()

# Initialize lists to hold the extracted data
timestamps = []
rssi_values = []
nodes = []
numeric_nodes = []

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
        rssi_values.append(int(rssi_match.group(1)))
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

print("Timestamps:", timestamps)
print("RSSI Values:", rssi_values)
print("Nodes:", nodes)

rssi_average = sum(rssi_values) / len(rssi_values)
print(rssi_average)
# exit()


## NODOS YA MEJOR PERO CON MUCHO RANGO
unique_nodes = list(set(nodes))
node_map = {node: i+1 for i, node in enumerate(unique_nodes)}  # Start numbering from 1
# numeric_nodes = [node_map[node] for node in nodes]
print(nodes)
print(node_map)
print(numeric_nodes)

transform_nodes = []
dict = {}

for x in numeric_nodes:
    if x == 1:
        transform_nodes.append(rssi_average)
        dict[rssi_average] = x
    elif x == 2:
        transform_nodes.append(rssi_average - 5)
        dict[rssi_average - 5] = x

# numeric_nodes = [rssi_average if x == 1 else x for x in numeric_nodes]
# numeric_nodes = [rssi_average - 5 if x == 2 else x for x in numeric_nodes]

# Create a time series for x-axis
time_series = list(range(1, len(rssi_values) + 1))

fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot RSSI over time on the primary y-axis
ax1.plot(time_series, rssi_values, color='blue', marker='o', label='RSSI (dBm)')
ax1.set_xlabel('Time')
ax1.set_ylabel('RSSI (dBm)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')


# ax1.plot(time_series, numeric_nodes, color='orange', marker='-', label='Ptx (dBm)')
# ax1.plot(time_series, transform_nodes, color='orange', linestyle='--', label='Ptx (dBm)')

# Annotate the nodes
for i in range(len(transform_nodes)):
    if i == 0 or transform_nodes[i] != transform_nodes[i - 1]:
        ax1.annotate(f'node {dict[transform_nodes[i]]}', 
        # ax1.annotate(f'node {numeric_nodes[i]}', 
                        xy=(time_series[i], transform_nodes[i]), 
                        xytext=(time_series[i], -40),
                        # xytext=(time_series[i] + 2, -40),
                        # xytext=(time_series[i] + 2, transform_nodes[i] + 0.1),
                        textcoords='data',
                        fontsize=18,
                        fontweight='bold',
                        color='black')
        
        ax1.axvline(x=time_series[i], color='black', linestyle='--', alpha=0.5)





# Add a legend
ax1.legend(loc='best')


#  # Create a secondary y-axis for Ptx values
# ax2 = ax1.twinx()
# ax2.plot(time_series, numeric_nodes, color='green', marker='x', label='Ptx (dBm)')
# ax2.set_ylabel('Ptx (dBm)', color='green')
# ax2.tick_params(axis='y', labelcolor='green')

# # Adding a legend
# lines, labels = ax1.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()
# ax1.legend(lines + lines2, labels + labels2, loc='best')

# Customize the plot
plt.title('RSSI and Nodes over Time')
plt.grid(True)
plt.show()





# # # # Create a secondary y-axis for the numeric node values
# # # ax2 = ax1.twinx()
# # # ax2.step(time_series, numeric_nodes, color='orange', where='mid', linestyle='--', label='Node')
# # # ax2.set_ylabel('Node', color='orange')
# # # ax2.tick_params(axis='y', labelcolor='orange')
# # # ax2.set_yticks(list(node_map.values()))
# # # ax2.set_yticklabels(list(node_map.keys()))

# # # # Annotate the nodes
# # # for i in range(len(numeric_nodes)):
# # #     if i == 0 or numeric_nodes[i] != numeric_nodes[i - 1]:
# # #         ax2.annotate(f'node {numeric_nodes[i]}', 
# # #                         xy=(time_series[i], numeric_nodes[i]), 
# # #                         xytext=(time_series[i] + 2, numeric_nodes[i] + 0.1),
# # #                         textcoords='data',
# # #                         fontsize=12,
# # #                         color='orange')

# # # # Adding a legend
# # # lines, labels = ax1.get_legend_handles_labels()
# # # lines2, labels2 = ax2.get_legend_handles_labels()
# # # ax1.legend(lines + lines2, labels + labels2, loc='best')

# # # # Customize the plot
# # # plt.title('RSSI and Node over Time')
# # # plt.grid(True)
# # # plt.show()

























## NODOS CON LINEA PERO ESCALA NUMERICA QUE NO ME GUSTA
# # # unique_nodes = list(set(nodes))
# # # node_map = {node: i for i, node in enumerate(unique_nodes)}
# # # numeric_nodes = [node_map[node] for node in nodes]

# # # # Normalize node values to be in the middle range of RSSI values
# # # rssi_min = min(rssi_values)
# # # rssi_max = max(rssi_values)
# # # node_min = min(numeric_nodes)
# # # node_max = max(numeric_nodes)
# # # norm_nodes = [
# # #     ((n - node_min) / (node_max - node_min)) * (rssi_max - rssi_min) + rssi_min
# # #     for n in numeric_nodes
# # # ]


# # # # Create a time series for x-axis
# # # time_series = list(range(1, len(rssi_values) + 1))

# # # fig, ax1 = plt.subplots(figsize=(12, 6))

# # # # Plot RSSI over time on the primary y-axis
# # # ax1.plot(time_series, rssi_values, color='blue', label='RSSI (dBm)')
# # # ax1.set_xlabel('Time')
# # # ax1.set_ylabel('RSSI (dBm)', color='blue')
# # # ax1.tick_params(axis='y', labelcolor='blue')

# # # # Plot normalized node values
# # # ax1.step(time_series, norm_nodes, color='orange', where='mid', linestyle='--', label='Node')

# # # # Annotate the nodes
# # # for i in range(len(norm_nodes)):
# # #     if i == 0 or norm_nodes[i] != norm_nodes[i - 1]:
# # #         ax1.annotate(f'node {norm_nodes[i]}', 
# # #                         xy=(time_series[i], norm_nodes[i]), 
# # #                         xytext=(time_series[i] + 2, norm_nodes[i] + 0.1),
# # #                         textcoords='data',
# # #                         fontsize=12,
# # #                         color='orange')

# # # # Adding a legend
# # # lines, labels = ax1.get_legend_handles_labels()
# # # ax1.legend(lines, labels, loc='best')

# # # # Customize the plot
# # # plt.title('RSSI and Node over Time')
# # # plt.grid(True)
# # # plt.show()




## NODOS YA MEJOR PERO CON MUCHO RANGO
# # # # # # unique_nodes = list(set(nodes))
# # # # # # node_map = {node: i+1 for i, node in enumerate(unique_nodes)}  # Start numbering from 1
# # # # # # numeric_nodes = [node_map[node] for node in nodes]

# # # # # # unique_nodes = list(set(nodes))
# # # # # # node_map = {node: i+1 for i, node in enumerate(unique_nodes)}  # Start numbering from 1
# # # # # # numeric_nodes = [node_map[node] for node in nodes]

# # # # # # # Create a time series for x-axis
# # # # # # time_series = list(range(1, len(rssi_values) + 1))

# # # # # # fig, ax1 = plt.subplots(figsize=(12, 6))

# # # # # # # Plot RSSI over time on the primary y-axis
# # # # # # ax1.plot(time_series, list(map(int, rssi_values)), color='blue', label='RSSI (dBm)')
# # # # # # ax1.set_xlabel('Time')
# # # # # # ax1.set_ylabel('RSSI (dBm)', color='blue')
# # # # # # ax1.tick_params(axis='y', labelcolor='blue')

# # # # # # # Create a secondary y-axis for the numeric node values
# # # # # # ax2 = ax1.twinx()
# # # # # # ax2.step(time_series, numeric_nodes, color='orange', where='mid', linestyle='--', label='Node')
# # # # # # ax2.set_ylabel('Node', color='orange')
# # # # # # ax2.tick_params(axis='y', labelcolor='orange')
# # # # # # ax2.set_yticks(list(node_map.values()))
# # # # # # ax2.set_yticklabels(list(node_map.keys()))

# # # # # # # Annotate the nodes
# # # # # # for i in range(len(numeric_nodes)):
# # # # # #     if i == 0 or numeric_nodes[i] != numeric_nodes[i - 1]:
# # # # # #         ax2.annotate(f'node {numeric_nodes[i]}', 
# # # # # #                         xy=(time_series[i], numeric_nodes[i]), 
# # # # # #                         xytext=(time_series[i] + 2, numeric_nodes[i] + 0.1),
# # # # # #                         textcoords='data',
# # # # # #                         fontsize=12,
# # # # # #                         color='orange')

# # # # # # # Adding a legend
# # # # # # lines, labels = ax1.get_legend_handles_labels()
# # # # # # lines2, labels2 = ax2.get_legend_handles_labels()
# # # # # # ax1.legend(lines + lines2, labels + labels2, loc='best')

# # # # # # # Customize the plot
# # # # # # plt.title('RSSI and Node over Time')
# # # # # # plt.grid(True)
# # # # # # plt.show()





## NODOS CON LINEA PERO MAL LA ESCALA
# # # unique_nodes = list(set(nodes))
# # # node_map = {node: i for i, node in enumerate(unique_nodes)}
# # # numeric_nodes = [node_map[node] for node in nodes]


# # # # # # # Create a time series for x-axis
# # # # # # time_series = list(range(1, len(rssi_values) + 1))

# # # # # # fig, ax1 = plt.subplots(figsize=(12, 6))

# # # # # # # Plot RSSI over time on the primary y-axis
# # # # # # ax1.plot(time_series, list(map(int, rssi_values)), color='blue', marker='o', label='RSSI (dBm)')
# # # # # # ax1.set_xlabel('Time')
# # # # # # ax1.set_ylabel('RSSI (dBm)', color='blue')
# # # # # # ax1.tick_params(axis='y', labelcolor='blue')

# # # # # # # Create a secondary y-axis for the numeric node values
# # # # # # ax2 = ax1.twinx()
# # # # # # ax2.plot(time_series, numeric_nodes, color='red', marker='x', label='Node')
# # # # # # ax2.set_ylabel('Node', color='red')
# # # # # # ax2.tick_params(axis='y', labelcolor='red')

# # # # # # # Adding a legend
# # # # # # lines, labels = ax1.get_legend_handles_labels()
# # # # # # lines2, labels2 = ax2.get_legend_handles_labels()
# # # # # # ax1.legend(lines + lines2, labels + labels2, loc='best')

# # # # # # # Customize the plot
# # # # # # plt.title('RSSI and Node over Time')
# # # # # # plt.grid(True)
# # # # # # plt.show()










## NODOS CON ANOTACION POR PUNTO
# # # # # # # # Plot the data
# # # # # # # plt.figure(figsize=(12, 6))

# # # # # # # # Plot RSSI as a continuous variable
# # # # # # # plt.plot(timestamps, rssi_values, label='RSSI', color='blue', marker='o')

# # # # # # # # Annotate nodes
# # # # # # # for i, node in enumerate(nodes):
# # # # # # #     plt.annotate(node, (timestamps[i], rssi_values[i]), textcoords="offset points", xytext=(0,10), ha='center')

# # # # # # # # Add labels and title
# # # # # # # plt.xlabel('Time')
# # # # # # # plt.ylabel('RSSI (dBm)')
# # # # # # # plt.title('RSSI and Node Over Time')
# # # # # # # plt.legend()
# # # # # # # plt.grid(True)

# # # # # # # # Show plot
# # # # # # # plt.show()
