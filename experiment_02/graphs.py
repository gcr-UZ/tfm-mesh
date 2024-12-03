import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read the file
file_path = './results/02.txt'  # Replace with your file path
data = []

with open(file_path, 'r') as f:
    for line in f:
        # Split the line to extract timestamp and signal level
        parts = line.split()
        timestamp_str = parts[0]# + ' ' + parts[1]  # Combine date and time
        # print(parts[-1].split('=')[-1])
        rssi_level = parts[-1].split('=')[-1]
        if rssi_level[0] == '-':
            signal_level = int(rssi_level)  # Extract the signal level (the last part)
        else:
            signal_level = -120
        # print(timestamp_str)
        # print(signal_level)
        # exit()
        # Convert the timestamp string to a datetime object
        timestamp = datetime.strptime(timestamp_str, '%Y%m%d-%H:%M:%S.%f')
        
        # Append the data
        data.append((timestamp, signal_level))

# Convert to pandas DataFrame
df = pd.DataFrame(data, columns=['Timestamp', 'Signal Level'])

# Plot the signal levels over time
plt.figure(figsize=(10, 6))
plt.plot(df['Timestamp'], df['Signal Level'])
plt.title('Signal Level Over Time')
plt.xlabel('Time')
plt.ylabel('Signal Level (dBm)')
plt.grid(True)
plt.xticks(rotation=45)
plt.ylim(-120, 0)  # Set y-axis limits
plt.tight_layout()

# Show the plot
plt.show()
