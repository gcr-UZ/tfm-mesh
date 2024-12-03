import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import re
from matplotlib.ticker import MaxNLocator

usage = f"Usage: {sys.argv[0]}  {{intel|alfa1|alfa2}} exp_number [-j]"
jitter = False

print(len(sys.argv))
if len(sys.argv) != 3 and len(sys.argv) != 4:
    print(usage)
    exit(-1)

card = sys.argv[1]
print(sys.argv[1])

if (card != "intel") and (card != "alfa1") and (card != "alfa2"):
    print(usage)
    exit(-1)

if len(sys.argv) == 4:
    if sys.argv[3] != "-j":
        print(usage)
        exit(-1)
    else:
        jitter = True

cardd = sys.argv[1]
numberr = sys.argv[2]

if card == "intel":
    main_title = f"Intel (Intel Wi-Fi 6 AX201) -> {numberr}\n\n"
elif card == "alfa1":
    main_title = f"Alfa1 (Alfa AWUS036ACHM) -> {numberr}\n\n"
else:
    main_title = f"Alfa 2 (Alfa AWUS036AXML) -> {numberr}\n\n"

# Read the signal data file
signal_file_path = f'./results/{cardd}_rssi_{numberr}.txt'  # Replace with your file path
signal_data = []

with open(signal_file_path, 'r') as f:
    for line in f:
        parts = line.split('Access Point')  # Split on 'Access Point'
        timestamp_str = parts[0].strip()  # Get the timestamp string

        rssi_level = parts[1].split('level=')[-1]
        if rssi_level[0] == '-':
            signal_level = int(rssi_level)  # Extract the signal level (the last part)
        else:
            signal_level = -120
        # # signal_level = int(parts[1].split('level=')[-1])  # Extract the signal level (after 'level=')

        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d-%H:%M:%S.%f')

        # Append the data
        signal_data.append((timestamp, signal_level))

# Convert to pandas DataFrame
df_signal = pd.DataFrame(signal_data, columns=['Timestamp', 'Signal Level'])
x_axisss_time_signal = pd.DataFrame(np.linspace(0, 60, df_signal['Timestamp'].size), columns=['X time signal'])

# Read the loss data file
loss_file_path = f'./results/{cardd}_iperf_{numberr}.txt'  # Replace with your file path
loss_data = []
jitter_data = []

loss_percentage_pattern = re.compile(r'(\d+)/\d+ \((\d+(\.\d+)?)%\)')
jitter_pattern = re.compile(r'\d+\.\d+\s+ms')

# total_datagrams = []

with open(loss_file_path, 'r') as f:
    for line in f:
        # Look for lines with the data
        match = loss_percentage_pattern.search(line)
        if match:
            timestamp_str = line.split()[0]# + ' ' + line.split()[1]  # Combine date and time
            # print(str(match.group(0)) + "--" + str(match.group(1)) + "--" + str(match.group(2)))

            # print(str(match.group(0)))
            if str(match.group(0)) == "0/0 (0%)":
                print("YES")
                loss_percentage = float(100)  # Extract loss percentage
            else:
                loss_percentage = float(match.group(2))  # Extract loss percentage
            
            # Convert the timestamp string to a datetime object
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d-%H:%M:%S.%f')

            lost_and_total = str(match.group(0)).split(' ')[0].split('/')
            # received_packets = int(lost_and_total[1])
            received_packets = int(lost_and_total[1]) - int(lost_and_total[0])
            # print(f'{lost_and_total[0]} -- {lost_and_total[1]}')
            # print(received_packets)
            
            # Append the data
            loss_data.append((timestamp, loss_percentage, received_packets))

        # match2 = re.search(r'/(\d+)', line)
        # if match2:
        #         total_datagrams.append((timestamp, int(match.group(1))))

        ## Jitter
        if jitter:
            j_match = jitter_pattern.search(line)
            if j_match:
                timestamp_str = line.split()[0]
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d-%H:%M:%S.%f')
                # print(j_match.group(0).split(' ')[0])
                jitter_data.append((timestamp, float(j_match.group(0).split(' ')[0])))


# Convert to pandas DataFrame
df_loss = pd.DataFrame(loss_data, columns=['Timestamp', 'Loss Percentage', 'Received Packets'])
# df_datagrams = pd.DataFrame(total_datagrams, columns=['Timestamp', 'Total Datagrams'])
x_axisss_time = pd.DataFrame(np.linspace(0, 60, df_loss['Timestamp'].size), columns=['X time'])
# print(f"EYYYY - {df_loss['Timestamp'].size}")

if jitter:
    df_jitter = pd.DataFrame(jitter_data, columns=['Timestamp', 'Jitter'])
    x_axisss_time_jitter = pd.DataFrame(np.linspace(0, 60, df_jitter['Timestamp'].size), columns=['X time Jitter'])



# Create plots
n_plots = 3
if jitter:
    n_plots = 4
fig, axs = plt.subplots(n_plots, 1, figsize=(10, 12))

# prefixxxx = f"{cardd} {numberr} ->"
prefixxxx = f""

# Plot the signal levels over time
# axs[0].plot(df_signal['Timestamp'], df_signal['Signal Level'])
i_rssi = 0
i_jitter = 3
if jitter:
    i_rssi = 3
    i_jitter = 0
axs[i_rssi].plot(x_axisss_time_signal, df_signal['Signal Level'])
axs[i_rssi].set_title(f"{prefixxxx}{main_title}RSSI a lo largo del tiempo", fontweight='bold')
# axs[i_rssi].set_title(f"{prefixxxx}RSSI a lo largo del tiempo", fontweight='bold')
axs[i_rssi].set_xlabel('Tiempo (s)')
axs[i_rssi].set_ylabel('RSSI (dBm)')
axs[i_rssi].grid(True)
axs[i_rssi].set_ylim(-120, 0)  # Set y-axis limits

# Plot the loss percentage over time
# axs[1].plot(df_loss['Timestamp'], df_loss['Loss Percentage'], color='red')
axs[1].plot(x_axisss_time, df_loss['Loss Percentage'], color='red')
axs[1].set_title(f"{prefixxxx}Porcentaje de paquetes perdidos a lo largo del tiempo (muestreado cada 0.1ms)", fontweight='bold')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('%')
axs[1].grid(True)
axs[1].set_ylim(0, 100)  # Set y-axis limits

# axs[1].plot(df_datagrams['Timestamp'], df_datagrams['Total Datagrams'], color='green')

# print(df_loss['Received Packets'].size)
# axs[2].plot(df_loss['Timestamp'], df_loss['Received Packets'], color='blue')
# axs[2].plot(df_loss['Timestamp'], df_loss['Received Packets'].size*[100], color='yellow')
axs[2].plot(x_axisss_time, df_loss['Received Packets'], color='blue')
axs[2].plot(x_axisss_time, df_loss['Received Packets'].size*[100], color='yellow')
axs[2].set_title(f"{prefixxxx}Número de paquetes recibidos a lo largo del tiempo (muestreado cada 0.1s)", fontweight='bold')
axs[2].set_xlabel('Tiempo (s)')
axs[2].set_ylabel('Nº Paquetes')
axs[2].grid(True)
axs[2].set_ylim(0, 400)  # Set y-axis limits
mean = df_loss[df_loss['Received Packets'] <= 1000]['Received Packets'].mean()
std = df_loss[df_loss['Received Packets'] <= 1000]['Received Packets'].std()
axs[2].text(1, 1, f'Mean = {mean}', transform=axs[2].transAxes, fontsize=12, color='purple',
         verticalalignment='top', horizontalalignment='right')
axs[2].text(1, 0.90, f'Std =  {std}', transform=axs[2].transAxes, fontsize=12, color='purple',
         verticalalignment='top', horizontalalignment='right')         


if jitter:
    axs[i_jitter].plot(x_axisss_time_jitter, df_jitter['Jitter'])
    # axs[i_jitter].set_title(f"{prefixxxx}{main_title}Jitter a lo largo del tiempo (muestreado cada 0.1s)", fontweight='bold')
    axs[i_jitter].set_title(f"{prefixxxx}Jitter a lo largo del tiempo (muestreado cada 0.1s)", fontweight='bold')
    axs[i_jitter].set_xlabel('Tiempo (s)')
    axs[i_jitter].set_ylabel('Jitter (ms)')
    axs[i_jitter].grid(True)
    axs[i_jitter].set_ylim(0, 5)  # Set y-axis limits


# ax2 = axs[1].twinx()
# ax2.plot(df_loss['Timestamp'], df_loss['Received Packets'] / 2)
# ax2.set_ylabel('cos(x)', color='b')
# # ax2.tick_params(axis='y', labelcolor='blue', rotation=45)
# ax2.tick_params(axis='x', rotation=45)

# ax2.set_ylim(0, 100)  # Set y-axis limits


# print(df_loss['Received Packets'])
# print(df_loss['Loss Percentage'])



# Format x-axis labels
for ax in axs:
    ax.tick_params(axis='x', rotation=45)
    ax.set_xticks(range(0, 61, 5))
    ax.set_xticks(range(0, 61, 1), minor=True)
    ax.grid(which='minor', linestyle='-', linewidth='0.2', color='gray', alpha=0.5)
    
plt.tight_layout()

hspace=0.36
if jitter:
    hspace=0.47
plt.subplots_adjust(hspace=hspace)





## Calcular media y std de paquetes recibidos diferenciando por NODO
prev = 1
summ = []
summ_jitter = []
j = 0
# count = 0
for i in df_loss['Received Packets']:
    if prev == 0 and i == prev:
        if len(summ) == 0:
            continue
        print(':)')
        print('-- Paquetes recibidos --')
        dff = pd.DataFrame(summ, columns=['summ'])
        m = dff['summ'].mean()
        std = dff['summ'].std()
        print(f'Media: {m}')
        print(f'Std: {std}')
        print(f'{len(summ)}')
        summ = []
        if jitter:
            print('-- Jitter --')
            dff_j = pd.DataFrame(summ_jitter, columns=['summ_jitter'])
            m_j = dff_j['summ_jitter'].mean()
            std_j = dff_j['summ_jitter'].std()
            print(f'Media: {m_j}')
            print(f'Std: {std_j}')
            print(f'{len(dff_j)}')
            summ_jitter = []
        continue
    prev = i
    # summ += i
    # count += 1
    if jitter:
        summ.append(i)
        summ_jitter.append(df_jitter['Jitter'][j])
        j = j + 1

print(':)')
print('-- Paquetes recibidos --')
dff = pd.DataFrame(summ, columns=['summ'])
m = dff['summ'].mean()
std = dff['summ'].std()
print(f'Media: {m}')
print(f'Std: {std}')
print(f'{len(summ)}')
if jitter:
    print('-- Jitter --')
    dff_j = pd.DataFrame(summ_jitter, columns=['summ_jitter'])
    m_j = dff_j['summ_jitter'].mean()
    std_j = dff_j['summ_jitter'].std()
    print(f'Media: {m_j}')
    print(f'Std: {std_j}')
    print(f'{len(dff_j)}')
    summ_jitter = []












# Show the plots
plt.show()

# plt.clf()
# plt.close()






# fig, ax1 = plt.subplots(figsize=(12, 6))
# ax1.plot(x_axisss_time_signal, df_signal['Signal Level'], color='blue', label='RSSI (dBm)', zorder=1)
# ax1.set_xlabel('Tiempo (s)')
# ax1.set_ylabel('RSSI (dBm)', color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')

# plt.grid(True)
# ax1.tick_params(axis='x', rotation=45)
# ax1.set_xticks(range(0, 61, 5))
# ax1.set_xticks(range(0, 61, 1), minor=True)
# ax1.grid(which='minor', linestyle='-', linewidth='0.2', color='gray', alpha=0.5)

# ax1.legend(loc='best')

# plt.title('title')
# plt.suptitle('main_title', fontweight='bold')


# # plt.title("Figure 2 cleared with clf()")
# plt.show()








# fig, ax1 = plt.subplots(figsize=(12, 6))
# ax1.plot(x_axisss_time, df_loss['Loss Percentage'], color='red', label='%', zorder=1)
# ax1.set_xlabel('Tiempo (s)')
# ax1.set_ylabel('%', color='red')
# ax1.tick_params(axis='y', labelcolor='red')

# plt.grid(True)
# ax1.tick_params(axis='x', rotation=45)
# ax1.set_xticks(range(0, 61, 5))
# ax1.set_xticks(range(0, 61, 1), minor=True)
# ax1.grid(which='minor', linestyle='-', linewidth='0.2', color='gray', alpha=0.5)

# ax1.legend(loc='best')

# plt.title('title')
# plt.suptitle('main_title', fontweight='bold')


# # plt.title("Figure 2 cleared with clf()")
# plt.show()








# fig, ax1 = plt.subplots(figsize=(12, 6))
# ax1.plot(x_axisss_time, df_loss['Received Packets'], color='blue', label='Nº Paquetes', zorder=1)
# ax1.set_xlabel('Tiempo (s)')
# ax1.set_ylabel('Nº Paquetes', color='blue')
# ax1.tick_params(axis='y', labelcolor='blue')

# plt.grid(True)
# ax1.tick_params(axis='x', rotation=45)
# ax1.set_xticks(range(0, 61, 5))
# ax1.set_xticks(range(0, 61, 1), minor=True)
# ax1.grid(which='minor', linestyle='-', linewidth='0.2', color='gray', alpha=0.5)

# ax1.legend(loc='best')

# plt.title('title')
# plt.suptitle('main_title', fontweight='bold')


# # plt.title("Figure 2 cleared with clf()")
# plt.show()