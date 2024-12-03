import re
import matplotlib.pyplot as plt

# File containing the log
file_path = './results/alfa1_iperf_13.txt'

# List to store jitter values
jitter_values = []

# Open and read the file
with open(file_path, 'r') as file:
    for line in file:
        # Match lines containing data with Jitter values using regex
        match = re.search(r'\d+\.\d+\s+ms', line)
        if match:
            # Extract the Jitter value and convert it to a float (removing "ms")
            jitter = float(match.group().replace(' ms', ''))
            jitter_values.append(jitter)

# Generate an x-axis based on the number of jitter values
time_intervals = [i * 0.1 for i in range(len(jitter_values))]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(time_intervals, jitter_values, linestyle='-', color='blue', label='Jitter (ms)')
plt.title('Jitter Over Time')
plt.xlabel('Time (s)')
plt.ylabel('Jitter (ms)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
