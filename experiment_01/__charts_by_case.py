import argparse
import re
import os
import matplotlib.pyplot as plt

def extract_digits(filename):
    match = re.search(r'(\d{2})\.txt$', filename)
    return int(match.group(1)) if match else None

def get_element(arr, *index):
    # Access the element using the index
    # return arr[index] if len(index) > 1 else arr[index[1]]
    print(plot_rows)
    print(plot_columns)
    return arr[index] if arr.ndim > 1 else arr[index[1]]


"""
docu
"""
def plot_experiment_case(case):
    files, plot_rows, plot_columns = switch_files(case)

    if not files or files is None: 
        print(f"No files have been found for case {case}")
        exit()

    sorted_files = sorted(files, key=extract_digits)


    figure, axis = plt.subplots(plot_rows, plot_columns)
    row = 0
    column = 0

    for f in sorted_files:
        with open(f'./ax201/{f}', 'r') as file:
            data = file.read()

        # Initialize lists to hold the extracted data
        timestamps = []
        rssi_values = []
        nodes = []
        numeric_nodes = []

        rssi_min = 0
        rssi_min_i = 0

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

        for x in numeric_nodes:
            if x == 1:
                transform_nodes.append(rssi_average)
                dict[rssi_average] = x
            elif x == 2:
                transform_nodes.append(rssi_average - 5)
                dict[rssi_average - 5] = x

        # Create a time series for x-axis
        time_series = list(range(1, len(rssi_values) + 1))

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # fig, ax1 = plt.subplots(figsize=(12, 6))

        get_element(axis, row, column).plot(time_series, rssi_values, color='blue', label='RSSI (dBm)', zorder=1)
        get_element(axis, row, column).set_xlabel('Time')
        get_element(axis, row, column).set_ylabel('RSSI (dBm)', color='blue')
        get_element(axis, row, column).tick_params(axis='y', labelcolor='blue')

        # show min rssi
        # plt.scatter(rssi_min_i+1, rssi_min, c='red', marker='o', s=100, zorder=2)
        get_element(axis, row, column).scatter(rssi_min_i+1, rssi_min, c='red', marker='o', s=100, zorder=2)
        get_element(axis, row, column).annotate(f'{rssi_min} dBm', 
                                xy=(rssi_min_i+1, rssi_min), 
                                xytext=(rssi_min_i+1 - 1.4, rssi_min - 3),
                                textcoords='data',
                                fontsize=12,
                                color='red')

        get_element(axis, row, column).set_ylim([ min(rssi_values_no_none) - 10, max(rssi_values_no_none) + 10])
        # plt.gca().set_ylim([ min(rssi_values_no_none) - 10, max(rssi_values_no_none) + 10])
        # plt.gca().set_ylim([ min(rssi_values) - 10, max(rssi_values) + 10])

        # Annotate the nodes
        for i in range(len(transform_nodes)):
            if i == 0 or transform_nodes[i] != transform_nodes[i - 1]:
                get_element(axis, row, column).annotate(f'node {dict[transform_nodes[i]]}', 
                # ax1.annotate(f'node {numeric_nodes[i]}', 
                                xy=(time_series[i], transform_nodes[i]), 
                                xytext=(time_series[i], -35),
                                # xytext=(time_series[i] + 2, -40),
                                # xytext=(time_series[i] + 2, transform_nodes[i] + 0.1),
                                textcoords='data',
                                fontsize=18,
                                fontweight='bold',
                                color='black')
                
                get_element(axis, row, column).axvline(x=time_series[i], color='black', linestyle='--', alpha=0.5)

        # Add a legend
        # axis[row].legend(loc='best')
        get_element(axis, row, column).legend(loc='upper right')

        # Customize the plot
        get_element(axis, row, column).set_title('RSSI and Nodes over Time')
        get_element(axis, row, column).grid(True)
        # plt.show()

        if column == plot_columns - 1:
            column = 0
            row = row + 1
        else:
            column = column + 1
        

    plt.show()


def switch_files(case):
    if case == 1:
        file_pattern = re.compile("^2n_noR_\d{2}\.txt$")
        return [f for f in os.listdir('./ax201') if file_pattern.match(f)], 2, 2
    elif case == 2:
        file_pattern = re.compile("^2n_noR_iperf_\d{2}\.txt$")
        return [f for f in os.listdir('./ax201') if file_pattern.match(f)], 2, 3
    elif case == 3:
        file_pattern = re.compile("^2n_siR_siI_\d{2}\.txt$")
        return [f for f in os.listdir('./ax201') if file_pattern.match(f)], 1, 2
    elif case == 4:
        file_pattern = re.compile("^2n_siR_siI_iperf_\d{2}\.txt$")
        return [f for f in os.listdir('./ax201') if file_pattern.match(f)], 2, 2
    else:
        return None 


"""
Argument parsing stuff.
"""
def parse_args():
    class SmartFormatter(argparse.HelpFormatter):
        def _split_lines(self, text, width):
            if text.startswith('R|'):
                return text[2:].splitlines()  
            # this is the RawTextHelpFormatter._split_lines
            return argparse.HelpFormatter._split_lines(self, text, width)
    
    parser = argparse.ArgumentParser(description="Experiment 01 results.", 
                                     formatter_class=SmartFormatter)
    parser.add_argument("--case", type=int, required=True, help="R|Select the experiment"
                        " case to display results.\n1-> MESH without router\n"
                        "2-> MESH without router + iperf3\n3-> MESH with router + internet\n"
                        "4-> MESH with router + internet + iperf3")
    # parser.add_argument("-t", action="store_true", help="If set, something happens.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    plot_experiment_case(args.case)